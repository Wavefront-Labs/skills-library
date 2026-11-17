---
id: computing-software.search-and-information-retrieval.meilisearch.tenant-token-payload
name: tenant-token-payload
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [tenant-tokens, search-rules, multi-tenancy, meilisearch]
level: advanced
status: docs-checked
description: "Build Meilisearch tenant token JWT payloads: searchRules with per-index filters and wildcards, apiKeyUid, and exp expiry, plus revocation caveats."
sources: ["https://www.meilisearch.com/docs/capabilities/security/advanced/tenant_token_payload"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tenant token payload

A tenant token is a JWT with three payload elements: `searchRules`, `apiKeyUid` and optionally `exp`. Example: `{"exp": 1646756934, "apiKeyUid": "<KEY_UID>", "searchRules": {"INDEX_NAME": {"filter": "attribute = value"}}}`.

## searchRules

An object whose keys are indexes: a name, a prefix wildcard (`medical*`), or `*` for all. Each value is an object with at most a `filter` (a normal filter expression) or `{}` for all documents. A token only reaches indexes listed. Specific entries override `*`. Examples: `{"medical_records": {"filter": "user_id = 1 AND published = true"}}`; or `{"*": {"filter": "user_id = 1"}, "medical_records": {"filter": "user_id = 1 AND published = true"}}`.

## apiKeyUid

Required, the uid of an API key that has the `search` action. The token gets the same indexes and routes as that key. If the key expires or is deleted, the token becomes invalid. Always generate tokens on the back end.

## exp

A UNIX timestamp or `null`, never later than the parent key's expiry. Strongly recommended, because the only way to revoke a token without expiry is to delete its parent API key.

Tip from the docs: inspect tokens with jwt.io while developing.

## Checked

2026-11-03. Confirmed claim by claim against the Tenant token payload page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: an unsupported claim that invalid filters fail at search time.

Method: documentation only; no commands were run.
