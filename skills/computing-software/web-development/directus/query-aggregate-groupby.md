---
id: computing-software.web-development.directus.query-aggregate-groupby
name: query-aggregate-groupby
category: computing-software
field: web-development
product: directus
tags: [query-aggregate, group-by, aggregate-functions, date-functions]
level: practitioner
status: docs-checked
description: "Run Directus aggregate queries (count, sum, avg, min, max and distinct variants) with groupBy, including date functions such as year(field)."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/3.query-parameters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Aggregate functions: `count`, `countDistinct`, `sum`, `sumDistinct`, `avg`, `avgDistinct`, `min`, `max`; `countAll` exists in GraphQL only.

```http
GET /items/posts?aggregate[count]=*
GET /items/posts?aggregate[count]=views,comments&groupBy[]=author&groupBy[]=year(publish_date)
```

`groupBy` runs the aggregate per shared value instead of over the whole dataset; group by several fields at once, including functions for per year/month/day reporting.

SDK:

```js
await directus.request(aggregate("posts", {
  aggregate: { count: ["views", "comments"] },
  groupBy: ["author", "year(publish_date)"],
}));
```

GraphQL: query `posts_aggregated(groupBy: [...]) { group count { views comments } }` or `countAll`.

## Checked

2026-11-04: confirmed against the Directus docs Query Parameters page (Aggregate and GroupBy sections): function table, countAll GraphQL-only, REST, GraphQL and SDK examples. Removed the garbled REST gotcha and the unsupported verify line.

Method: documentation only; no commands were run.
