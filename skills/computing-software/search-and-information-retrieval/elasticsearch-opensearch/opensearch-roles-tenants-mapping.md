---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.opensearch-roles-tenants-mapping
name: opensearch-roles-tenants-mapping
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, opensearch-roles-tenants-mapping]
level: practitioner
status: docs-checked
description: "Define OpenSearch Security roles with cluster, index, DLS/FLS and tenant permissions, map users and backend roles, and restrict access to the Security API."
sources:
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/access-control/users-roles.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/access-control/api.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/access-control/document-level-security.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/access-control/field-level-security.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/multi-tenancy/tenant-index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_security/multi-tenancy/multi-tenancy-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles, role mappings and tenants

**Goal:** least privilege in OpenSearch with the Security plugin.

## Roles
- A role bundles cluster permissions, index permissions (including DLS and FLS) and tenant permissions.
- Create with the REST API, for example `PUT _plugins/_security/api/roles/logs_read {"cluster_permissions":["cluster_composite_ops_ro"],"index_permissions":[{"index_patterns":["logs-*"],"allowed_actions":["read"]}]}`.
- `cluster_composite_ops_ro` is the cluster permission the docs give for read-only access to cluster-wide resources such as dashboards. A Dashboards user who only views visualizations also needs read on the underlying index.
- The `.yml` files (`roles.yml`, `roles_mapping.yml`, `internal_users.yml`) are for initial setup; the docs recommend Dashboards or the REST API for ongoing changes, except for reserved or hidden resources.
- Resources flagged `reserved: true` cannot be changed through the API or Dashboards; `hidden: true` ones are not returned and are also reserved.

## Mapping
- Map users or backend roles: `PUT _plugins/_security/api/rolesmapping/logs_read {"users":["ana"],"backend_roles":["analyst"]}`. In `roles_mapping.yml` the fields are `users`, `backend_roles`, `hosts` and `and_backend_roles`.
- Built-in roles worth knowing: `all_access` (superuser; keep unmapped for normal users), `readall`, `readall_and_monitor`, `kibana_user` (sign in to Dashboards; combine with data read), `kibana_server` (the Dashboards server user only).

## DLS and FLS
- DLS: `"dls"` holds a DSL query as an escaped JSON string, for example `"{\"term\": { \"public\": true}}"`. Variables such as `${user.name}` can be substituted. It restricts reads only; a role with write permission can still modify documents DLS hides. Maximum size is 1024 KB. Keep queries simple (performance cost). Map user-id style fields as `keyword`, because analyzed `text` fields can match unintended values.
- FLS: in `fls` you either include fields (users see only those) or exclude them. Also reads only.

## Tenants
- Tenants hold Dashboards saved objects (index patterns, visualizations, dashboards). Every Dashboards user gets the global and private tenants by default; administrators can add custom tenants.
- Grant tenant access in the role: `"tenant_permissions":[{"tenant_patterns":["human_resources"],"allowed_actions":["kibana_all_read"]}]`. `kibana_all_write` lets the role view and modify, `kibana_all_read` view only.
- Settings: `multitenancy_enabled` and `private_tenant_enabled` (both default true) in `config/opensearch-security/config.yml`; `opensearch.requestHeadersAllowlist` must include `securitytenant` or Dashboards starts red.

## Who may call the Security API
- `plugins.security.restapi.roles_enabled` (static, restart needed) lists roles that can call the Security APIs, except the allow list, distinguished name and certificate APIs. Fine-grained `restapi:admin/*` permissions need `plugins.security.restapi.admin.enabled: true`, and roles containing them must be defined in `roles.yml`, not through the role API.

## Verify
- [ ] The mapped user can read `logs-*` and gets 403 on other indices.
- [ ] A user with only `kibana_all_read` cannot save objects in the tenant.

## Checked
2026-11-08. Confirmed from the OpenSearch documentation source pages on users and roles, API permissions, document-level and field-level security, and multi-tenancy (overview and configuration): role fields, `cluster_composite_ops_ro`, `read` action group, mapping fields, built-in role purposes, DLS escaping, read-only scope and 1024 KB limit, include/exclude FLS, tenant defaults and permission names, restapi settings. Removed: "mapping to `*` backend roles over-grants" (not stated in any page read) and generic notes.
Method: documentation only; no commands were run.
