---
id: computing-software.search-and-information-retrieval.typesense.create-api-keys
name: create-api-keys
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [api-keys, search-only-key, key-expiry, typesense]
level: practitioner
status: docs-checked
description: "Create Typesense API keys with POST /keys scoped by actions and collections, set expires_at and autodelete; the key is shown only at creation."
sources: ["https://typesense.org/docs/30.2/api/api-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create API keys

Typesense keys can be restricted per collection, per action, per record or per field. Use the bootstrap key (`--api-key`) only to create other keys; do not use it in production applications.

## Request

`POST /keys` with:

| Field | Notes |
|---|---|
| `actions` (required) | allowed actions, `resource:verb` such as `documents:search`; `*` for all |
| `collections` (required) | collection names; regex supported, e.g. `org_.*`. Applies to collection endpoints only, not global ones like `synonym_sets`, `keys` or `stopwords` |
| `description` (required) | what the key is for |
| `value` | choose your own key string; otherwise random |
| `expires_at` | Unix timestamp until which the key is valid |
| `autodelete` | purge expired keys, runs hourly, default `false` |

Admin-style key: `{"description": "Admin key.", "actions": ["*"], "collections": ["*"]}`; avoid such wide scope. Search-only: `{"description": "Search-only companies key.", "actions": ["documents:search"], "collections": ["companies"]}`.

## Cautions

The generated key value is returned only at creation; store it securely. A search key scoped to one collection can also expose fields of collections that collection references, when read through a joined query, although the referenced collection cannot be searched directly.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page API Keys (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
