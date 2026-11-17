---
id: computing-software.web-development.strapi.error-classes-in-services
name: error-classes-in-services
category: computing-software
field: web-development
product: strapi
tags: [strapi, error-handling, applicationerror, utils, services, lifecycles]
level: advanced
status: docs-checked
description: "Throw Strapi error classes from @strapi/utils in services and lifecycle hooks so the admin panel shows proper messages."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Error classes in deeper layers

Below controllers and middlewares, throw the error classes from the `@strapi/utils` package. They extend Node's `Error`. In model lifecycles use `ApplicationError` so proper messages appear in the admin panel. Not limited to services.

Imports:

```js
const { errors } = require('@strapi/utils');
const { ApplicationError } = errors;
```

Then `throw new ApplicationError('message', details)` inside the service method or lifecycle function.

## Rules
- The REST and GraphQL error shapes on the page describe `name` as `'ApplicationError'` or `'ValidationError'`.
- In lifecycles, generally throw only in `beforeX` hooks, not `afterX`.
- Controllers/middlewares: prefer `ctx.badRequest(...)` instead (`computing-software.web-development.strapi.error-responses-and-ctx`).
- The default error class list is in the page's "default error classes" section.

## Checked

Checked 2026-11-04 against the Strapi Error handling page (services and models lifecycles, default error classes, error shape). Reworded the error-name rule to match the page's wording.

Method: documentation only; no commands were run.
