---
id: computing-software.web-development.bun.serve-error-handling
name: serve-error-handling
category: computing-software
field: web-development
product: bun
tags: [serve-error-handler, development-mode, node-env-production, error-page]
level: intro
status: docs-checked
description: "Handle errors in Bun.serve with an error callback and turn off development mode before deploying so stack traces and source are not sent to clients."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/error-handling.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Bun.serve()` runs in development mode by default. If a handler throws and no `error` handler returns a response, Bun serves a built-in 500 page with the message, stack trace, nearby source and file paths.

```ts
Bun.serve({
  fetch(req) { throw new Error("woops!"); },
  error(error) {
    return new Response(`<pre>${error}\n${error.stack}</pre>`, {
      headers: { "Content-Type": "text/html" },
    });
  },
});
```

Turn development mode off:

```ts
Bun.serve({ development: false, fetch(req) { throw new Error("woops!"); } });
```
or run with `NODE_ENV=production`.

Gotchas:
- The development error page exposes source code and file paths to the requester. Disable it before deploying.
- The `--production` flag does not disable it; that flag belongs to `bun build` and `bun install`, and `bun run` ignores it.
- In production, still write an `error` handler that returns a generic response rather than `error.stack`.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/http/error-handling: development mode by default, turned off by NODE_ENV=production or development: false, built-in 500 page contents, error callback example, the warning about source and file paths, and the --production flag note. Removed the appended Verify line, which the page does not contain.
Method: documentation only; no commands were run.
