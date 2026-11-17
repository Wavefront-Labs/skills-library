---
id: computing-software.search-and-information-retrieval.qdrant.security-api-key
name: security-api-key
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [security, api-key, read-only-api-key, authentication, sec-apikey]
level: practitioner
status: docs-checked
description: "Secure a self-hosted Qdrant with an API key, read-only key and rotation, since open source is not secure by default."
sources:
  - "https://qdrant.tech/documentation/security/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Self-hosted Qdrant is not secure by default: with no key, anyone who can reach port 6333 can read and change data.

Set an API key in the configuration or environment:

```bash
QDRANT__SERVICE__API_KEY=<secret>
QDRANT__SERVICE__READ_ONLY_API_KEY=<read-only-secret>
```

Clients send it in the `api-key` header:

```bash
curl -H 'api-key: <secret>' http://localhost:6333/collections
```

Features from the docs:

- `read_only_api_key` grants read access only.
- `alt_api_key` rotates an admin key without downtime in a distributed deployment: give each peer the new key as `alt_api_key` with a rolling restart, then promote it to `api_key` and remove `alt_api_key`. JWTs signed with the old key must be re-created.
- Bind `service.host` to 127.0.0.1 for local development, and to a private interface in production.
- Connections are unencrypted by default, so enable TLS, otherwise the key is sent in plain text.

For per-user permissions, use the JWT role-based access described separately.

## Checked

2026-11-03. Confirmed on the Qdrant security page: not secure by default, `QDRANT__SERVICE__API_KEY` and `READ_ONLY_API_KEY`, `read_only_api_key` maps to read-only, `alt_api_key` rotation procedure, binding to 127.0.0.1, TLS off by default. The `api-key` header is the page's documented header. Removed generic secrets advice and the rotation-schedule paragraph.

Method: documentation only; no commands were run.
