---
id: computing-software.web-development.strapi.api-config-file
name: api-config-file
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-api, strictparams, defaultlimit, maxlimit, privateattributes]
level: practitioner
status: docs-checked
description: "config/api: REST prefix, default and max limits, withCount, privateAttributes and the strictParams options for REST and Document Service."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/api

| Property | Meaning | Default |
|---|---|---|
| `responses.privateAttributes` | attributes treated as private globally | `[]` |
| `rest.prefix` | API prefix | `/api` |
| `rest.defaultLimit` | default `limit`; `-1` removes the limit | `25` |
| `rest.maxLimit` | max requestable `limit` | `100` |
| `rest.withCount` | include totals in `meta.pagination` | `true` |
| `rest.strictParams` | accept only allowed query/body params on Content API routes | - |
| `documents.strictParams` | Document Service rejects unknown root-level keys | - |

If `maxLimit` is below `defaultLimit`, `maxLimit` is used. `defaultLimit: -1` returns every matching entry for requests with no `pagination` and `maxLimit` does not cap it.

Apps scaffolded with `create-strapi-app` set both `strictParams` to `true` in the generated file. Extra allowed parameters are added via the custom Content API parameters mechanism.

```js
module.exports = ({ env }) => ({
  responses: {
    privateAttributes: ['_v', 'id', 'created_at'],
  },
  rest: {
    prefix: '/v1',
    defaultLimit: 100,
    maxLimit: 250,
    strictParams: true, // only allow parameters defined on routes or added via contentAPI.addQueryParams/addInputParams
  },
  documents: {
    strictParams: true, // reject unrecognized root-level parameters in strapi.documents() calls
  },
});
```

## Checked

2026-11-04: checked against the Strapi docs page API calls configuration (configurations/api). Confirmed: every property, default (`[]`, `/api`, `25`, `100`, `true`), the maxLimit/defaultLimit interaction, `-1` behaviour, strictParams scope and the scaffolded `true` values, example config. Filled in the two defaults that said 'see page'.

Method: documentation only; no commands were run.
