---
id: computing-software.web-development.strapi.core-router-config
name: core-router-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, routes, createcorerouter, only, except, prefix, auth]
level: practitioner
status: docs-checked
description: "Configure generated Strapi routes with createCoreRouter: prefix, only, except, and per-route auth, policies, middlewares."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Core routers

Core routes (`find`, `findOne`, `create`, `update`, `delete`) are generated per content-type. Router files go in `./src/api/[apiName]/routes`. `createCoreRouter` takes:

| Parameter | Meaning |
|---|---|
| `prefix` | custom prefix for all routes of this model (e.g. `/test`) |
| `only` | the only core routes loaded; anything else is ignored |
| `except` | core routes not loaded (opposite of `only`) |
| `config` | policies, middlewares and public availability per route |

```js
const { createCoreRouter } = require('@strapi/strapi').factories;

module.exports = createCoreRouter('api::restaurant.restaurant', {
  only: ['find'],
  config: {
    find: {
      auth: false,
      policies: [],
      middlewares: [],
    }
  }
});
```

This allows only a `GET` on `/restaurants` through the core `find` controller, without authentication (`auth: false`).

`except` lists core routes that should not be loaded. For custom routes see `computing-software.web-development.strapi.custom-route-to-action`. If you only customize the default controller actions, leave the router as is.

## Checked

Checked 2026-11-04 against the Strapi Routes page (core routers, `createCoreRouter` parameters, the `only: ['find']` example, and the note on customizing default actions). Removed the advice to use `only`/`except` to replace routes with custom routers, which the page does not state.

Method: documentation only; no commands were run.
