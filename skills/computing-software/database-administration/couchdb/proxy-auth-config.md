---
id: computing-software.database-administration.couchdb.proxy-auth-config
name: proxy-auth-config
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, proxy-auth, x-auth-couchdb, public-fields, users-db-public]
level: advanced
status: docs-checked
description: "Configure CouchDB proxy authentication headers and secret, and expose selected user document fields with public_fields and users_db_public."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxy auth options, all in `[chttpd_auth]`:

- `x_auth_username`: header with the username (default `X-Auth-CouchDB-UserName`).
- `x_auth_roles`: header with comma-separated roles (default `X-Auth-CouchDB-Roles`).
- `x_auth_token`: header with an HMAC created from `secret` and the username (default `X-Auth-CouchDB-Token`). Optional unless `proxy_use_secret` is `true`.
- `proxy_use_secret`: when `true`, `secret` is required for proxy auth.
- `secret`: must match between the proxy client and the CouchDB node.

Up to CouchDB 3.3.1 only `sha1` validated the token; since 3.3 `hash_algorithms` selects algorithms.

**User documents.**

- `users_db_public = true` lets all users view user documents (default `false`: admins see all, users see only their own).
- `public_fields` is a comma-separated list of user document fields readable by any user (page example: `first_name, last_name, contacts, url`). It requires `users_db_public = true`, which has no other purpose.

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page ([chttpd_auth] options): x_auth_username, x_auth_roles and x_auth_token headers and defaults, proxy_use_secret, secret, hash_algorithms (3.3, sha1 only up to 3.3.1), users_db_public default false, public_fields and its users_db_public requirement. Nothing removed.

Method: documentation only; no commands were run.
