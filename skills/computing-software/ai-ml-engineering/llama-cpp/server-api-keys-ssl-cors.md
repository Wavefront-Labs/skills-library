---
id: computing-software.ai-ml-engineering.llama-cpp.server-api-keys-ssl-cors
name: server-api-keys-ssl-cors
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, api-key, ssl, cors, security]
level: practitioner
status: docs-checked
description: "Secure llama-server with API keys, TLS certificate flags and CORS origin settings."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API keys, TLS and CORS

**API keys**

- `--api-key KEY`: one or more keys, comma separated (env `LLAMA_API_KEY`).
- `--api-key-file FNAME`: file with one key per line; lines starting with a hash are comments.
- Errors use the OpenAI format; the README's example is `{"error": {"code": 401, "message": "Invalid API Key", "type": "authentication_error"}}`. `GET /health` is public (no API key check).

**TLS**

Build with `-DLLAMA_OPENSSL=ON`, then pass `--ssl-key-file` and `--ssl-cert-file` (PEM files).

**CORS**

- `--cors-origins` default `*`: the Origin header is reflected with credentials allowed. The special value `localhost` reflects only localhost origins.
- `--cors-methods` default `GET, POST, DELETE, OPTIONS`; `--cors-headers` default `*`.
- `--cors-credentials` / `--no-cors-credentials`: default enabled.
- Enabling `--tools`, `--mcp-servers-config`, `--mcp-servers-json` or `--agent` makes `--cors-origins` default to `localhost`; pass it explicitly to override.

Recommended settings: public server, set an API key and use a reverse proxy; local network, set `--cors-origins` to your frontend origin; same machine, `--cors-origins localhost`.

Other related flags: `--host` (comma-separated addresses or `.sock` UNIX socket paths), `--reuse-port`, `--api-prefix PREFIX`. Behind a corporate proxy export `HTTP_PROXY` and `HTTPS_PROXY` before model downloads.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: --api-key, --api-key-file, LLAMA_API_KEY, the 401 error example, /health being public, the OpenSSL build flag and PEM key and certificate flags, all CORS flags and defaults, the localhost default when tools, MCP or agent options are on, the deployment recommendations, --host, --reuse-port, --api-prefix and the proxy variables. Reworded: the 401 line now says it is the README's example.

Method: docs-only read of cited pages, 2026-11-08
