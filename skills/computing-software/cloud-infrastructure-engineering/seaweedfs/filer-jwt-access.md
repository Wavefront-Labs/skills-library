---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-jwt-access
name: filer-jwt-access
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [bearer, security-toml, authorization, jwt, filer-auth]
level: practitioner
status: docs-checked
description: "Authenticate filer HTTP requests with JWT: the filer only validates tokens signed with the security.toml key, via Bearer header, jwt query param or AT cookie."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-JWT-Use
  - https://github.com/seaweedfs/seaweedfs/wiki/Security-Overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer jwt access

The filer does not issue JWTs. Another service must sign them with the key set as `jwt.filer_signing.key` in `security.toml` (environment form: `WEED_JWT_FILER_SIGNING_KEY`), with a timeout in seconds that matches the one set in `security.toml`. Copy the same `security.toml` to the filers and all S3 proxies. `jwt.filer_signing.key` protects upload, update and delete requests; the optional `jwt.filer_signing.read.key` (`WEED_JWT_FILER_SIGNING_READ_KEY`) protects GET and HEAD.

A token can be presented three ways:
1. `Authorization: Bearer <token>` header
2. Query parameter: `http://localhost:8888/buckets/all?jwt=<token>`
3. HTTP-only cookie named `AT`

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8888/path/to/file
```

Verify: a request without a token (or signed with the wrong key) is rejected, the correctly signed one succeeds.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Filer JWT Use (read in full) and Security Overview (JWT sections). Claims about read-mode support and expose_directory_metadata were removed (the read-mode claim contradicted the source).
