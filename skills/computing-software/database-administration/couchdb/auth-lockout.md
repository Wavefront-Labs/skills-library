---
id: computing-software.database-administration.couchdb.auth-lockout
name: auth-lockout
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, lockout, brute-force, chttpd-auth-lockout, security]
level: practitioner
status: docs-checked
description: "Configure CouchDB automatic user lockout after repeated failed logins: mode off, warn or enforce, threshold, max_lifetime and max_objects."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `[chttpd_auth_lockout]` section tracks failed authentication per username and client IP pair.

- `mode`: `off` does not track failures; `warn` logs a warning on repeated failures; `enforce` (the default) rejects requests with 403.
- `threshold` (default `5`): failed requests within one `max_lifetime` period before further attempts are locked out for the rest of that period (when `enforce`).
- `max_lifetime`: maximum lockout period in milliseconds (page example `300000`). Picked up only at start or restart.
- `max_objects` (default `10,000`): maximum username and IP pairs tracked, to limit memory. Picked up only at start or restart.

```ini
[chttpd_auth_lockout]
mode = enforce
threshold = 5
max_objects = 10000
max_lifetime = 300000
```

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page (chttpd_auth_lockout): mode values and enforce default with 403, threshold default 5, max_objects 10,000, max_lifetime in milliseconds, restart-only note. Nothing removed.

Method: documentation only; no commands were run.
