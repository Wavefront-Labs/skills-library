---
id: computing-software.database-administration.elasticsearch.run-as-and-has-privileges
name: run-as-and-has-privileges
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, run-as, has-privileges, elasticsearch-security, impersonation, authorization]
level: practitioner
status: verified
description: "Let a trusted service act on behalf of users with Elasticsearch run-as (es-security-runas-user header), and check permissions with the _has_privileges API."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/run-as-privilege.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-has-privileges.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run-as impersonation and _has_privileges

**Goal:** an application authenticates as itself but executes searches with the end user's document- and field-level security, and the UI can ask "may this user do X?" before showing a button.

## Grant run-as
```json
POST _security/role/app_proxy
{ "run_as": ["analyst_*", "support_*"],
  "cluster": [], "indices": [] }
```
Assign `app_proxy` to the service user. The impersonated users must exist in a realm that supports run-as lookup (native confirmed here; for other realms check the run-as documentation).

## Use it
```bash
curl -u app_svc:secret -H "es-security-runas-user: analyst_jane" \
  "https://es:9200/sales-*/_search?q=region:emea"
```
Authorization (index privileges, DLS/FLS) is evaluated as `analyst_jane`. If the run-as user lacks privileges, the request fails with 403 naming both: `unauthorized for user [app_svc] run as [analyst_jane] with effective roles [logs_reader]`.

## Check privileges
```json
GET _security/user/_has_privileges
{ "cluster": ["monitor"],
  "index": [ { "names": ["sales-*"], "privileges": ["read", "write"] } ],
  "application": [ { "application": "kibana-.kibana", "privileges": ["feature_discover.all"], "resources": ["*"] } ] }
```
Response has `has_all_requested` and a per-index/per-privilege map. Sent with the run-as header it answers for the impersonated user (`username: analyst_jane`).

## Gotchas
- Run-as is powerful: restrict the user pattern and protect the service credentials; prefer API keys with `role_descriptors` when the app only needs a fixed scope.
- The service user itself has no data access: the same search without the header returned 403.

## Verify
`GET _security/_authenticate` with the run-as header shows `username: analyst_jane` and `authentication_realm` plus `lookup_realm`.
