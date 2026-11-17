---
id: computing-software.web-development.strapi.custom-route-to-action
name: custom-route-to-action
category: computing-software
field: web-development
product: strapi
tags: [strapi, routes, custom-router, handler, controller-action, endpoint]
level: practitioner
status: docs-checked
description: "Expose a new controller action through a custom Strapi route with a fully-qualified handler string."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/controllers.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding a custom endpoint

Add a route only for new actions or paths. Handler format: `<scope>::<api-or-plugin-name>.<controllerName>.<actionName>`.

Controller action:

```js
const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::restaurant.restaurant', ({ strapi }) => ({
  async exampleAction(ctx) {
    const specials = await strapi.service('api::restaurant.restaurant').find({ filters: { isSpecial: true } });
    return this.transformResponse(specials.results);
  },
}));
```

Route file `./src/api/restaurant/routes/01-custom-restaurant.js`:

```js
module.exports = {
  routes: [
    {
      method: 'GET',
      path: '/restaurants/specials',
      handler: 'api::restaurant.restaurant.exampleAction',
    },
  ],
};
```

Use `yarn strapi routes:list` to see existing routes and their hierarchical order.

Route object fields: `method` (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`), `path` (leading slash), `handler`, optional `config`.

## Checked

Checked 2026-11-04 against the Strapi Routes page (route object fields, `routes:list`) and the Controllers page (core mapping notes, handler syntax, `01-custom-restaurant.js` example). Nothing removed.

Method: documentation only; no commands were run.
