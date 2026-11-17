---
id: computing-software.web-development.vite.server-host-port-hosts
name: server-host-port-hosts
category: computing-software
field: web-development
product: vite
tags: [server-host, server-allowed-hosts, server-port, server-strict-port, server-open]
level: practitioner
status: docs-checked
description: "Dev server listening options: host, allowedHosts (DNS rebinding risk), port 5173, strictPort, https and open with BROWSER variables."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/server-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `server.host` (`string | boolean`, default `'localhost'`): `0.0.0.0` or `true` listens on all addresses. CLI: `--host`. Other servers may answer instead: DNS result ordering can make browsers use a different address, and non-wildcard listeners beat wildcard ones. On WSL2, `host: true` alone is not enough for LAN access.
- `server.allowedHosts` (`string[] | true`, default `[]`): `localhost`, `.localhost` and IPs are allowed; skipped under HTTPS. A leading `.` allows the domain and subdomains. Only add hosts you control, never a TLD like `.com`. `true` allows DNS rebinding attacks that can download your source; env `__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS` adds comma-separated hosts.
- `server.port` (default `5173`): if taken, Vite tries the next port.
- `server.strictPort`: `true` exits instead.
- `server.https`: `https.ServerOptions`, enables TLS + HTTP/2; needs a certificate (`@vitejs/plugin-basic-ssl` makes a cached self-signed one, own certs recommended).
- `server.open` (`boolean | string`): string is the URL pathname. Set `process.env.BROWSER` (for example `firefox`) and `BROWSER_ARGS`, also usable in `.env`.

## Checked

2026-11-04. Confirmed against the Vite server options page (docs/config/server-options.md): host, allowedHosts (defaults, leading dot, DNS rebinding warning, env variable), port 5173, strictPort, https, open with BROWSER and BROWSER_ARGS. Nothing removed.

Method: documentation only; no commands were run.
