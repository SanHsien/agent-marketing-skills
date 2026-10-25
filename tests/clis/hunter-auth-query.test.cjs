const { test } = require('node:test')
const assert = require('node:assert/strict')
const { spawnSync } = require('node:child_process')
const path = require('node:path')
const cli = path.resolve(__dirname, '../../tools/clis/hunter.js')

function run(args, key, network = false) {
  const code = `global.fetch = async (url, options) => {
    if (!${network}) throw new Error('Unexpected request');
    return {status: 200, text: async () => JSON.stringify({url: String(url), method: options.method})};
  }; process.argv = ['node', ${JSON.stringify(cli)}, ...${JSON.stringify(args)}]; require(${JSON.stringify(cli)});`
  const r = spawnSync(process.execPath, ['-e', code], {
    encoding: 'utf8', timeout: 5000, env: {...process.env, HUNTER_API_KEY: key},
  })
  assert.equal(r.status, 0, r.stderr)
  return JSON.parse(r.stdout)
}

// 本 fork 的 _safe-output 會遮蔽輸出中所有等於金鑰的字串（含網域裡的片段），寧可多遮也不洩漏。
test('dry run redacts the authentication parameter and every other occurrence of the key', () => {
  const result = run(['domain', 'search', '--domain', 'test-key.example.com', '--dry-run'], 'test-key')
  const query = new URL(result.url).searchParams
  assert.equal(query.get('api_key'), '***')
  assert.equal(query.get('domain'), '***.example.com')
  assert.equal(JSON.stringify(result).includes('test-key'), false)
})

test('query credentials round trip reserved characters without adding extra parameters', () => {
  const key = 'test+key&injected=1#suffix'
  const result = run(['email', 'verify', '--email', 'hello+tag@example.com'], key, true)
  const query = new URL(result.url).searchParams
  assert.equal(query.get('api_key'), key)
  assert.equal(query.get('email'), 'hello+tag@example.com')
  assert.equal(query.has('injected'), false)
})

test('a dry-run account request contains no credential and makes no request', () => {
  const result = run(['account', 'info', '--dry-run'], 'test+key&injected=1#suffix')
  assert.equal(new URL(result.url).searchParams.get('api_key'), '***')
  assert.equal(JSON.stringify(result).includes('injected'), false)
})

test('ordinary live requests retain method, domain and pagination', () => {
  const result = run(['domain', 'search', '--domain', 'example.com', '--limit', '10'], 'test-key', true)
  assert.equal(result.method, 'GET')
  assert.equal(new URL(result.url).searchParams.get('limit'), '10')
  // 輸出會遮蔽回顯的金鑰；金鑰往返請求的行為由上一個測試以複雜金鑰驗證。
  assert.equal(new URL(result.url).searchParams.get('api_key'), '***')
})
