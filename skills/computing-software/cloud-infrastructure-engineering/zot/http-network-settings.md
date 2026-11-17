---
id: computing-software.cloud-infrastructure-engineering.zot.http-network-settings
name: http-network-settings
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, http-config, tls-certificate, shutdown-timeout, hsts, realm]
level: practitioner
status: docs-checked
description: "Configure Zot's http block (address, port, realm, TLS) and the graceful shutdown timeout, including HSTS and start-up failure behaviour."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
"http": {
  "address":"127.0.0.1", "port":"8080", "realm":"zot",
  "tls": { "cert":"test/data/server.cert", "key":"test/data/server.key" }
}
```

- `address`, `port`: where Zot listens.
- `realm`: security policy domain.
- `tls.cert`, `tls.key`: paths to the certificate and server key.
- `shutdownTimeout`: maximum time to drain in-flight requests on shutdown. Default `30s`; zero or negative waits with no timeout. Added in v2.1.23. Changing it needs a restart.

Behaviour:
- With TLS, Zot sends a `Strict-Transport-Security` header on every HTTPS response. Confirm subdomains are HTTPS-ready before serving from a parent domain.
- On shutdown Zot stops accepting requests, waits for active ones, then closes storage and metadata. Connections still open at the timeout are closed.
- For large transfers, set a longer termination grace period in the service manager or pod spec.
- Start-up failures such as a port already in use exit with a nonzero status.

## Checked

2026-11-08. Read in full: docs/admin-guide/admin-configuration.md and compared every claim above against it. Removed: the externalUrl bullet (not on this page).

Method: documentation only; no commands were run.
