---
id: computing-software.ai-ml-engineering.litellm.litellm-spend-tracking-key-user-team
name: litellm-spend-tracking-key-user-team
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, spend-tracking, key-info, team-info]
level: practitioner
status: docs-checked
description: "Read spend per key, user, team or end user from /key/info, /user/info, /team/info and /end_user/info."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spend is tracked automatically (in USD) when calls go to /completions, /chat/completions or /embeddings, using litellm's `completion_cost()` function.

Where it is stored: the key row in LiteLLM_VerificationTokenTable; if the key has a user_id or team_id, user spend goes to LiteLLM_UserTable and team spend to LiteLLM_TeamTable.

Endpoints:

- key: `/key/info`
- user: `/user/info`
- team: `/team/info`
- end users: `/end_user/info`

```
curl 'http://0.0.0.0:4000/key/info?key=<user-key>' \
     -X GET \
     -H 'Authorization: Bearer <your-master-key>'
```

The response has `info.spend` (a USD amount), `expires`, `models` and `aliases`.

Spend per user:

```
curl --location 'http://localhost:4000/user/new' \
--header 'Authorization: Bearer <your-master-key>' \
--header 'Content-Type: application/json' \
--data-raw '{user_email: "krrish@berri.ai"}'
```

The response includes a unique `user_id`. Create a key with `"user_id": "my-unique-id"` in /key/generate, then read `GET /user/info?user_id=my-unique-id`.

Spend per team: POST /team/new with `team_alias`, create keys with `team_id`, then `GET /team/info?team_id=...`.

Use teams, not users, if keys should be owned by several people such as a production app.

The cost per model is calculated by the `completion_cost` function.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (spend section, read from downloaded copy); removed unconfirmed price-map claim
