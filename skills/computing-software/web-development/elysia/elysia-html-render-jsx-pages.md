---
id: computing-software.web-development.elysia.elysia-html-render-jsx-pages
name: elysia-html-render-jsx-pages
category: computing-software
field: web-development
product: elysia
tags: [html, jsx, xss, plugin, kitajs]
level: practitioner
status: docs-checked
description: "Return HTML and JSX templates from Elysia with @elysia/html, configure tsconfig for JSX, and escape user input with the safe attribute."
sources:
  - https://elysiajs.com/plugins/html.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve server-rendered HTML with correct headers from an Elysia route.

1. Install: `bun add @elysia/html`
2. Use the plugin; strings and JSX are both accepted:

```tsx
import { Elysia } from 'elysia'
import { html, Html } from '@elysia/html'

new Elysia()
    .use(html())
    .get('/jsx', () => (
        <html lang="en"><head><title>Hello World</title></head>
        <body><h1>Hello World</h1></body></html>
    ))
    .listen(3000)
```

The plugin adds `Content-Type: text/html; charset=utf8`, adds `<!doctype html>` to a response starting with `<html>` and wraps it into a Response.

3. JSX is powered by @kitajs/html and compiled to strings. Name files `.tsx`/`.jsx` and add to tsconfig.json:

```jsonc
{ "compilerOptions": {
    "jsx": "react",
    "jsxFactory": "Html.createElement",
    "jsxFragmentFactory": "Html.Fragment" } }
```

If you see `Cannot find name 'Html'. Did you mean 'html'?`, import `Html` (capital H) from `@elysia/html` in that file.

4. Escape untrusted values with the `safe` attribute: `<h1 safe>{body}</h1>` (with `body: t.String()` in the route schema).

5. For compile-time XSS reminders on larger apps: `bun add @kitajs/ts-html-plugin` and add `"plugins": [{ "name": "@kitajs/ts-html-plugin" }]` under `compilerOptions`.

Options:
- `contentType` (default `'text/html; charset=utf8'`)
- `autoDetect` (default `true`): auto-detect HTML strings and set the content type
- `autoDoctype` (default `true`; `'full'` also adds doctypes to responses from routes not using the plugin)
- `isHtml` (default exported `isHtml`): a string counts as HTML if longer than 7 characters, starts with `<` and ends with `>`; the docs say it is a best guess only.

Gotcha: values are NOT escaped unless you add `safe`; treat every interpolated user value as hostile.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/html.html); each claim, option name and default was compared with the page text. Removed the invented Verify step; corrected the doctype wording to match autoDoctype.

Method: documentation only; no commands were run.
