---
id: computing-software.database-administration.couchdb.admin-only-operations
name: admin-only-operations
category: computing-software
field: database-administration
product: couchdb
tags: [security, admin, authorization, basic-auth, plaintext-passwords]
level: intro
status: docs-checked
description: "Which CouchDB requests need a server admin, creating an admin via local.ini or the config API, and how plaintext passwords are rehashed to -pbkdf2-."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/intro/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
One admin must exist for CouchDB to start. Admin-only requests include: creating or deleting a database, setting `_security`, creating, updating or deleting design documents, triggering compaction, `GET /_active_tasks`, restarting a node, reading or updating `/_node/{node-name}/_config`, and purging documents.

**Create an admin** by hand: add `admin = password` under `[admins]` in `etc/local.ini` and restart. Or via the config API (note the double quotes, since the value is a JSON string):

```
curl -X PUT $HOST/_node/_local/_config/admins/anna -d '"secret"'
```

The response is the previous value (empty string for a new admin). Choose a non-guessable name and a secure password.

**Hashing.** On startup CouchDB rewrites plaintext entries in the ini file as `-pbkdf2-<hash>,<salt>,<iterations>`. The prefix lets it avoid hashing a hash twice, so a plaintext password cannot start with `-pbkdf2-`. The `.ini` files can be edited by hand while CouchDB is stopped.

**Basic auth** (`http://user:pass@host`) sends credentials in plain text; over any shared network use TLS. Without credentials a protected request returns `{"error":"unauthorized","reason":"You are not a server admin."}`.

## Checked

2026-11-04. Confirmed against the CouchDB intro/security page (Authentication, Creating a New Admin User, Hashing Passwords, Basic Authentication): admin-only request list, local.ini and config API creation, previous value returned, -pbkdf2- rehash and prefix rule, plain-text basic auth warning, unauthorized error text. Nothing removed.

Method: documentation only; no commands were run.
