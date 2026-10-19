"""MCP Server wrapper for Prompt Injection Canary Sentinel."""
import json
import sys
from client import PromptInjectionCanarySentinel

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "generate_prompt_canary",
                    "description": "Generate invisible zero-width HMAC canary token for system prompt protection",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"secret_id": {"type": "string"}},
                        "required": ["secret_id"]
                    }
                },
                {
                    "name": "audit_response_leak",
                    "description": "Audit response text for zero-width canary leaks indicating prompt exfiltration",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "response_text": {"type": "string"},
                            "expected_hash_prefix": {"type": "string"}
                        },
                        "required": ["response_text", "expected_hash_prefix"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        name = req.get("params", {}).get("name")
        args = req.get("params", {}).get("arguments", {})
        if name == "generate_prompt_canary":
            res = PromptInjectionCanarySentinel.generate_canary(args.get("secret_id", ""))
        else:
            res = PromptInjectionCanarySentinel.audit_response(
                args.get("response_text", ""),
                args.get("expected_hash_prefix", "")
            )
        return {
            "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
        }
    return {}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            try:
                r = json.loads(line)
                out = handle_request(r)
                print(json.dumps(out), flush=True)
            except Exception as e:
                print(json.dumps({"error": str(e)}), flush=True)
