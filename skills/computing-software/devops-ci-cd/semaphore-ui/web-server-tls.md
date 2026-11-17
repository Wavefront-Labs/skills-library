---
id: computing-software.devops-ci-cd.semaphore-ui.web-server-tls
name: web-server-tls
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [tls, https, certificate, web-server, network, semaphore-ui]
level: practitioner
status: docs-checked
description: "Enable built-in TLS (v2.12+) and the HTTP-to-HTTPS redirect listener, or terminate TLS at a proxy."
sources:
  - https://semaphoreui.com/docs/admin-guide/security/network
  - https://semaphoreui.com/docs/admin-guide/reverse-proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serve Semaphore over HTTPS

Goal: never expose Semaphore over plain HTTP.

Options: a client-to-site VPN ending on the server, built-in TLS, or a reverse proxy.

Built-in TLS (since v2.12):

```json
{
  "tls": {
    "enabled": true,
    "cert_file": "/path/to/cert/example.com.cert",
    "key_file": "/path/to/key/example.com.key"
  }
}
```

Environment form:

```bash
export SEMAPHORE_TLS_ENABLED=True
export SEMAPHORE_TLS_CERT_FILE=/path/to/cert/example.com.cert
export SEMAPHORE_TLS_KEY_FILE=/path/to/key/example.com.key
```

Redirect listener: add one field to the `tls` block. They are mutually exclusive.

| Bind to | config.json | Variable |
|---|---|---|
| IP and port | `"http_redirect_addr": "172.29.184.90:80"` | `SEMAPHORE_TLS_HTTP_REDIRECT_ADDR` |
| all interfaces, port | `"http_redirect_port": 80` | `SEMAPHORE_TLS_HTTP_REDIRECT_PORT` |

A self-signed certificate (the page's example):

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=US/ST=California/L=San Francisco/O=CompanyName/OU=DevOps/CN=example.com"
```

Gotchas:
- Behind a proxy, set `web_host` to the public URL: Semaphore builds redirect URLs, sets the cookie `Secure` flag and checks the request origin from it; a mismatch breaks sign-in (reverse proxy page).
- Runners with self-signed servers need `runner.connection.server_ca_cert_file`.

## Checked

2026-11-07. Read in full: admin-guide/security/network.md, admin-guide/reverse-proxy/README.md and admin-guide/runners.md. Confirmed: the three options, v2.12 TLS block, environment variables, the mutually exclusive redirect fields, the openssl command, the web_host behaviour and the runner CA option. Corrected: the openssl command now matches the page, and the web_host gotcha uses the reverse proxy page wording instead of "OIDC redirect URIs, webhooks and notification links". Removed: the curl Verify step.
Method: documentation only; no commands were run.
