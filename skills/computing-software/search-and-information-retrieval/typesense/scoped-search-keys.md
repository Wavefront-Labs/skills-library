---
id: computing-software.search-and-information-retrieval.typesense.scoped-search-keys
name: scoped-search-keys
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [scoped-search-key, multi-tenancy, embedded-filter, typesense]
level: advanced
status: docs-checked
description: "Generate Typesense scoped search keys from a search-only parent key with embedded filter_by and expires_at for multi-tenant and role-based access."
sources: ["https://typesense.org/docs/30.2/api/api-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoped search keys

A scoped key embeds search parameters that Typesense applies automatically and users cannot override. Uses: multi-tenancy in one collection via an embedded `filter_by`, and locking parameters like `exclude_fields` or `limit_hits`.

## Multi-tenant example

Add an array field `accessible_to_user_ids` to each document. For user 1, generate on your backend a key with `filter_by: accessible_to_user_ids:=1`; add `exclude_fields: accessible_to_user_ids` to hide the list. Curated or `pinned_hits` documents are not filtered by default; also embed `filter_curated_hits: true` to filter them.

## Role-based access

Store `accessible_to_organization_id` and an array `accessible_to_roles` per document. Create a parent search key per organization, then generate scoped keys with `filter_by: accessible_to_organization_id:=1 && accessible_to_roles:=[sales,marketing]`. Revoking the parent key invalidates all scoped keys derived from it.

## Generating

No server call is needed. The parent must be a search-only key (`documents:search` and nothing else). Create an HMAC digest of the parameters with that key and use the result as the API key; the client libraries do this for you.

`expires_at` of a scoped key must be earlier than its parent's expiry. Never expose the parent key client-side.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page API Keys (names, defaults, parameters and behaviours as stated in the skill). Removed: the generateScopedSearchKey example and the byte-level HMAC-SHA256/base64 recipe, which the page does not spell out.

Method: documentation only; no commands were run.
