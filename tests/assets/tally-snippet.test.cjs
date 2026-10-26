'use strict'

// Behavioural contract for the Tally submission listener shipped in the
// conversion-tracking skill. The snippet runs in a visitor's browser, so it is loaded
// into a vm context with a fake window/document: no real browser, no network.

const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')
const vm = require('node:vm')

const SNIPPET = path.join(
  __dirname, '..', '..', 'skills', 'conversion-tracking', 'assets', 'snippets', 'tally.js',
)
const FORM_ID = 'abc123'

function install(frameSrcSelector = `iframe[src="https://tally.so/embed/${FORM_ID}"]`) {
  const listeners = []
  const frameWindow = {}
  const frame = {
    contentWindow: frameWindow,
    matches: (selector) => selector === frameSrcSelector,
  }
  const window = {
    dataLayer: [],
    addEventListener: (type, listener) => { if (type === 'message') listeners.push(listener) },
  }
  const document = { getElementsByTagName: (tag) => (tag === 'iframe' ? [frame] : []) }
  vm.runInNewContext(fs.readFileSync(SNIPPET, 'utf8'), { window, document })
  assert.equal(listeners.length, 1, 'the snippet registers exactly one message listener')
  const send = (data, overrides = {}) => listeners[0]({
    origin: 'https://tally.so',
    source: frameWindow,
    data: typeof data === 'string' ? data : JSON.stringify(data),
    ...overrides,
  })
  return { window, send }
}

function submission(payload = {}, event = 'Tally.FormSubmitted') {
  return { event, payload: { id: 'sub_1', formId: FORM_ID, fields: [], ...payload } }
}

test('a Tally submission pushes only the form and submission ids', () => {
  const { window, send } = install()
  send(submission({ fields: [{ key: 'q1', label: 'Email', value: 'visitor@example.com' }] }))
  assert.deepEqual(window.dataLayer.map((entry) => ({ ...entry })), [
    { event: 'tally_form_submitted', form_id: FORM_ID, submission_id: 'sub_1' },
  ])
  assert.ok(!JSON.stringify(window.dataLayer).includes('visitor@example.com'))
})

test('the same submission is reported once', () => {
  const { window, send } = install()
  send(submission())
  send(submission())
  assert.equal(window.dataLayer.length, 1)
})

test('messages that are not a verified Tally submission push nothing', () => {
  const { window, send } = install()
  send(submission(), { origin: 'https://tally.so.evil.example' })
  send(submission(), { source: {} })
  send(submission({}, 'Tally.FormLoaded'))
  send(submission({ id: 'bad id!' }))
  send(submission({ formId: 'other' }))
  send('{"event":"Tally.FormSubmitted","payload":')
  send('not json')
  assert.deepEqual(window.dataLayer, [])
})

test('a frame whose src is not the fixed Tally path for that form id is not trusted', () => {
  const { window, send } = install('iframe[src="https://evil.example/embed/abc123"]')
  send(submission())
  assert.deepEqual(window.dataLayer, [])
})

test('payload keys that collide with Object.prototype names do not reject the submission', () => {
  // `constructor` and `toString` exist on every object. A lookup that treats them as
  // wanted metadata keys tries to read their (non-string) values as strings and throws,
  // dropping a real submission.
  const { window, send } = install()
  send(
    '{"event":"Tally.FormSubmitted","payload":{"constructor":{"a":1},"toString":[1],' +
      '"__proto__":{"polluted":true},"id":"sub_9","formId":"abc123","fields":[]}}',
  )
  assert.equal(window.dataLayer.length, 1)
  assert.equal(window.dataLayer[0].submission_id, 'sub_9')
  assert.equal({}.polluted, undefined)
})
