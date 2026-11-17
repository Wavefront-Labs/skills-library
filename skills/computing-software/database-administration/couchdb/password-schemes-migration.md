---
id: computing-software.database-administration.couchdb.password-schemes-migration
name: password-schemes-migration
category: computing-software
field: database-administration
product: couchdb
tags: [security, password-schemes, pbkdf2, simple-pbkdf2, migration]
level: advanced
status: docs-checked
description: "CouchDB user password schemes simple, pbkdf2 and simple+pbkdf2, and how to convert old simple hashes without knowing the password."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/intro/security.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Schemes (the `password_scheme` field):

- `simple`: deprecated. One SHA-1 iteration over password plus salt. Too weak unless the password has especially high entropy.
- `pbkdf2`: multiple iterations using a SHA-2 family member; the iteration count is configurable.
- `simple+pbkdf2`: a migration aid. If you have `simple` credentials you cannot delete or authenticate with, convert them without knowing the password: CouchDB applies `simple` first, then PBKDF2 to the result.

Python from the docs to compute the new key (the `password_sha` and `salt` values come from the existing user doc):

```python
import hashlib
doc = fetch_user_doc(username)
hashlib.pbkdf2_hmac('sha256', doc['password_sha'], doc['salt'], 600000).hex()
```

Store the result in `derived_key` and set the other fields:

```json
{"type": "user", "name": "user1", "password_scheme": "simple+pbkdf2",
 "derived_key": "<result>", "pbkdf2_prf": "sha256",
 "iterations": 600000, "salt": "<salt>"}
```

## Checked

2026-11-04. Confirmed against the CouchDB intro/security page (Password Schemes): simple (deprecated, one SHA-1 iteration), pbkdf2, simple+pbkdf2, the Python conversion code and example user document. Nothing removed.

Method: documentation only; no commands were run.
