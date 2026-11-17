---
id: computing-software.data-engineering.metabase.api-keys
name: api-keys
category: computing-software
field: data-engineering
product: metabase
tags: [api-keys, x-api-key, key-groups, regenerate, api-key-usage]
level: intro
status: docs-checked
description: "Create and manage Metabase API keys: admin path, group-based permissions, one-time display, X-API-Key header, regeneration, deletion and group-deletion effects."
sources:
  - https://www.metabase.com/docs/latest/people-and-groups/api-keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create: Admin, Settings, Authentication, API Keys, Manage, Create API Key. Enter a name and select a group; the key gets that group's permissions. Self-hosted Pro or Enterprise can also create keys in the config file.

Display: copy the key immediately. Metabase will not show it again, so a lost key must be regenerated.

Use: send the key in the `X-API-Key` header.
`curl -H 'X-API-Key: YOUR_API_KEY' -X GET 'http://localhost:3000/api/permissions/group'`
In JavaScript, keep it in an environment variable such as `METABASE_API_KEY` and pass it to `fetch` in that header.

Edit: the pencil icon changes the name or group. Regenerating replaces the key and the old one cannot be recovered.

Delete: the trash icon, then confirm. Deleted keys cannot be recovered; create a new one.

Gotchas:
- If a group is deleted, its keys keep working but move to All users, which changes their permissions. Reassign them manually.
- The API is unversioned; endpoints rarely change but client code may need updates.
- Usage is tracked under API key usage in Monitor.
- The page lists no endpoint-level restrictions beyond what the group allows.

Pick the narrowest group that works, since a key inherits every permission of its group.

## Checked
2026-11-03. Confirmed against the Metabase docs page People and groups, API keys: admin path, group permissions, one-time display, config-file creation (Pro/Enterprise self-hosted), regenerate and delete, group-deletion reassignment to All users, X-API-Key curl and fetch examples, unversioned API note, API key usage in Monitor. Nothing removed.
Method: documentation only; no commands were run.
