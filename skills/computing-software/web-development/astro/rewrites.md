---
id: computing-software.web-development.astro.rewrites
name: rewrites
category: computing-software
field: web-development
product: astro
tags: [rewrite, astro-rewrite, context-rewrite, middleware-rewrite]
level: advanced
status: docs-checked
description: "Serve another route's content without changing the URL using Astro.rewrite and context.rewrite, including 404 rewrites and middleware rewrites."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A rewrite serves a different route while the browser keeps the original address. Useful for the same content at multiple paths, or showing localized content for language variants.

```astro title="src/pages/es-cu/articles/introduction.astro"
---
return Astro.rewrite("/es/articles/introduction");
---
```

In endpoints, use `context.rewrite()`:

```js title="src/pages/api.js"
export function GET(context) {
  if (!context.locals.allowed) {
    return context.rewrite("/");
  }
}
```

If the rewrite target errors at runtime, dev shows the overlay and production returns 500. If the URL does not exist, 404 is returned. You can intentionally rewrite to `/404`:

```astro title="src/pages/[item].astro"
---
const { item } = Astro.params;

if (!itemExists(item)) {
  return Astro.rewrite("/404");
}
---
```

Conditional rewrite on response status in middleware:

```js title="src/middleware.mjs"
export const onRequest = async (context, next) => {
  const response = await next();
  if (response.status === 404) {
    return context.rewrite("/");
  }
  return response;
}
```

`Astro.rewrite()` triggers a new, complete rendering phase, re-executing middleware for the new route.

## Checked

2026-11-04. Confirmed against the Astro routing guide: Astro.rewrite, context.rewrite, 404 and 500 behaviour, middleware rewrite, and the new rendering phase. Nothing removed.

Method: documentation only; no commands were run.
