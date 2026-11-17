---
id: computing-software.database-administration.couchdb.jwt-auth-config
name: jwt-auth-config
category: computing-software
field: database-administration
product: couchdb
tags: [authentication, jwt, roles-claim-path, required-claims, bearer-token]
level: advanced
status: docs-checked
description: "Configure CouchDB JWT authentication: required_claims, and mapping roles from nested claims with roles_claim_path instead of deprecated roles_claim_name."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `[jwt_auth]`:

- `required_claims`: comma-separated claims that must be present in a presented token, for example `exp,iat`. A 404 is sent if any are missing.
- `roles_claim_name` (deprecated in 3.3): top-level attribute used as the user's roles; default `_couchdb.roles`.
- `roles_claim_path` (3.3): reads nested role claims. If set, `roles_claim_name` is ignored. No default. `.` nests; `\.` is a literal dot in a key.

```ini
roles_claim_path = resource_access.security\.settings.account.roles
```

**Migrating** from the old default: change the name and escape the dot so it is not read as nesting:

```ini
roles_claim_path = _couchdb\.roles
```

Verify with `GET /_session` and `Authorization: Bearer <JWT token>`: the response `userCtx.roles` should list the roles, and `info.authenticated` should be `jwt`.

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page ([jwt_auth]): required_claims and the 404 on missing claims, roles_claim_name default _couchdb.roles and deprecation in 3.3, roles_claim_path semantics and example, no default, migration to _couchdb\.roles, and the userCtx and authenticated jwt check. Nothing removed.

Method: documentation only; no commands were run.
