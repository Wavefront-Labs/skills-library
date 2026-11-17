---
id: computing-software.web-development.strapi.global-middleware-config
name: global-middleware-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-middlewares, loading-order, cors, security, resolve]
level: practitioner
status: docs-checked
description: "Order and configure global middlewares in config/middlewares: strapi:: built-ins, global:: custom, name and resolve forms."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/middlewares

`./config/middlewares.js` exports an array. Only middlewares listed there are applied, and array order is execution order. If unsure where to place one, add it at the end.

```js
module.exports = [
  // The array is pre-populated with internal, built-in middlewares, prefixed by `strapi::`
  'strapi::logger',
  'strapi::errors',
  'strapi::security',
  'strapi::cors',
  // custom middleware that does not require any configuration
  'global::my-custom-node-module',
  // custom name to find a package or a path
  {
    name: 'my-custom-node-module',
    config: {
      foo: 'bar',
    },
  },
  // custom resolve to find a package or a path
  {
    resolve: '../some-dir/custom-middleware',
    config: {
      foo: 'bar',
    },
  },
```

## Naming
| Type | Name |
|---|---|
| Internal | `strapi::middleware-name` |
| Application-level (`./src/middlewares`) | `global::middleware-name` |
| API-level | `api::api-name.middleware-name` |
| Plugin | `plugin::plugin-name.middleware-name` |

Optional keys: `config` (object, defines or overrides middleware config) and `resolve` (path to the middleware folder, useful for external ones).

Built-in internals include `body` (added by default, required), `compression` (not added by default, not required) and `cors` (added by default, required); the page has a reference per middleware.

## Checked

Checked 2026-11-04 against the Strapi Middlewares configuration page (loading order, naming conventions, optional configuration, internal middlewares table). Corrected the one-line summary of `compression` and `cors`.

Method: documentation only; no commands were run.
