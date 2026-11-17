---
id: computing-software.database-administration.couchdb.user-document-fields
name: user-document-fields
category: computing-software
field: database-administration
product: couchdb
tags: [security, user-documents, roles, derived-key, create-user]
level: practitioner
status: docs-checked
description: "Mandatory CouchDB user document fields (name, roles, password, derived_key, iterations) and creating a user with PUT /_users/org.couchdb.user:name."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/intro/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fields CouchDB needs for authentication:

- `_id`: the login with the `org.couchdb.user:` prefix.
- `name`: login. Immutable; to rename, create a new user.
- `roles`: array of strings. No built-in roles; you cannot set system roles such as `_admin`. Only admins may assign roles; users have none by default.
- `password`: plaintext may be supplied but is replaced by hashed fields before storage.
- `password_scheme`: `simple` or `pbkdf2`; with `password_sha`, `salt`, `derived_key`, `iterations`, and `pbkdf2_prf` (assumed `sha` if missing; may be `sha`, `sha224`, `sha256`, `sha384`, `sha512`).
- `type`: always `user`.

Custom fields are allowed.

**Create a user** (admin credentials):

```
curl -X PUT http://admin:password@localhost:5984/_users/org.couchdb.user:jan \
  -H "Content-Type: application/json" \
  -d '{"name": "jan", "password": "apple", "roles": [], "type": "user"}'
```

Success is `201 Created` with `{"ok":true,"id":"org.couchdb.user:jan","rev":"1-..."}`. Test with `curl -X POST http://localhost:5984/_session -d 'name=jan&password=apple'`.

## Checked

2026-11-04. Confirmed against the CouchDB intro/security page (Users Documents, Creating a New User): mandatory fields and their meanings, immutable name, roles rules, password replacement, password_scheme values, pbkdf2_prf values and default, type, custom fields, the creation request and 201 response, the _session test. Nothing removed.

Method: documentation only; no commands were run.
