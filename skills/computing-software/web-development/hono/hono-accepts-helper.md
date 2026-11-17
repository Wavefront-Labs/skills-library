---
id: computing-software.web-development.hono.hono-accepts-helper
name: hono-accepts-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, content-negotiation, accept-header]
level: intro
status: docs-checked
description: "Pick a supported value from Accept-Language or Accept-Encoding headers in Hono using the accepts helper and its header, supports, default and match options."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/accepts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accepts helper

Import: `import { accepts } from 'hono/accepts'`.

`accepts()` reads an Accept-style request header and returns the best value you support.

```ts
app.get('/', (c) => {
  const accept = accepts(c, {
    header: 'Accept-Language',
    supports: ['en', 'ja', 'zh'],
    default: 'en',
  })
  return c.json({ lang: accept })
})
```

## Options
- `header` (required): an `AcceptHeader`, one of `'Accept' | 'Accept-Charset' | 'Accept-Encoding' | 'Accept-Language' | 'Accept-Patch' | 'Accept-Post' | 'Accept-Ranges'`.
- `supports` (required): `string[]` of values your app supports.
- `default` (required): `string` returned when nothing matches.
- `match` (optional): custom `(accepts: Accept[], config: acceptsConfig) => string` for your own matching logic.

## Gotcha
`header`, `supports` and `default` are all required. `header` must be one of the `AcceptHeader` values listed above, and `match` lets you supply a custom `(accepts, config) => string` function in place of the built-in matching. The helper looks at the Accept header (such as Accept-Encoding or Accept-Language) and returns the proper value.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/accepts.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
