---
id: computing-software.cloud-infrastructure-engineering.zot.api-keys
name: api-keys
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, api-keys, apikey-endpoint, key-expiry, cli-credentials]
level: practitioner
status: docs-checked
description: "Enable and manage Zot API keys for CLI and CI use after web or social login: creation, one-time display, use as password, listing and revocation."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/developer-guide/api-user-guide.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API keys suit users who log in by GUI or social login but need command-line credentials, and limit exposure compared with sharing broader credentials such as LDAP.

Enable: set `"apikey": true` under `http.auth`.

Create: log in first with another mechanism (for example the web UI), then `POST /zot/auth/apikey`. Optional fields: `label`, `scopes`, `expirationDate`. By default a key has the same permissions as its creator. The `apiKey` value appears only in the creation output and cannot be retrieved later.

Use: as the password.

```
curl -u user:<apikey> http://localhost:8080/v2/_catalog
echo "<api-key>" | docker login myreg.example.com -u <username> --password-stdin
```

Manage while logged in:
- List: `GET /zot/auth/apikey` (shows label, scopes, expiration, `isExpired`; never the key).
- Revoke your own key: `DELETE /zot/auth/apikey?id=$uuid`.

API keys can match `adminPolicy`, unlike traditional bearer tokens. Zot-issued keys are never forwarded to an upstream token endpoint.

## Checked

2026-11-04. Read against the zot API user guide (API keys section) and Docker article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
