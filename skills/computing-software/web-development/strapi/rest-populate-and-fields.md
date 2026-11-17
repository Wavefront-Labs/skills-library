---
id: computing-software.web-development.strapi.rest-populate-and-fields
name: rest-populate-and-fields
category: computing-software
field: web-development
product: strapi
tags: [strapi, rest-api, populate, fields, relations, components, dynamic-zones]
level: practitioner
status: docs-checked
description: "Select fields and populate relations, media, components and dynamic zones in Strapi REST requests, with syntax table."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/populate-select.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Field selection and populate

By default the REST API returns only top-level scalar fields (string, date, number, boolean, JSON types) and populates nothing.

## fields
- One: `fields=name`
- Several: `fields[0]=name&fields[1]=description`

Field selection does not work on relation, media, component or dynamic zone fields.

```js
const query = qs.stringify(
  {
    fields: ['name', 'description'],
  },
  {
    encodeValuesOnly: true, // prettify URL
  }
);
await request(`/api/restaurants?${query}`);
```

## populate
| Use case | Syntax |
|---|---|
| Everything, 1 level | `populate=*` |
| One relation | `populate=a-relation-name` |
| Several relations | `populate[0]=relation-name&populate[1]=another-relation-name` |
| Nested levels | `populate[root-relation-name][populate][0]=nested-relation-name` |
| A component | `populate[0]=component-name` |
| Component and nested component | `populate[0]=component-name&populate[1]=component-name.nested-component-name` |

- `find` permission must be enabled for the populated content-type, otherwise it is not populated.
- Deep-populate plugins (`populate=deep`) are not recommended by Strapi.
- Populated relations always return full objects, not arrays of IDs.
- A dynamic zone: `populate[0]=dynamic-zone-name` returns only its first-level scalar fields; use `populate[dynamic-zone-name][on][component-category.component-name][populate][relation-name][populate][0]=field-name` for component-specific fields, nested components and relations.
- `fields`, `filters` and `sort` can be nested inside a populated relation (for example `populate[categories][filters][name][$eq]=Cars`); `status` is accepted only at the root of the query and returns `400` inside `populate`.
- Top-level `pagination` works alongside `populate`, but nested pagination on populated relations is not supported.
- For join-table relations, an explicit `sort` inside `populate` overrides the default connect order.
- In production the page advises explicit population over `populate=*`, limited to 2-3 levels deep.
- Long `populate[n]` lists are bounded by the query parser `arrayLimit` (default `100`); raise it on the `strapi::query` middleware.

## Checked

2026-11-04: checked against the Strapi docs page REST API: Population & Field Selection (api/rest/populate-select). Confirmed: nothing populated by default, default returned field types, fields syntax, fields unsupported on relations/media/components/dynamic zones, the populate syntax table, `find` permission prerequisite, deep-populate warning, `arrayLimit` default 100 on `strapi::query`. Added from the page: full objects, dynamic zone syntax, nested options, pagination limits, sort override and the production tip.

Method: documentation only; no commands were run.
