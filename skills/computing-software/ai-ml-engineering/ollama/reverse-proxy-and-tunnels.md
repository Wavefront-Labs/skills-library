---
id: computing-software.ai-ml-engineering.ollama.reverse-proxy-and-tunnels
name: reverse-proxy-and-tunnels
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [nginx, ngrok, cloudflared, host-header, proxy-pass]
level: advanced
status: docs-checked
description: "Publish Ollama through Nginx, ngrok or cloudflared, rewriting the Host header to localhost:11434."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/api/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: put a proxy or tunnel in front of the local server.

The FAQ documents three patterns.

Nginx reverse proxy: forward requests and set the Host header, as in the FAQ example:

```
server {
    listen 80;
    server_name example.com;
    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host localhost:11434;
    }
}
```

ngrok: the FAQ example rewrites the Host header:

```
ngrok http 11434 --host-header="localhost:11434"
```

cloudflared: the equivalent option is `--http-host-header`:

```
cloudflared tunnel --url http://localhost:11434 --http-host-header="localhost:11434"
```

All three recipes pin the Host header to `localhost:11434`. The FAQ says the proxy headers are optional only when Ollama is not exposed on the network, and that Ollama can be reached through a range of tunneling apps; ngrok and cloudflared are the documented examples.

Proxies for outbound traffic are a separate topic: Ollama honours `HTTPS_PROXY` when pulling models (the FAQ advises avoiding `HTTP_PROXY`, which can disrupt client connections to the server).

Local API calls carry no credentials (API authentication page), so add access control at the proxy yourself.

## Checked

2026-11-03. Nginx, ngrok and cloudflared recipes, `HTTPS_PROXY` advice against the FAQ (docs.ollama.com/faq); no-authentication statement against the API authentication page. Removed the claim that the FAQ explains why the Host header must be rewritten.

Method: documentation only; no commands were run.
