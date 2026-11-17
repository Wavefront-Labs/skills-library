---
id: computing-software.systems-network-administration.icinga-2.api-filters-and-querying-objects
name: api-filters-and-querying-objects
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, rest-api, filters, filter-vars, method-override, joins, attrs]
level: practitioner
status: docs-checked
description: "Query Icinga 2 objects over /v1/objects with name filters, filter expressions, filter_vars, attrs, joins and X-HTTP-Method-Override."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API filters and querying objects
**Query:** `GET /v1/objects/<plural type>`, for example `/v1/objects/hosts`. One object by path: `/v1/objects/services/example.localdomain!http` (composite names use the full name, see `__name`).

**Parameters:** `attrs` limits attributes, `joins` joins related types (`?joins=host` or `?joins=host.name`), `meta` adds `used_by` or `location`. `pretty` and `verbose` are global; `verbose` needs `diagnostic-information`.

**Simple filters:** the URL parameter is the lower-case type name: `?host=localhost`; several objects use the plural: `?hosts=a&hosts=b`.

**Advanced filters:** `filter` takes an apply-rule style expression, evaluated in a sandbox. The object is a variable named after the lower-case type (`host`, `service`) and also `obj`. Examples:
- `service.state!=ServiceOK`
- `match("example.localdomain*",host.name)`
- `"linux-servers" in host.groups`

The caller needs the `filter-expression` permission, granted only to trusted users because evaluation runs in the main worker process and can be abused for denial of service. Only one `filter` parameter is allowed. For actions on both hosts and services, add `"type"`.

**filter_vars:** avoids escaping, like bound parameters: `"filter": "group in host.groups", "filter_vars": { "group": "linux-servers" }`. Request body only.

**Method override:** GET cannot carry a body, so send `POST` with `X-HTTP-Method-Override: GET` and put filters in the body (documented best practice). The same works for `DELETE`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/. No commands were run.
