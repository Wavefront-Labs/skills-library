---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.admin-api-access
name: admin-api-access
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, admin-api, x-api-key, pagination, patch, allow-admin, admin-listen]
level: practitioner
status: docs-checked
description: "Use the APISIX Admin API: base URL and port 9180, X-API-KEY auth, allow_admin, resource list, page and page_size, filters, PUT/POST/PATCH/DELETE semantics and force delete."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/admin-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin API access

- Base URL: `http://127.0.0.1:9180/apisix/admin`; the port comes from `deployment.admin.admin_listen`.
- Auth: header `X-API-KEY` set to `deployment.admin.admin_key.key` from `config.yaml`. Access is also limited by the `deployment.admin.allow_admin` IP allowlist.
- Resources: Route, Stream Route, Service, Consumer, Credential, Upstream, SSL, Global Rule, Consumer Group, Plugin Config, Plugin Metadata, Plugin.

List queries:
- `page` (default 1, minimum 1) and `page_size` (10 to 500).
- `name` and `label` filters; filters are intersected.
- `uri` on Routes only.
- `filter=escape_uri(key=value)` on Routes and Stream Routes, by `service_id` or `upstream_id` (3.13.0+), for example `filter=service_id%3D1`.
- `ttl` on a Route PUT expires it after N seconds.

Methods:
- GET (list or by ID), PUT (with ID), POST (auto ID), DELETE, PATCH.
- PATCH on a whole resource merges fields; a field set to `null` is removed; arrays are replaced entirely. A subpath PATCH (`/{path}`) replaces one attribute.
- DELETE refuses to remove a resource still in use unless `force=true` is passed.

## Checked

2026-11-04. Confirmed against the APISIX Admin API page: port 9180 and the /apisix/admin prefix, X-API-KEY and allow_admin, page and page_size range, name, label and uri filters, the 3.13.0 reference filter, ttl, PATCH null and array semantics, force delete. Nothing removed.

Method: documentation only; no commands were run.
