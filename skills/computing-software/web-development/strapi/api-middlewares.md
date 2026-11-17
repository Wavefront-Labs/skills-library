---
id: computing-software.web-development.strapi.api-middlewares
name: api-middlewares
category: computing-software
field: web-development
product: strapi
tags: [strapi, middlewares, koa, routes, global-middleware, naming]
level: practitioner
status: docs-checked
description: "Write Strapi middlewares for the REST API, where to put them, how to name them, and how to attach them to routes."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Middlewares

Locations:
- `./src/middlewares/` application level
- `./src/api/[api-name]/middlewares/` API level
- `./src/plugins/[plugin-name]/middlewares/` plugin

Shape:

```js
module.exports = (config, { strapi })=> {
  return (context, next) => {};
};
```

Example timing middleware:

```js
module.exports = () => {
  return async (ctx, next) => {
    const start = Date.now();
    await next();
    const delta = Math.ceil(Date.now() - start);
    ctx.set('X-Response-Time', delta + 'ms');
  };
};
```

Globally scoped custom middlewares must be added to `config/middlewares` or Strapi won't load them. API and plugin middlewares attach to a route:

```js
config: {
  middlewares: ["[middleware-name]"],
},
```

## Names
- `global::middleware-name`
- `api::api-name.middleware-name`
- `plugin::plugin-name.middleware-name`

`yarn strapi middlewares:list` shows registered ones. The GraphQL plugin has its own middleware syntax.

New application-level or API-level middlewares can be created with the interactive `strapi generate` command or by hand in the folders above. In TypeScript use `export default (config, { strapi }) => ...`.

The docs recommend a middleware as the replacement for the old "is-owner policy" (only the entry's author may edit or delete). Generate one named `isOwner` with `strapi generate` (choose `middleware`, then `Add middleware to an existing API`). Its body reads `ctx.state.user`, loads the entry with `strapi.documents('<api::x.x>').findOne({ documentId, populate: "*" })`, and returns `ctx.unauthorized(...)` unless `user.id` equals `entry.author.id`, otherwise `return next()`. Attach it per action in the router, for example:

```js
createCoreRouter("api::restaurant.restaurant", {
  config: {
    update: { middlewares: ["api::restaurant.is-owner"] },
    delete: { middlewares: ["api::restaurant.is-owner"] },
  },
});
```

The docs describe this as the most basic implementation; real logic depends on your project. Route-level middlewares are also suggested as a place to centralize population logic.

## Checked
Confirmed 2026-11-08 against the Strapi middlewares customization page (read in full): locations, signature, timer example, routing, naming and the `middlewares:list` tip. Added the `strapi generate` route, TypeScript form and the is-owner walkthrough. The timer example in the docs is titled `/config/middlewares.js`. The docs' is-owner example names the file `isOwner.js` but references `api::restaurant.is-owner` in the route; check the registered name with `middlewares:list`.
Method: docs-only read of cited pages, 2026-11-08
