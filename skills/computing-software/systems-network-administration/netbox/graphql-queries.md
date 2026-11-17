---
id: computing-software.systems-network-administration.netbox.graphql-queries
name: graphql-queries
category: computing-software
field: systems-network-administration
product: netbox
tags: [graphql, graphql-filters, strawberry-django]
level: practitioner
status: docs-checked
description: "Send read-only queries to /graphql/ with list and single-object fields and filters."
sources: ["https://netboxlabs.com/docs/netbox/integrations/graphql-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GraphQL queries

Goal: fetch exactly the nested fields you need.

NetBox offers a read-only GraphQL API, powered by Strawberry Django, to complement REST. All queries go to the `/graphql/` root endpoint.

```
curl -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  http://netbox/graphql/ \
  --data '{"query": "query {circuit_list(filters:{status: {exact: STATUS_ACTIVE}}) {cid provider {name}}}"}'
```

Pipe the result through `jq` for readability.

**Two fields per type**

- `$OBJECT`: one object; pass the unique ID, such as `device(id:123)`.
- `$OBJECT_list`: a list, optionally filtered, such as `device_list`.

**Filters** are key-value pairs inside parentheses after the query name:

```
query {
  site_list(filters: {status: {exact: STATUS_ACTIVE}}) { name }
}
```

Filters combine with logical operators such as `OR` and `NOT`. For lookup syntax see the Strawberry Django documentation.

The GraphQL configuration page documents server-side limits for the endpoint.

**Checklist**

1. Pass a Bearer token.
2. Use `_list` for collections.
3. Use enum values such as `STATUS_ACTIVE`.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: GraphQL API page: read-only API on /graphql/, Strawberry Django, singular and _list fields, filters with OR/NOT, Bearer token example. Removed: Nothing.

Method: documentation only; no commands were run.
