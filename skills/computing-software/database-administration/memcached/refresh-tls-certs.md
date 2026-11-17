---
id: computing-software.database-administration.memcached.refresh-tls-certs
name: refresh-tls-certs
category: computing-software
field: database-administration
product: memcached
tags: [tls, refresh-certs, certificates, rotation, stats]
level: advanced
status: docs-checked
description: "Rotate memcached TLS certificates without a restart using the refresh_certs command, and monitor cert age."
sources:
  - https://docs.memcached.org/features/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

After replacing certificate files (same names and paths as originally configured), connect and run:

```
refresh_certs
```
Memcached reloads them; new connections use the new certificates, existing connections continue to use session keys created with the old certificates.

Monitor:
- `stats` -> `time_since_server_cert_refresh`: seconds since certs were loaded from disk (alert when this is longer than your renewal interval).
- `stats settings` -> `ssl_*` values.
- `watch connevents` shows TLS protocol errors.

Do this after renewal automation (cron, ACME hooks). Verify with `openssl s_client -connect host:port` and check the certificate dates.

Gotcha: the certificate names and paths must be the same as the originals.

## Checked

Confirmed 2026-11-09: `refresh_certs` reloads certificates without a restart, new connections use the new certificates, existing connections keep session keys from the old ones, names and paths must match the originals, `time_since_server_cert_refresh` in `stats`, `ssl_` settings in `stats settings`, TLS protocol errors in `watch connevents`, and `openssl s_client -connect host:port` as a quick test (TLS Support page; protocol.txt stats and watch sections). Removed the claim that changed paths need a restart.

Method: docs-checked 2026-11-09 against docs.memcached.org TLS Support page and memcached doc/protocol.txt
