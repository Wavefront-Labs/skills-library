---
id: computing-software.web-development.astro.middleware-rewrite-and-error-pages
name: middleware-rewrite-and-error-pages
category: computing-software
field: web-development
product: astro
tags: [context-rewrite, next-rewrite, middleware-error-pages, login-guard]
level: advanced
status: docs-checked
description: "Rewrite requests in middleware with context.rewrite or next(path), understand re-execution and the request body caveat, and how middleware runs for 404/500 pages."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/middleware.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`context.rewrite()` shows a different page without redirecting, and triggers a new rendering phase in which middleware re-executes.

```js title="src/middleware.js"
import { isLoggedIn } from "~/auth.js"
export function onRequest (context, next) {
  if (!isLoggedIn(context)) {
    return context.rewrite(new Request("/login", {
      headers: {
        "x-redirect-to": context.url.pathname
      }
    }));
  }

  return next();
};
```

Passing a path (string, URL or `Request`) to `next()` rewrites in place without a new rendering phase. In a `sequence()`, the next middleware receives the updated context and nothing re-runs:

```js
async function first(context, next) {
  console.log(context.url.pathname) // this will log "/blog"
  return next("/")
}

async function second(context, next) {
  console.log(context.url.pathname) // this will log  "/"    
  return next()
}

export const onRequest = sequence(first, second);
```

Caveat: `next(path)` creates a new `Request` from the old one, so consuming `Request.body` before or after throws a runtime error. This often occurs with Astro Actions using HTML forms; handle those rewrites from templates with `Astro.rewrite()`.

Error pages: middleware tries to run for all on-demand pages, even unmatched routes and custom 404 pages, but the adapter decides whether it runs. It also tries to run before a 500 page, unless the error happened in the middleware itself; then `Astro.locals` is unavailable on the 500 page.

## Checked

2026-11-04. Confirmed against the Astro middleware guide: context.rewrite re-execution, next(path) in-place rewrite, the Request.body caveat, and 404/500 middleware behaviour. Nothing removed.

Method: documentation only; no commands were run.
