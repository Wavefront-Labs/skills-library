---
id: computing-software.database-administration.couchdb.server-admins-config
name: server-admins-config
category: computing-software
field: database-administration
product: couchdb
tags: [admins, authentication, pbkdf2, hashed-passwords, config-api]
level: practitioner
status: docs-checked
description: "Create and manage CouchDB server administrators in the [admins] config section or via /_node/{node}/_config/admins, including raw=true hashed passwords."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/auth.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 3.0.0, CouchDB requires an admin account to start; with none it prints an error and terminates.

Admins are not stored in `_users` but in the last `[admins]` section found in the ini chain (for example `local.ini` or `local.d/10-admins.ini`). Secure that file so it is readable only by system administrators.

```ini
[admins]
admin = mysecretpassword
```

Plaintext entries are salted and hashed when CouchDB restarts (stored as `-pbkdf2-...` or `-hashed-...` strings). Alternatively use the HTTP API, which needs no restart and no plaintext in files:

- `GET /_node/{node-name}/_config/admins` lists admins and their hashes.
- `PUT /_node/{node-name}/_config/admins/{name}` creates one; DELETE removes one.

To store an already hashed string (from an old ini or another server) without double hashing, add `?raw=true`:

```
PUT /_node/nonode@nohost/_config/admins/architect?raw=true
"-pbkdf2-<hash>,<salt>,<iterations>"
```

## Checked

2026-11-04. Confirmed against the CouchDB config/auth page (Server Administrators): 3.0.0 admin requirement, last [admins] section in the ini chain, securing the file, hashing on restart, -hashed- and -pbkdf2- formats, the _config/admins endpoint and raw=true. Nothing removed.

Method: documentation only; no commands were run.
