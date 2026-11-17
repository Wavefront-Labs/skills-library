---
id: computing-software.web-development.astro.middleware-basics-and-locals
name: middleware-basics-and-locals
category: computing-software
field: web-development
product: astro
tags: [middleware, onrequest, locals, next-function]
level: practitioner
status: docs-checked
description: "Write Astro middleware with onRequest in src/middleware, share request data through context.locals, and rewrite the response body."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/middleware.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create `src/middleware.js|ts` (or `src/middleware/index.js|ts`) and export an `onRequest(context, next)` function; it must not be a default export. Return a `Response` or the result of `next()`. Middleware runs at build time for prerendered pages and at request time for on-demand pages.

```js title="src/middleware.js"
export function onRequest (context, next) {
    // intercept data from a request
    // optionally, modify the properties in `locals`
    context.locals.title = "New title";
    context.locals.property = "information";

    // return a Response or the result of calling `next()`
    return next();
};
```

Read it in any `.astro` file with `Astro.locals`:

```astro
---
const data = Astro.locals;
---
<h1>{data.title}</h1>
```

`locals` can hold any type (strings, functions, Maps). It lives and dies within a single route render, so persist anything else elsewhere. `locals` itself cannot be overridden at run time; Astro throws. Integrations may also set `locals` properties, so avoid overriding theirs.

Modify the rendered output:

```js
export const onRequest = async (context, next) => {
    const response = await next();
    const html = await response.text();
    const redactedHtml = html.replaceAll("PRIVATE INFO", "REDACTED");
    
    return new Response(redactedHtml, {
        status: 200,
        headers: response.headers
    });
};
```

## Checked

2026-11-04. Confirmed against the Astro middleware guide: file locations, named onRequest export, locals behaviour and lifetime, build-time versus request-time rendering, and the response rewriting example. Nothing removed.

Method: documentation only; no commands were run.
