---
id: computing-software.database-administration.elasticsearch.roles-users-and-api-keys
name: roles-users-and-api-keys
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, elasticsearch-roles, elasticsearch-api-keys, native-realm, role-mapping, cluster-privileges, index-privileges, least-privilege]
level: practitioner
status: verified
description: "Grant least-privilege access in Elasticsearch with custom roles, native users, API keys (scoped, expiring) and role mappings for SSO/LDAP realms."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/defining-roles.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles, users and API keys

**Goal:** every app and person gets just the cluster and index privileges they need; nothing uses `elastic` day to day.

## Role
```json
PUT _security/role/logs_writer
{
  "cluster": ["monitor", "manage_index_templates"],
  "indices": [
    { "names": ["logs-app-*"], "privileges": ["create_doc", "auto_configure", "view_index_metadata"] }
  ]
}
PUT _security/role/logs_reader
{ "indices": [ { "names": ["logs-*"], "privileges": ["read", "view_index_metadata"] } ] }
```
Useful privileges: cluster `monitor`, `manage_ilm`, `manage_pipeline`; index `read`, `create_doc` (append only, no updates), `write`, `create_index`, `manage`, `delete_index`. Avoid `all` and the `superuser` role.

## Native user
```json
POST _security/user/ana
{ "password": "...", "roles": ["logs_reader", "kibana_admin"], "full_name": "Ana" }
```
Or `bin/elasticsearch-users useradd` (file realm, per node: break-glass only).

## API keys (preferred for services)
```json
POST _security/api_key
{
  "name": "shipper-prod-eu", "expiration": "90d",
  "role_descriptors": { "ship": { "indices": [ { "names": ["logs-app-*"], "privileges": ["create_doc", "auto_configure"] } ] } },
  "metadata": { "owner": "platform", "ticket": "OPS-1234" }
}
```
Returns `id`, `api_key`, `expiration` and `encoded` (base64 id:key) for `Authorization: ApiKey <encoded>`. The key's effective privileges are the intersection of its descriptors and the creating user's privileges at creation time (snapshot).
Manage: `GET _security/api_key?name=shipper-*`, `DELETE _security/api_key { "ids": [...] }` (invalidate), `POST _security/_query/api_key` for inventory. Rotate by creating a new key before invalidating the old one.

## Role mappings for external realms
```json
PUT _security/role_mapping/sso_sre
{ "roles": ["logs_reader", "monitoring_user"], "enabled": true,
  "rules": { "all": [ { "field": { "realm.name": "saml1" } }, { "field": { "groups": "sre" } } ] } }
```

## Check
```json
GET _security/_authenticate
POST _security/user/_has_privileges { "index": [ { "names": ["logs-app-1"], "privileges": ["delete"] } ] }
```

## Gotchas
- Reserved roles such as `superuser` cannot be modified (400 "is reserved and may not be used"); rotate built-in user passwords with `elasticsearch-reset-password`.
- Data streams need `auto_configure` / `create_doc` on the stream name, not on backing indices.
- Creating an API key needs a cluster privilege such as `manage_own_api_key`; a user with only index privileges got an error.

## Verify
With the shipper key, indexing to `logs-app-x` succeeds and `DELETE logs-app-x` returns 403 `security_exception`.
