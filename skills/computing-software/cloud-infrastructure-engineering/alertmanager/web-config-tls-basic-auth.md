---
id: computing-software.cloud-infrastructure-engineering.alertmanager.web-config-tls-basic-auth
name: web-config-tls-basic-auth
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, web-config-file, tls-server-config, basic-auth-users]
level: advanced
status: docs-checked
description: "Securing the Alertmanager HTTP listener with --web.config.file: tls_server_config, client_auth_type, http_server_config headers and bcrypt basic_auth_users."
sources: ["https://prometheus.io/docs/alerting/latest/https/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS and basic auth for the web listener

Alertmanager supports basic authentication and TLS. The reference calls this experimental and subject to change. TLS applies to HTTP traffic and gossip traffic.

Load the YAML file with `--web.config.file`. The file is read on every HTTP request, so changes to configuration and certificates are picked up immediately.

```yaml
tls_server_config:
  cert_file: /path/to/server.crt
  key_file: /path/to/server.key
  client_auth_type: RequireAndVerifyClientCert
  client_ca_file: /path/to/ca.crt
basic_auth_users:
  admin: $2y$10$<bcrypt-hash>
```

`tls_server_config` keys:
- `client_auth_type`: default `NoClientCert`. To enable client authentication use `RequireAndVerifyClientCert`; other values are insecure.
- `client_ca_file`, `client_allowed_sans` (exact DNS, IP, email or URI SAN match).
- `min_version` default `TLS12`; `max_version` default `TLS13`.
- `cipher_suites` (empty means Go defaults), `prefer_server_cipher_suites` default `true`, `curve_preferences`.

`http_server_config`: `http2` (default `true`, only with TLS, not changeable on the fly) and `headers` for `Content-Security-Policy`, `X-Frame-Options` (`deny` or `sameorigin`), `X-Content-Type-Options` (`nosniff`), `X-XSS-Protection`, `Strict-Transport-Security`; unset if blank.

`basic_auth_users` maps usernames to bcrypt-hashed passwords. If empty, no basic authentication is required.

## Checked

2026-11-03. Confirmed against the HTTPS and authentication page: tls_server_config, http_server_config, basic_auth_users, defaults.

Method: documentation only; no commands were run.
