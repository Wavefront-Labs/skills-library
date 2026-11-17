---
id: computing-software.database-administration.couchdb.password-hashing-and-policy
name: password-hashing-and-policy
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, pbkdf2, iterations, password-regexp, upgrade-hash-on-auth]
level: advanced
status: docs-checked
description: "Tune CouchDB PBKDF2 password hashing (iterations, min and max), enforce a password_regexp policy, and auto-upgrade stored hashes."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `[chttpd_auth]`:

- `iterations`: PBKDF2 iteration count (example 10000). Higher is more durable but costs performance on each request needing authentication; with hundreds of thousands of iterations use session cookies. The internal hash is SHA1, which affects the recommended count.
- `min_iterations` / `max_iterations`: users hashed with fewer or more iterations are forbidden (examples 100 and 100000).
- `password_regexp` (3.2): new passwords must match all listed regular expressions; each may be paired with a reason text:

```ini
password_regexp = [{".{10,}", "Min length is 10 chars."}, "[A-Z]+", "[a-z]+", "\\d+"]
```

A failing expression's reason is appended to the default "Password does not conform to requirements."

- `upgrade_hash_on_auth` (added 3.4): on the next successful authentication, upgrade the user's stored hash to current hashing settings. The default changed from `false` to `true` in 3.5.0.

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page ([chttpd_auth]): iterations with the SHA1 and session-cookie note, min_iterations and max_iterations, password_regexp (3.2) example and default reason text, upgrade_hash_on_auth (3.4, default change in 3.5.0). Nothing removed.

Method: documentation only; no commands were run.
