---
id: computing-software.search-and-information-retrieval.typesense.retrieve-list-delete-api-keys
name: retrieve-list-delete-api-keys
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [list-keys, key-prefix, delete-key, typesense]
level: intro
status: docs-checked
description: "Inspect and revoke Typesense API keys with GET /keys, GET /keys/:id and DELETE /keys/:id; only a key prefix is returned after creation."
sources: ["https://typesense.org/docs/30.2/api/api-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retrieve, list and delete keys

- `GET /keys/:id` returns metadata for one key.
- `GET /keys/` returns metadata for all keys.
- `DELETE /keys/:id` deletes a key given its ID.

For security only the create endpoint returns the complete key; later reads return only the key prefix. Keep the secret when you create it.

Deleting a parent search key also invalidates every scoped key generated from it, which makes deletion the revocation mechanism for a tenant or organization.

Access to these calls is governed by the actions `keys:list`, `keys:get` and `keys:delete`.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page API Keys (names, defaults, parameters and behaviours as stated in the skill). Removed: the exact response field names and JSON shapes, the delete response body and the required header, which the page does not show in readable form.

Method: documentation only; no commands were run.
