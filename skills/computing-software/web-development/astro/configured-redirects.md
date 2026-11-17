---
id: computing-software.web-development.astro.configured-redirects
name: configured-redirects
category: computing-software
field: web-development
product: astro
tags: [redirects, redirects-config, status-code, external-redirect]
level: practitioner
status: docs-checked
description: "Declare permanent redirects in astro.config with the redirects option: dynamic routes, external URLs, status objects, and precedence against real pages."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Map old routes to new in the `redirects` config. Internal targets are a route path; external URLs starting with `http` or `https` that can be parsed are also supported.

```js title="astro.config.mjs"
import { defineConfig } from "astro/config";

export default defineConfig({
  redirects: {
    "/old-page": "/new-page",
    "/blog": "https://example.com/blog"
  }
});
```

Redirects follow the same priority rules as file-based routes and always take lower precedence than an existing page file: `/old-page` will not redirect if `src/pages/old-page.astro` exists.

Dynamic routes are allowed if the old and new routes contain the same parameters:

```js
{
  "/blog/[...slug]": "/articles/[...slug]"
}
```

With SSR or a static adapter, set the `status` by giving an object value:

```js
redirects: {
  "/old-page": {
    status: 302,
    destination: "/new-page"
  },
}
```

On `astro build`, Astro outputs HTML files with a meta refresh tag by default; supported adapters write the host's configuration file instead. The default status is `301`; when building to HTML files the status code is not used by the server.

## Checked

2026-11-04. Confirmed against the Astro routing guide: redirects config, external URLs, same-parameter dynamic routes, status objects, meta refresh output and default 301. Nothing removed.

Method: documentation only; no commands were run.
