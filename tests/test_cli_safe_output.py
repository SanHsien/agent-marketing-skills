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


def _redact(value: object, secrets: list[object]) -> object:
    script = """
const { safeStringify } = require(process.argv[1])
const input = JSON.parse(process.argv[2])
process.stdout.write(safeStringify(input.value, input.secrets))
"""
    result = subprocess.run(
        ["node", "-e", script, str(HELPER), json.dumps({"value": value, "secrets": secrets})],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def test_a_secret_that_contains_another_secret_is_redacted_whole() -> None:
    """Replacing the shorter secret first left the tail of the longer one in the output."""
    for secrets in (["abc", "abcdef"], ["abcdef", "abc"]):
        assert _redact({"message": "bad key abcdef rejected"}, secrets) == {
            "message": "bad key *** rejected"
        }


def test_a_missing_or_empty_secret_redacts_nothing() -> None:
    assert _redact({"message": "plain text"}, [None, "", "***"]) == {"message": "plain text"}
