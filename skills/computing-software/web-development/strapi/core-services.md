---
id: computing-software.web-development.strapi.core-services
name: core-services
category: computing-software
field: web-development
product: strapi
tags: [strapi, services, createcoreservice, document-service, reusable]
level: practitioner
status: docs-checked
description: "Create, wrap and replace Strapi services with createCoreService and call them via strapi.service(uid)."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/services.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Services

Services are reusable functions that keep controllers small. Create with `strapi generate` or manually in `./src/api/[api-name]/services/` (plugins: `./src/plugins/[plugin-name]/services/`). Export a factory receiving `strapi`.

```js
const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::restaurant.restaurant', ({ strapi }) =>  ({
  // Method 2: Wrapping a core service (leaves core logic in place)
  async find(...args) {
    const { results, pagination } = await super.find(...args);

    // some custom logic
    results.forEach(result => {
      result.counter = 1;
    });

    return { results, pagination };
  },

  // Method 3: Replacing a core service
  async findOne(documentId, params = {}) {
    return strapi.documents('api::restaurant.restaurant').findOne({
        documentId,
        // Use super to keep core fetch parameter formatting
        ...super.getFetchParams(params),
     });
  }
}));
```

Method 1 is a brand-new method (e.g. `exampleService(...args)`). Call a service from anywhere:

```js
strapi.service('api::restaurant.restaurant').sendNewsletter(...args)
```

Core services inherit methods that wrap the Document Service API (`computing-software.web-development.strapi.document-service-read`):

- Collection types: `find(params)`, `findOne(documentId, params)`, `create(params)`, `update(documentId, params)`, `delete(documentId, params)`, `count(params)`, `publish`, `unpublish`, `discardDraft`.
- Single types: `find(params)`, `createOrUpdate({ data, ...params })`, `delete(params)`, `count`, `publish`, `unpublish`, `discardDraft`.
- When no `status` is passed, core services set `status: 'published'`; pass `status: 'draft'` to query drafts.
- `getFetchParams(params)` converts a controller query object into the parameters these methods expect.
- A core service can be replaced entirely by a custom service with the same method name (for example `find`).
- `yarn strapi services:list` lists the available services; `strapi.service('plugin::pluginName.serviceName')` reaches plugin services.

## Checked

2026-11-04: checked against the Strapi docs page Services (backend-customization/services). Confirmed: generate or manual creation, folder locations, the factory receiving `strapi`, the three methods in the example, calling via `strapi.service(uid)`. Added from the page: the core service method lists, the default published status, getFetchParams, replacement by name, services:list.

Method: documentation only; no commands were run.
