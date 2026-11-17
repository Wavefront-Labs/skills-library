---
id: computing-software.web-development.strapi.core-controllers
name: core-controllers
category: computing-software
field: web-development
product: strapi
tags: [strapi, controllers, createcorecontroller, ctx, actions, super]
level: practitioner
status: docs-checked
description: "Write and extend Strapi controllers with createCoreController: custom actions, wrapping core actions with super, ctx."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/controllers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controllers

Controllers hold the business logic for routes. Create with `strapi generate` or manually in `./src/api/[api-name]/controllers/` (auto-loaded). Move heavy logic into services.

```js
const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::restaurant.restaurant', ({ strapi }) =>  ({
  // Method 1: Creating an entirely custom action
  async exampleAction(ctx) {
    try {
      ctx.body = 'ok';
    } catch (err) {
      ctx.body = err;
    }
  },

  // Method 2: Wrapping a core action (leaves core logic in place)
  async find(ctx) {
    // some custom logic here
    ctx.query = { ...ctx.query, local: 'en' }

    // Calling the default core action
    const { data, meta } = await super.find(ctx);

    // some more custom logic
    meta.date = Date.now()

    return { data, meta };
  },
}));
```

Every action receives a context object `ctx` (request context and response context). In TypeScript use `factories.createCoreController` from `@strapi/strapi`.

Generated content-types get a controller and router targeting `find`, `findOne`, `create`, `update`, `delete`; overriding those needs no route change. A new action needs a route (see `computing-software.web-development.strapi.custom-route-to-action`). For safe overrides see `computing-software.web-development.strapi.controller-sanitize-override`.

## Checked

Checked 2026-11-04 against the Strapi Controllers page (adding a controller, extending core controllers, `ctx`, core mapping and routes notes). Removed the claim that actions may be sync or async, which the page does not state.

Method: documentation only; no commands were run.
