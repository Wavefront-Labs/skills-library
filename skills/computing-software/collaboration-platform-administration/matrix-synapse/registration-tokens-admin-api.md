---
id: computing-software.collaboration-platform-administration.matrix-synapse.registration-tokens-admin-api
name: registration-tokens-admin-api
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, registration-tokens, admin-api, registration-requires-token, invite-only, msc3231]
level: practitioner
status: docs-checked
description: "Issue, list, update and delete Synapse registration tokens through the admin API, with uses_allowed, expiry_time, pending versus completed counters and the valid filter."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_api/registration_tokens.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Registration tokens gate sign-up so only people you give a token to can register (MSC3231, stable in version 1.2 of the Matrix spec). Enable `registration_requires_token` in `homeserver.yaml` and call the API with an admin `access_token`. The API is disabled when Matrix Authentication Service integration is on; use the MAS admin API or CLI then.

A token object has `token`, `uses_allowed`, `pending`, `completed` and `expiry_time` (milliseconds since the Unix epoch, null for none). `pending` goes up when someone starts using the token and drops when they finish, at which point `completed` increases, so concurrent use cannot exceed `uses_allowed`.

Endpoints:

- `GET /_synapse/admin/v1/registration_tokens` lists tokens under `registration_tokens`. `?valid=true` returns only valid ones, `?valid=false` only expired or exhausted ones.
- `GET /_synapse/admin/v1/registration_tokens/<token>` returns one.
- `POST /_synapse/admin/v1/registration_tokens/new` creates one. Body fields: `token` (up to 64 characters from `[A-Za-z0-9._~-]`, random if omitted), `uses_allowed` (default null, unlimited), `expiry_time` (default null), and `length` (1 to 64, default 16, for a generated token).
- `PUT /_synapse/admin/v1/registration_tokens/<token>` changes `uses_allowed` or `expiry_time`; omitted fields are unchanged and null means unlimited or no expiry.
- `DELETE /_synapse/admin/v1/registration_tokens/<token>` removes it and returns `{}`.

Setting `uses_allowed` to `0` is the easy way to invalidate a token without deleting its history. A missing token gives `404` with `M_NOT_FOUND`. For a one-off invite, create with `{"token": "defg", "uses_allowed": 1}`. To compute an expiry in milliseconds the docs suggest `date '+%s000' -d 'tomorrow'`.

## Checked

2026-11-04. Confirmed against the Synapse Registration Tokens page: endpoints, body fields and defaults, token object fields, valid filter, 404 error, MAS note. Nothing removed.
Method: documentation only; no commands were run.
