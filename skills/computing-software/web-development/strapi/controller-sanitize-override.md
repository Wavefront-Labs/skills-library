---
id: computing-software.web-development.strapi.controller-sanitize-override
name: controller-sanitize-override
category: computing-software
field: web-development
product: strapi
tags: [strapi, controllers, sanitizequery, validatequery, sanitizeoutput, security]
level: advanced
status: docs-checked
description: "Replace a core Strapi controller action safely: validateQuery, sanitizeQuery, service call, sanitizeOutput, transformResponse."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/controllers.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/document-service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replacing a core action with sanitization

When overriding core actions, always validate and sanitize queries and responses to avoid leaking private fields or bypassing access rules. Use `validateQuery` (optional), `sanitizeQuery` (recommended even if validating) and `sanitizeOutput` before returning data.

```js
async find(ctx) {
  // validateQuery (optional)
  // to throw an error on query params that are invalid or the user does not have access to
  await this.validateQuery(ctx);

  // sanitizeQuery to remove any query params that are invalid or the user does not have access to
  // It is strongly recommended to use sanitizeQuery even if validateQuery is used
  const sanitizedQueryParams = await this.sanitizeQuery(ctx);
  const { results, pagination } = await strapi.service('api::restaurant.restaurant').find(sanitizedQueryParams);
  const sanitizedResults = await this.sanitizeOutput(results, ctx);

  return this.transformResponse(sanitizedResults, { pagination });
}
```

Why: the Document Service is a data-access layer unaware of user permissions or field visibility; results may include private fields, passwords and restricted relations. Built-in REST and GraphQL sanitize for you; custom controllers or plugin routes calling it directly must do so themselves.

Validation asserts the data is already clean and throws; sanitization cleans and returns it.

## Checked

Checked 2026-11-04 against the Strapi Controllers page (safe `find` override, sanitization and validation definitions) and the Document Service API page (unsanitized-data caution). Nothing removed.

Method: documentation only; no commands were run.
