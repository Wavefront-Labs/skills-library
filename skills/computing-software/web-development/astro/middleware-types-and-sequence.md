---
id: computing-software.web-development.astro.middleware-types-and-sequence
name: middleware-types-and-sequence
category: computing-software
field: web-development
product: astro
tags: [definemiddleware, sequence, locals-types, env-d-ts]
level: practitioner
status: docs-checked
description: "Type Astro middleware with defineMiddleware or MiddlewareHandler, declare App.Locals in env.d.ts, and chain several middlewares with sequence()."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/middleware.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type safety with `defineMiddleware()`:

```ts
// src/middleware.ts
import { defineMiddleware } from "astro:middleware";

// `context` and `next` are automatically typed
export const onRequest = defineMiddleware((context, next) => {

});
```

With JSDoc, use `MiddlewareHandler`:

```js
/**
 * @type {import("astro").MiddlewareHandler}
 */
export const onRequest = (context, next) => {

};
```

Type `Astro.locals` by declaring a global namespace in `env.d.ts`:

```ts title="src/env.d.ts"
type User = {
  id: number;
  name: string;
};

declare namespace App {
  interface Locals {
    user: User;
    welcomeTitle: () => string;
    orders: Map<string, object>;
  }
}
```

Chain middleware in order with `sequence()`:

```js
import { sequence } from "astro:middleware";

export const onRequest = sequence(validation, auth, greeting);
```

Each function awaits `next()`, so the console order is: validation request, auth request, greeting request, greeting response, auth response, validation response.

## Checked

2026-11-04. Confirmed against the Astro middleware guide: defineMiddleware, MiddlewareHandler, App.Locals in env.d.ts and the sequence() console order. Nothing removed.

Method: documentation only; no commands were run.
