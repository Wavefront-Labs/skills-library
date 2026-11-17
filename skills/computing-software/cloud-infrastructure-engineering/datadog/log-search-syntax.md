---
id: computing-software.cloud-infrastructure-engineering.datadog.log-search-syntax
name: log-search-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, log-search, facets, log-query, log-explorer]
level: practitioner
status: docs-checked
description: "Search Datadog logs with free text, reserved and @attributes, tags, wildcards, ranges and Boolean operators in Log Explorer."
sources: ["https://docs.datadoghq.com/logs/explorer/search_syntax/", "https://docs.datadoghq.com/logs/explorer/facets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log search syntax and facets
Goal: find the logs you need quickly.

```
authentication AND -password
"hello world"
service:checkout status:error env:prod
-service:healthcheck
@http.status_code:[400 TO 499]
@http.response_time:>100
@http.url_details.path:"/api/v1/test"
env:(prod OR test)
(env:prod AND -version:beta)
-@http.status_code:*
@my_attribute:hello\:world
```

- Boolean operators are case sensitive: `AND` (the default between terms), `OR`, and `-` for exclusion.
- A quoted sequence such as `"hello world"` matches those words; use straight double quotes, not curly ones.
- Free text (no `@`, no `key:`) searches only the `message`, `@title`, `@error.message` and `@error.stack` attributes, not every attribute. To search another attribute, name it with `@`.
- Reserved attributes (`host`, `source`, `status`, `service`, `trace_id`, `message`) and tags are searched without `@`. Custom attributes take the `@` prefix and their path uses dots (`@http.url_details.path`).
- You do not have to define a facet to search on attributes and tags. To search a numerical attribute with `<`, `>`, `<=`, `>=` first add it as a facet (measure).
- Attribute searches are case sensitive; free-text search is case insensitive. A value with special characters needs escaping (`hello\:world`) or double quotes; `?` matches a single special character or space.
- Wildcards: `*` multi-character; they work in free text on the message and on tags and attributes (with the attribute prefix, for example `@my_attribute:value*`). Inside double quotes wildcards are not interpreted. Plain single-word searches are fastest; combine wildcard and quoted searches with a selective filter such as `service` or `host`.
- `CIDR(@network.client.ip,13.0.0.0/8)` filters on an IP range.
- Saved Views keep the query, columns, time horizon and facet.

Gotcha: searching a bare word such as `error` does not look at `status`; use `status:error`.

## Verify
- The same query in a saved view returns the same count as a dashboard widget using that query.

## Checked
2026-11-03. Confirmed against the Log Search Syntax page. Fixed: the draft said bare words match "any attribute" and that custom attributes must be facets for search; the page says free text covers only message and error fields and facets are not required for search (they are required for numeric comparison). Removed `@duration:>1000000000`, `host:web-*` and patterns/Live Tail statements as unconfirmed.
Method: documentation only; no commands were run.
