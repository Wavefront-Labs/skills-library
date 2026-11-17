---
id: computing-software.devops-ci-cd.semaphore-ui.reverse-proxy-caddy
name: reverse-proxy-caddy
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [caddy, caddyfile, reverse-proxy, automatic-tls, semaphore-ui]
level: intro
status: docs-checked
description: "Reverse-proxy Semaphore with a minimal Caddyfile that gets automatic TLS and handles websockets."
sources:
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy/caddy
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Caddy in front of Semaphore

Goal: HTTPS with almost no configuration.

Caddy supports websockets and by default only enables secure ciphers (TLS 1.2 and 1.3). Minimal `/etc/caddy/Caddyfile`:

```
example.com {
    reverse_proxy 127.0.0.1:3000 {
        header_up X-Real-IP {client_ip}
    }
}
```

If Caddy cannot obtain a certificate through ACME (firewall, internal domains), add `tls internal` inside the site block to use its internal CA.

Steps:
1. Put the site block in `/etc/caddy/Caddyfile`.
2. Set Semaphore's `web_host` to the public URL (`https://example.com`); Semaphore builds redirect URLs and checks the request origin from it.

Verify: open a running task over HTTPS and confirm its log fills while it runs.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/reverse-proxy/caddy.md and admin-guide/reverse-proxy/README.md. Confirmed: websocket support and TLS 1.2 and 1.3 defaults, the Caddyfile, the `tls internal` advice, and the web_host requirement. Removed: DNS and port steps, the caddy reload command, the advice to keep port 3000 private (tied to JWT proxy auth), the clients-must-trust-root remark, and the curl Verify step, none of which these pages state.
Method: documentation only; no commands were run.
