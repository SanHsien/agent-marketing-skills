const SENSITIVE_KEYS = new Set([
  'apikey',
  'apisecret',
  'accesstoken',
  'refreshtoken',
  'idtoken',
  'authorization',
  'password',
  'secret',
  'clientsecret',
  'token',
])

function isSensitiveKey(key) {
  return SENSITIVE_KEYS.has(key.replace(/[^a-z0-9]/gi, '').toLowerCase())
}

function redactText(value, secrets) {
  let redacted = value
  for (const secret of secrets) {
    if (secret && secret !== '***') {
      redacted = redacted.replaceAll(String(secret), '***')
    }
  }
  return redacted
}

// Longest first: when one secret contains another, replacing the shorter one first
// would leave the rest of the longer one in the output.
function replacementOrder(secrets) {
  return [...new Set(secrets.filter(secret => secret && secret !== '***').map(String))]
    .sort((a, b) => b.length - a.length)
}

function safeStringify(value, secrets = []) {
  const ordered = replacementOrder(secrets)
  return JSON.stringify(
    value,
    (key, item) => {
      if (isSensitiveKey(key)) return '***'
      return typeof item === 'string' ? redactText(item, ordered) : item
    },
    2,
  )
}

function writeJson(value, secrets = []) {
  process.stdout.write(`${safeStringify(value, secrets)}\n`)
}

module.exports = { safeStringify, writeJson }
