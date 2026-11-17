---
id: computing-software.systems-network-administration.netbox.graphql-configuration-limits
name: graphql-configuration-limits
category: computing-software
field: systems-network-administration
product: netbox
tags: [graphql-enabled, graphql-max-query-depth, graphql-max-aliases]
level: practitioner
status: docs-checked
description: "Configure GraphQL enablement, alias and query depth limits."
sources: ["https://netboxlabs.com/docs/netbox/configuration/graphql-api/", "https://netboxlabs.com/docs/netbox/integrations/graphql-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GraphQL configuration

Goal: control the GraphQL endpoint served at `/graphql/`.

**Parameters**

- `GRAPHQL_ENABLED` (default True, dynamic): set False to disable the API.
- `GRAPHQL_MAX_ALIASES` (default 10): maximum number of queries one request may contain.
- `GRAPHQL_MAX_QUERY_DEPTH` (default None, no limit): requests exceeding the depth are rejected when set to a positive integer; `None` or `0` disables enforcement.
- `GRAPHQL_DEFAULT_VERSION`: the version served by `/graphql/`. To reach a specific version, append it to the URL, for example `/graphql/v2/`.


**Query shape.** Every object type has a singular field taking an ID, such as `device(id:123)`, and a plural `$OBJECT_list` field, such as `device_list`, with optional filters:
```
query { site_list(filters: {status: {exact: STATUS_ACTIVE}}) { name } }
```
Filters can be combined with `OR` and `NOT` and applied to related objects, for example `interfaces(filters: {enabled: {exact: true}})` under `device_list`. Requests go to `/graphql/` with an `Authorization: Bearer $TOKEN` header. The API is powered by Strawberry Django. Fields that return several types, such as cable terminations, use inline fragments and expose `class_type`.

**Checklist**

1. Disable if unused.
2. Set a depth limit for exposed instances.
3. Pin clients to a versioned URL.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: GraphQL configuration page: GRAPHQL_ENABLED, GRAPHQL_MAX_ALIASES default 10, GRAPHQL_MAX_QUERY_DEPTH, versioned URL; GraphQL API page for list/singular query shape and filters. Removed: Nothing.

Method: documentation only; no commands were run.
