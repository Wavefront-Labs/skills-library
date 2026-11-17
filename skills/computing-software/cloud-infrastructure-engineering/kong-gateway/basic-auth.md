---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.basic-auth
name: basic-auth
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, basic-auth, hide-credentials, realm, authentication, plugins]
level: intro
status: docs-checked
description: "basic-auth plugin: hide_credentials, anonymous and realm (default service) config, header lookup order, base64 credentials, and brute-force protection."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/basic-auth/schema.lua
  - https://developer.konghq.com/plugins/basic-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic-auth

Config:

| Field | Default |
|---|---|
| `hide_credentials` | `false`; when `true` strips the `Authorization` header before proxying |
| `anonymous` | none; Consumer ID or username (not custom ID) used when auth fails |
| `realm` | `service`; value of the `realm` attribute in `WWW-Authenticate` on failure |

Behaviour:
- Needs at least one Consumer with a username and password credential.
- Credentials are base64 in the header: `Ariel:Password` becomes `QXJpZWw6UGFzc3dvcmQ=`.
- Kong checks `Proxy-Authorization` first, then `Authorization`.
- Enable on a Service, a Route, or globally.
- Without `anonymous`, failed authentication returns a 4xx.

`brute_force_protection` (v3.13+) tracks failed logins by username and returns `429 Too Many Requests`; each further failure doubles the wait (2^n seconds), capped by a configurable maximum of 1 hour. Its strategy can be Redis, PostgreSQL or in-memory.

Delete a credential: `DELETE /consumers/{consumer_id_or_name}/basic-auth/{credentials_id}`.

Updating a Consumer's username or tag overwrites the stored password with its encrypted value; re-enter the original password when updating.

## Checked

2026-11-04. Confirmed against the basic-auth schema.lua (anonymous, hide_credentials default false, realm default service) and the plugin page (header order, base64 example, 429 brute-force protection since 3.13 with 2^n second waits capped at 1 hour, DELETE credential path, password overwrite FAQ, Redis/PostgreSQL/in-memory backends). The page gives both 3rd and 4th failed attempt as the first 429, so no attempt count is stated here.

Method: documentation only; no commands were run.
