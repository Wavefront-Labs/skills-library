---
id: computing-software.ai-ml-engineering.ollama.server-host-and-origins
name: server-host-and-origins
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ollama-host, ollama-origins, cors, expose-network]
level: practitioner
status: docs-checked
description: "Expose Ollama on the network with OLLAMA_HOST and permit browser origins with OLLAMA_ORIGINS."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/api/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach the server from other machines or web pages.

By default Ollama binds `127.0.0.1` on port `11434`. Change the bind address and port with `OLLAMA_HOST`, for example `OLLAMA_HOST=0.0.0.0:11434` to listen on all interfaces. Client commands also read `OLLAMA_HOST`, so a remote server is used with:

```
OLLAMA_HOST=my-server:11434 ollama run phonon "Hello from the server."
```

(The speech capability page shows this form.)

Cross-origin access is controlled by `OLLAMA_ORIGINS`. By default Ollama allows origins `127.0.0.1` and `0.0.0.0`; additional origins are added through this variable. Browser extensions are matched with patterns:

- `chrome-extension://*`
- `moz-extension://*`
- `safari-web-extension://*`

Set these per operating system as described in the environment-variable skill (launchctl, systemctl edit or Windows user variables).

Exposing the port is a decision: local requests need no authentication, per the API authentication page, so anything that can reach the port can use the server. Put a reverse proxy in front if you publish it; the FAQ gives an Nginx configuration and tunnel recipes (ngrok, cloudflared).

## Checked

2026-11-03. `OLLAMA_HOST` default and `OLLAMA_ORIGINS` patterns confirmed against the FAQ (docs.ollama.com/faq); the no-authentication statement against the API authentication page; the remote `OLLAMA_HOST` form against the speech page. Dropped an unsupported remark about where audio plays.

Method: documentation only; no commands were run.
