import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "tools" / "clis" / "_safe-output.js"


def test_safe_output_redacts_sensitive_keys_and_values() -> None:
    script = """
const { safeStringify } = require(process.argv[1])
const trickySecret = 'quote"slash\\\\line\\nnext'
process.stdout.write(safeStringify({
  api_key: 'response-secret',
  nested: { token: 'nested-secret', value: 'prefix-live-secret-suffix' },
  escaped: `before-${trickySecret}-after`,
  token_count: 42,
  safe: 'visible'
}, ['live-secret', trickySecret]))
"""
    result = subprocess.run(
        ["node", "-e", script, str(HELPER)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    payload = json.loads(result.stdout)
    assert payload == {
        "api_key": "***",
        "nested": {"token": "***", "value": "prefix-***-suffix"},
        "escaped": "before-***-after",
        "token_count": 42,
        "safe": "visible",
    }
