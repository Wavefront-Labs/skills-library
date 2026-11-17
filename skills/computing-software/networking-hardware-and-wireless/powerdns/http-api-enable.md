---
id: computing-software.networking-hardware-and-wireless.powerdns.http-api-enable
name: http-api-enable
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, http-api, webserver, api-key, webserver-allow-from, x-api-key, prometheus]
level: practitioner
status: docs-checked
description: "Enable the PowerDNS Authoritative HTTP API and webserver: api, api-key, webserver address and password settings, /api/v1 prefix, X-API-Key header, errors and exposure warnings."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/http-api/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable the HTTP API

```
webserver=yes
webserver-address=127.0.0.1
webserver-port=8081
webserver-allow-from=127.0.0.1
api=yes
api-key=changeme
```
Settings: `webserver` (anything but `no` starts it), `webserver-address` (default `127.0.0.1`; a UNIX socket path since 5.0.0, in which case port and allow-from are ignored), `webserver-port`, `webserver-password` (HTTP Basic for stats pages, username ignored), `webserver-allow-from`, `webserver-max-bodysize` (MB), `webserver-connection-timeout` (seconds), `webserver-max-concurrent-connections`, `api`, `api-key`.

Use:
- Prefix `/api/v1`, for example `http://127.0.0.1:8081/api/v1/servers/localhost`.
- Auth header `X-API-Key: <api-key>`.
- `/api/docs` serves the OpenAPI definition (YAML or JSON per `Accept`); `/metrics` serves Prometheus format (since 4.4.0).
- JSON bodies (RFC 7159), ISO 8601 dates. An unknown `Accept` or `*/*` returns 400; invalid JSON or non-object body 400; failed validation 422.

Security:
- Before 4.1.0 changing `webserver-address` opened access from anywhere; always set a password and ACL.
- The webserver exposes sensitive data (query and remote-host lists), so restrict it to clients that need it.
- It cannot manage the daemon remotely, though it does control query and response ring sizes.

## Checked

2026-11-04. Read http-api/index.rst in full and confirmed the webserver settings and descriptions, 127.0.0.1 default, UNIX socket from 5.0.0, pre-4.1.0 ACL warning, metrics endpoint since 4.4.0, api and api-key lines, /api/v1 prefix, X-API-Key header, /api/docs formats and the error and data format rules. Nothing removed.

Method: documentation only; no commands were run.
