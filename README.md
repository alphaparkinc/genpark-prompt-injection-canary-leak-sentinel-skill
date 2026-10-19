# genpark-prompt-injection-canary-leak-sentinel-skill

[![Verified by Smithery](https://smithery.ai/badge/@alphaparkinc/genpark-prompt-injection-canary-leak-sentinel-skill)](https://smithery.ai/servers/@alphaparkinc/genpark-prompt-injection-canary-leak-sentinel-skill)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![Website](https://img.shields.io/badge/Website-GenPark.ai-green)](https://www.genpark.ai)

> HMAC-signed zero-width invisible canary token generator and output response leak auditor for LLM guardrails

## Quick Installation & MCP Integration
Add to your Claude Desktop or Cursor configuration:
```json
{
  "mcpServers": {
    "genpark-prompt-injection-canary-leak-sentinel-skill": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

## Zero Dependencies
Implemented entirely in Python 3 standard library.
