---
id: computing-software.devops-ci-cd.verdaccio.storage-and-secret
name: storage-and-secret
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [storage, verdaccio-db, secret, storage-path, token-secret, migrate-legacy-signature]
level: advanced
status: docs-checked
description: "Where Verdaccio stores packages and the .verdaccio-db file, and why the 32-character token secret matters on 6.x versus 7.x, including migrateToSecureLegacySignature."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/env/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`storage: ./storage` is the local filesystem path. `VERDACCIO_STORAGE_PATH` overrides it (default storage only, not plugins). With the default storage, `.verdaccio-db` (JSON) sits in the storage folder and holds the published-package `list` and the token `secret`.

```json
{ "list": ["package1", "@scope/pkg2"], "secret": "secret_token_32_characters_long" }
```
The secret must be exactly 32 characters. Older installs may have a 64-character one.
- 7.x: startup fails with `Invalid storage secret key length, must be 32 characters long but is N`.
- 6.x: with `security.api.migrateToSecureLegacySignature` true (the default) a wrong-length secret is silently replaced and every old token stops working. Set it to `false` to fail loudly instead.

Fix manually by editing the secret to 32 characters, or on 6.x:
```yaml
security:
  api:
    migrateToSecureLegacySignature: true
```
Replacing the secret invalidates all previously issued tokens. The property was removed in 7.x.

`VERDACCIO_STORAGE_NAME` renames the local-storage database file.

## Checked

2026-11-04. Confirmed against the Verdaccio Configuration page (storage and .verdaccio-db, 32 versus 64 character secret, 7.x startup error, 6.x migrateToSecureLegacySignature behaviour, VERDACCIO_STORAGE_PATH scope) and Environment Variables page. Removed: the store-overrides-storage claim.
Method: documentation only; no commands were run.
