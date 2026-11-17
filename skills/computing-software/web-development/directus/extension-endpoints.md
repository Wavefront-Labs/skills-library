---
id: computing-software.web-development.directus.extension-endpoints
name: extension-endpoints
category: computing-software
field: web-development
product: directus
tags: [extension-endpoints, custom-routes, express-router, endpoint-error-next]
level: advanced
status: docs-checked
description: "Add custom API routes to Directus with an endpoint extension: Express router, custom root id, context, sandboxed handlers and next(error)."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/09.extensions/2.api-extensions/2.endpoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The entrypoint exports a register function receiving an Express `router` and a `context` (`services`, `database`, `getSchema`, `env`, `logger`, `emitter`). Routes are sub-routes of `/<extension-name>`.

```js
export default (router, context) => {
  router.get('/', (req, res) => res.send('Hello, World!'));
};
```

To set your own root route, export an object:

```js
export default {
  id: 'greet',
  handler: (router, context) => {
    router.get('/', (req, res) => res.send('Hello, World!'));
    router.get('/intro', (req, res) => res.send('Nice to meet you.'));
  },
};
```

These serve `/greet` and `/greet/intro`.

Sandboxed endpoints receive only `router`; handlers take a `request` (`url`, `headers`, `body`) and return `{ status, body }`. Type the router with `SandboxEndpointRouter` from `directus:api`.

Error handling: call `next(error)`, e.g. `next(new ForbiddenError())`, so the error middleware responds consistently instead of the request hanging or the server crashing.

## Checked

2026-11-04: confirmed against the Directus docs API Endpoints page: register function and context properties, config object with id, sandbox router and request/response shape, SandboxEndpointRouter from directus:api, next(error). Removed the unsupported curl verify line.

Method: documentation only; no commands were run.
