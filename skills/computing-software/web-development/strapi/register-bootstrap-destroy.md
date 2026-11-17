---
id: computing-software.web-development.strapi.register-bootstrap-destroy
name: register-bootstrap-destroy
category: computing-software
field: web-development
product: strapi
tags: [strapi, register, bootstrap, destroy, src-index, lifecycle-functions]
level: practitioner
status: docs-checked
description: "Global register, bootstrap and destroy functions in src/index: what each can access and when it runs."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# register, bootstrap, destroy

In `./src/index.js` (or `.ts`). Each can be sync, async or return a promise; Strapi waits for it. Return values are ignored; throw or reject to signal failure.

- `register()`: very first step at startup, before any setup. No access to the database, routes, policies or other back-end elements. Use for: extending plugins, extending content-types programmatically, loading env variables, registering a custom field, registering a custom Users & Permissions provider, front-loading security tasks.
- `bootstrap()`: called at every server start, before the server starts but after the app is set up, so the whole `strapi` object is available. Use for creating an admin user, seeding necessary data, declaring RBAC conditions.
- `destroy()`: asynchronous teardown that runs before the application shuts down.

```js
module.exports = {
  register({ strapi }) {
    strapi.customFields.register({
      name: 'color',
      plugin: 'my-color-picker',
      type: 'string',
    });
  },
};
```

Async bootstrap example from the page:

```js
async bootstrap({ strapi }) {
  const articles = await strapi
    .documents('api::article.article')
    .findMany({
      status: 'published',
      fields: ['documentId'],
    });
  strapi.log.info(`Indexed ${articles.length} published articles`);
},
```

Since bootstrap runs at every server start, the page's seeding example first looks the record up (`findMany` with a `slug` filter) and creates it only if none exists.

`destroy()` is for graceful cleanup: stopping running services and cleaning up plugin actions (closing connections, removing listeners, clearing intervals).

## Checked

2026-11-04: checked against the Strapi docs page Lifecycle functions (configurations/functions). Confirmed: file location, sync/async/promise modes, ignored return values and throw or reject for failure, register timing and limits and use cases, bootstrap timing and use cases, the custom field and async bootstrap examples. Replaced: the unstated 'make seeding idempotent' advice with what the page example does. Added: destroy use cases.

Method: documentation only; no commands were run.
