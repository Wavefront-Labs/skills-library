---
id: computing-software.devops-ci-cd.semaphore-ui.reverse-proxy-nginx
name: reverse-proxy-nginx
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [nginx, reverse-proxy, websocket, tls, semaphore-ui]
level: practitioner
status: docs-checked
description: "Put nginx in front of Semaphore with TLS, forwarded headers and the websocket route on /api/ws."
sources:
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy/nginx
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nginx in front of Semaphore

Goal: terminate TLS in nginx and keep the live UI (websocket) working.

```nginx
server {
  listen 443 ssl;
  server_name example.com;
  add_header Strict-Transport-Security "max-age=31536000" always;
  ssl_certificate /etc/nginx/cert/cert.pem;
  ssl_certificate_key /etc/nginx/cert/privkey.pem;
  chunked_transfer_encoding on;

  location / {
    proxy_pass http://127.0.0.1:3000/;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
    proxy_request_buffering off;
  }

  location /api/ws {
    proxy_pass http://127.0.0.1:3000/api/ws;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
  }
}
```

Why the parts matter: task logs stream over a websocket on `/api/ws`, which needs the Upgrade headers (without them the log window stays empty while the task runs); the page comments that `chunked_transfer_encoding on` is required to avoid HTTP 411.

Gotchas:
- Set `web_host` in Semaphore to the public URL; sign-in fails if it does not match what the browser used.
- Use a read timeout longer than the websocket ping interval (Semaphore pings an idle websocket about every two minutes); a proxy that closes idle connections after 60 seconds disconnects the log view repeatedly.
- The page's block also sets `ssl_protocols TLSv1.1 TLSv1.2`, `ssl_ciphers` and `ssl_session_cache`, omitted above; set TLS protocols and ciphers according to your own policy.

Verify: open a running task over HTTPS and confirm its log fills while it runs.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/reverse-proxy/nginx.md and admin-guide/reverse-proxy/README.md. Confirmed: every directive in the server block, the HTTP 411 comment, the websocket route, the ping interval and 60 second timeout remark, and web_host. Removed: the claim that proxy_buffering off lets output stream, the claim that the 411 fix is for some uploads, and the nginx -t Verify step. The ssl_protocols, ssl_ciphers and ssl_prefer_server_ciphers lines of the page's sample were left out of the block on purpose.
Method: documentation only; no commands were run.
