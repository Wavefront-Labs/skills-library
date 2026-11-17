---
id: computing-software.web-development.strapi.error-responses-and-ctx
name: error-responses-and-ctx
category: computing-software
field: web-development
product: strapi
tags: [strapi, error-handling, ctx-badrequest, rest-errors, graphql-errors, http-errors]
level: practitioner
status: docs-checked
description: "Strapi's REST and GraphQL error shapes, and throwing HTTP errors from controllers and middlewares with ctx.badRequest."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Error responses and throwing from controllers

## REST error shape
```json
{
  "data": null,
  "error": {
    "status": "", // HTTP status
    "name": "", // Strapi error name ('ApplicationError' or 'ValidationError')
    "message": "", // A human readable error message
    "details": {
      // error info specific to the error type
    }
  }
}
```

GraphQL returns an `errors` array whose items have `message` and `extensions` (`error.name`, `error.message`, `error.details`, and a GraphQL `code` such as `BAD_USER_INPUT`), with `data` null for the query.

## Throwing in controllers and middlewares
The recommended way: call an error function on `ctx` (names from the `http-errors` constructor list). Args: message, then details object (becomes `error.details`).

```js
module.exports = {
  renameDog: async (ctx, next) => {
    const newName = ctx.request.body.name;
    if (!newName) {
      return ctx.badRequest('name is missing', { foo: 'bar' })
    }
    ctx.body = strapi.service('api::dog.dog').rename(newName);
  }
}
```

Same call works in a middleware before `await next()`. For deeper layers see `computing-software.web-development.strapi.error-classes-in-services`.

## Checked

Checked 2026-11-04 against the Strapi Error handling page (receiving errors, throwing in controllers and middlewares, `http-errors` function names in lower camel case). Nothing removed.

Method: documentation only; no commands were run.
