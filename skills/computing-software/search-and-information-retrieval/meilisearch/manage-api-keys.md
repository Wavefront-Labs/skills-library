---
id: computing-software.search-and-information-retrieval.meilisearch.manage-api-keys
name: manage-api-keys
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [api-keys, key-actions, key-rotation, meilisearch]
level: practitioner
status: docs-checked
description: "Create, scope, update, rotate and delete Meilisearch API keys via /keys, choosing actions and indexes, setting expiresAt, and least-privilege practice."
sources: ["https://www.meilisearch.com/docs/capabilities/security/how_to/manage_api_keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manage API keys

Default keys: an admin key (full access, server side only), a search key (client side), and custom keys. Manage them at `/keys` with the admin key.

## Create

`POST /keys` with `description`, `actions`, `indexes` and `expiresAt`, for example `{"description": "Search-only key for products index", "actions": ["search"], "indexes": ["products"], "expiresAt": "2026-12-31T00:00:00Z"}`. `indexes: ["*"]` means all; `expiresAt: null` never expires. Avoid `actions: ["*"]`.

Actions include `search`, `documents.add`, `documents.get`, `documents.delete`, `indexes.create/get/update/delete/swap`, `tasks.get/cancel/delete`, `settings.get/update`, `stats.get`, `dumps.create`, `snapshots.create`, `version`, and `keys.get/create/update/delete`.

## Immutable fields

`actions`, `indexes` and `expiresAt` cannot change after creation; you can only PATCH `name` and `description` at `/keys/<uid>` (use the key uid, not the key). Need different permissions, make a new key.

Custom keys are deterministic: the key is a SHA256 of the uid and the master key, so a new instance with the same master key and same uids reproduces identical keys.

## Rotation and practice

Rotate by creating a replacement with the same actions and indexes, switching the application, verifying, then deleting the old key (deletion rejects requests immediately). Expired keys give 403. Prefer expirations such as 90 days, narrow actions and indexes, and never expose admin keys.

## Checked

2026-11-03. Confirmed claim by claim against the Manage API keys page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
