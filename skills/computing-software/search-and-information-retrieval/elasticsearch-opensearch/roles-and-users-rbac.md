---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.roles-and-users-rbac
name: roles-and-users-rbac
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, roles-and-users-rbac, es-security-rbac]
level: practitioner
status: docs-checked
description: "Create least-privilege roles with index privileges and assign them to users with the Elasticsearch native realm security APIs."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-has-privileges
  - https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles
  - https://docs.opensearch.org/latest/security/access-control/users-roles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles and users (RBAC)

**Goal:** least privilege access.
```
PUT _security/role/log_reader
{"indices":[{"names":["logs-*"],"privileges":["read","view_index_metadata"]}]}
PUT _security/user/ana {"password":"<password>","roles":["log_reader"]}
```
- Both calls need the `manage_security` cluster privilege. A role has `cluster` (cluster privileges), `indices` (each entry needs `names` and `privileges`; optional `field_security` grant/except and a document-level `query`), and `applications` entries. These are separate lists.
- Native realm users: a password (at least 6 characters) or `password_hash` is required when adding a user, optional when updating; use `roles: []` for none. `refresh` defaults to true.
- Role names must be unique. Roles in a `roles.yml` file win over an API role of the same name, cannot be viewed or changed through the UI or API, and must be copied to every node because the file is local to each node. The role APIs and Kibana UI are the preferred route.
- Wildcard patterns that cover restricted (system) indices need `allow_restricted_indices: true`; by default restricted indices do not match patterns.
- Check access: `GET _security/user/_has_privileges` with a body listing `cluster` and `index` privileges tests the calling user; checking another user needs run-as.
- OpenSearch: users, roles and role mappings can be defined in Dashboards, `internal_users.yml`, `roles.yml`, `roles_mapping.yml` or the REST API; users map to roles through role mappings. Only the page's section headings were checked.
- Failure mode (a judgment, not stated on the pages): a broad `names` pattern such as `logs-*` also matches indices created later.

## Verify
- [ ] The user can read `logs-*` and gets 403 on other indices.

## Checked
Checked 2026-11-08 against the Elasticsearch "Create or update roles", "Create or update users", "Check user privileges" and "Defining roles" pages, plus the OpenSearch "Defining users and roles" page. Removed: the advice to use API keys or service accounts instead of the `elastic` superuser (not on these pages).
Method: documentation only; no commands were run.
