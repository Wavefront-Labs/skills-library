---
id: computing-software.web-development.strapi.rest-status-parameter
name: rest-status-parameter
category: computing-software
field: web-development
product: strapi
tags: [strapi, rest-api, status, draft, published, draft-and-publish]
level: practitioner
status: docs-checked
description: "Use the status parameter on Strapi REST requests to read or write drafts; default is published, unlike the Document Service."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/status.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST `status`

Requires Draft & Publish enabled. Values:
- `published` (default): published versions
- `draft`: draft versions

```bash
curl 'http://localhost:1337/api/restaurants?status=draft' \
  -H 'Authorization: Bearer <token>'
```

```js
const query = qs.stringify({
    status: 'draft',
}, {
    encodeValuesOnly: true, // prettify URL
});
await request(`/api/restaurants?${query}`);
```

## Traps
- The REST API defaults to `published` for every request, including `POST` and `PUT`: a write publishes immediately unless you pass `status=draft`. The Document Service API defaults to `draft`.
- In a draft response `publishedAt` is `null`, even when a published version exists.
- `status` applies to the whole request, including populated relations. Without it (or with `published`) populated relations return published versions and never-published related documents are left out.
- To select by how draft and published versions relate (never-published, modified...), see the `publicationFilter` REST parameter.
- `status` is accepted only at the root of the query: putting it inside `populate` (for example `populate[categories][status]=draft`) returns a `400` error.
- A `PUT` needs a `data` object: send `"data": {}` to publish a draft unchanged; omitting `data` returns `400`.

## Checked

2026-11-04: checked against the Strapi docs page REST API: status (api/rest/status). Confirmed: Draft & Publish prerequisite, values and default, curl and qs examples, REST default of published on POST and PUT versus draft in the Document Service, `publishedAt` null in drafts, populated-relation rules, `publicationFilter` pointer. Added from the page: root-only `status` and the `data` requirement on PUT.

Method: documentation only; no commands were run.
