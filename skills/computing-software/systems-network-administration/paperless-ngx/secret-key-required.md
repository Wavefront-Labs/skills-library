---
id: computing-software.systems-network-administration.paperless-ngx.secret-key-required
name: secret-key-required
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, secret-key, paperless-secret-key, security, sessions, upgrade]
level: practitioner
status: docs-checked
description: "PAPERLESS_SECRET_KEY has no default and must be set, or Paperless refuses to start; how to generate it and what rotating it invalidates."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PAPERLESS_SECRET_KEY

Paperless uses this value to make session tokens and sign sensitive data. It is required, has no default, and Paperless will refuse to start if it is not set. It is a critical security setting for cryptographic signing and should be a long, random value.

## Generate one
Use any sequence of characters (the more, the better); you do not need to remember it. A suitable key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```
Set it as `PAPERLESS_SECRET_KEY=<SECRET_VALUE>`. For Docker, the setup guide says configuration values can be supplied from a Docker secret by appending `_FILE` to the name (its example is `PAPERLESS_DBUSER_FILE`), and `paperless.conf` is not used on Docker. On bare metal, the settings go in `paperless.conf`.

## Upgrading to v3
If your installation relied on the previous built-in default key, you have two options:
- Set `PAPERLESS_SECRET_KEY` to that previous value to preserve existing sessions and tokens.
- Set it to a new random value to improve security, understanding that this will invalidate existing sessions and other signed tokens.

## Keep it random
The setup guide says it should be a random sequence of characters used for authentication, and that failing to do so allows third parties to forge authentication credentials.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the PAPERLESS_SECRET_KEY entry in configuration, the Secret Key section of migration-v3, the bare metal configuration step in setup, the Docker Compose step 3 note on `_FILE` secrets, and the opening lines of configuration listing which `paperless.conf` paths are used.
Corrections: removed "Do not commit it to version control", "anyone holding it can forge signed data" and "rotate it deliberately; do not change it casually" (none stated; the pages say a non-random key allows forged credentials and rotating invalidates sessions); removed `docker-compose.env` as a storage location (not stated for this key) and tied `_FILE` and `paperless.conf` to the pages that mention them; added the setup page as a source.
Method: documentation only; no commands were run.
