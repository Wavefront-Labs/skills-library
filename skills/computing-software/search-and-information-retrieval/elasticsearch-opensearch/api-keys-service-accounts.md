---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.api-keys-service-accounts
name: api-keys-service-accounts
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, api-keys-service-accounts]
level: practitioner
status: docs-checked
description: "Create Elasticsearch API keys with role descriptors and expiration, list and invalidate them; prefer scoped keys for applications."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-invalidate-api-key
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-api-key
  - https://www.elastic.co/docs/deploy-manage/api-keys/elasticsearch-api-keys
  - https://www.elastic.co/docs/reference/elasticsearch/security-privileges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API keys with restricted privileges

**Goal:** scoped, revocable credentials. These are Elasticsearch APIs; the pages cited are Elasticsearch only.
- `POST _security/api_key {"name":"ingest","expiration":"30d","role_descriptors":{"w":{"indices":[{"names":["logs-*"],"privileges":["create_doc"]}]}}}`.
- The response contains `id`, `api_key` and `encoded` (base64 of `id:api_key`); send `Authorization: ApiKey <encoded>`.
- Revoke: `DELETE _security/api_key {"ids":["<id>"]}`; list: `GET _security/api_key`. Invalidated keys fail authentication but stay visible for the retention period.
- With `role_descriptors`, the key's permissions are the intersection of the descriptors and the creating user's permissions, so a key cannot exceed its creator. If omitted, the key gets a snapshot of the creator's permissions.
- `create_doc` allows only document creation: indexing requests must use `op_type` `create`.
- Failure mode: keys never expire by default; set `expiration` and rotate.
- Creating needs the `manage_own_api_key` cluster privilege (or `manage_api_key`).

## Verify
- [ ] A request with the key can create documents in `logs-*` and is refused for other indices.

## Checked
Date: 2026-11-07
- Elasticsearch create API key page: read the description, authorization, request body (`expiration`, `name`, `role_descriptors`, intersection note) and response `encoded` field; the remaining schema and language samples were searched, not read. Examples show `Authorization: ApiKey`.
- Elasticsearch invalidate API keys page, read through the request body: `DELETE /_security/api_key`, `ids`, retention wording, required privileges.
- Elasticsearch get API key page: searched, confirmed `GET /_security/api_key`.
- Elasticsearch API keys overview page, read in full: privileges for creating and deleting keys.
- Elasticsearch security privileges page: searched, confirmed `create_doc` and its `op_type` requirement.
- Removed: nothing factual; the skill is marked Elasticsearch-only because none of the cited pages describe an OpenSearch equivalent.
Method: documentation only; no commands were run.
