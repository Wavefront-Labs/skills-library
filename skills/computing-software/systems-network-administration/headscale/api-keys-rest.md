---
id: computing-software.systems-network-administration.headscale.api-keys-rest
name: api-keys-rest
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, apikeys, rest, bearer, api-v1]
level: practitioner
status: docs-checked
description: "Create, list and expire Headscale API keys and call the REST API at /api/v1 with a Bearer token, including the register endpoint."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API keys and the REST API

```
headscale apikeys create
headscale apikeys list
headscale apikeys expire --prefix <PREFIX>
```

`create` defaults to 90 days expiry. A key cannot be retrieved after creation; if lost, expire it and make a new one.

## Calling the API

Base URL `https://headscale.example.com/api/v1` (docs at `/api/v1/docs`; version at `/version`).

```shell
curl -H "Authorization: Bearer <API_KEY>" \
    https://headscale.example.com/api/v1/user

curl -H "Authorization: Bearer <API_KEY>" \
    --json '{"user": "<USER>", "authId": "<AUTH_ID>"}' \
    https://headscale.example.com/api/v1/auth/register
```

`/api/v1/user?name=bob` returns one user.

## Gotchas

- The `Authorization` header must use the Bearer scheme.
- A Tailscale-compatible API subset is at `/api/v2`, accepting API keys and OAuth client credentials.
- Copy the key when it is created; it cannot be retrieved again.

## Checked

2026-11-04. Confirmed against the Headscale API reference: apikeys create/list/expire, the 90-day default, no retrieval, /api/v1, /api/v1/docs, /version, Bearer authentication, the user and register examples, and the /api/v2 subset. Removed an unsourced admin-control remark and a third-party client reference.
Method: documentation only; no commands were run.
