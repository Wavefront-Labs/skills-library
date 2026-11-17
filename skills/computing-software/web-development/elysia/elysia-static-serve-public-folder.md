---
id: computing-software.web-development.elysia.elysia-static-serve-public-folder
name: elysia-static-serve-public-folder
category: computing-software
field: web-development
product: elysia
tags: [static, files, plugin, assets]
level: practitioner
status: docs-checked
description: "Serve a folder of static files from Elysia with @elysia/static, tune prefix, ignore patterns, headers and SPA index.html fallback."
sources:
  - https://elysiajs.com/plugins/static.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose files from a directory as routes.

1. Install: `bun add @elysia/static`
2. Use it:

```typescript
import { Elysia } from 'elysia'
import { staticPlugin } from '@elysia/static'

new Elysia().use(staticPlugin()).listen(3000)
```

By default the folder is `public` registered under the `/public` prefix. With `public/takodachi.png` and `public/nested/takodachi.png` you get `/public/takodachi.png` and `/public/nested/takodachi.png`.

Config (defaults):
- `assets` (`"public"`): folder to expose.
- `prefix` (`"/public"`): URL prefix.
- `ignorePatterns` (`[]`): files not to serve.
- `staticLimit` (`1024`): paths are registered on the Router by static name up to this count; beyond it they are added lazily to save memory at some performance cost.
- `alwaysStatic` (`false`): true registers every path on the Router, skipping `staticLimit`.
- `headers` (`{}`): response headers for files.
- `indexHTML` (`false`): true serves `index.html` from the static directory for any request that matches neither a route nor an existing static file (single-page-app fallback).

Serving one file only: skip the plugin and return a file helper.

```typescript
import { Elysia, file } from 'elysia'
new Elysia().get('/file', file('public/takodachi.png'))
```

Gotchas:
- The default `prefix` is `/public`; the page does not show serving from the site root.
- Static plugin and `file()` need filesystem access, so they do not work on Cloudflare Workers (see the Cloudflare skill for the assets binding alternative).

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/static.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the unsupported site-root advice.

Method: documentation only; no commands were run.
