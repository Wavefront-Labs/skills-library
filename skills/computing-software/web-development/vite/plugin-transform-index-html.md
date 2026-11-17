---
id: computing-software.web-development.vite.plugin-transform-index-html
name: plugin-transform-index-html
category: computing-software
field: web-development
product: vite
tags: [transform-index-html-hook, html-tag-descriptor, inject-to, index-html-order]
level: advanced
status: docs-checked
description: "transformIndexHtml hook: return a string, tag descriptors with injectTo, or { html, tags }; order pre and post; context with server or bundle."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`transformIndexHtml` is a per-environment, async, sequential hook for HTML entry files. It receives the HTML and a context (`path`, `filename`, `originalUrl`, plus `server` in dev or `bundle` and `chunk` in build). It may return:
- a transformed string,
- an array of `HtmlTagDescriptor` objects to inject,
- `{ html, tags }`.

```ts
interface HtmlTagDescriptor {
  tag: string
  attrs?: Record<string, string | boolean>  // escaped automatically
  children?: string | HtmlTagDescriptor[]
  injectTo?: 'head' | 'body' | 'head-prepend' | 'body-prepend'  // default 'head-prepend'
}
```

Order: by default the hook runs after the HTML was transformed. `order: 'pre'` runs before HTML processing, needed when an injected script must go through the Vite plugin pipeline; `order: 'post'` runs after all default-order hooks. Use the object form `{ order, handler }`.

```js
transformIndexHtml(html) {
  return html.replace(/<title>(.*?)<\/title>/, `<title>Title replaced!</title>`)
}
```

It is not called when a framework handles entry files itself (the docs cite SvelteKit).

## Checked

Date: 2026-11-07

Read api-plugin.md in full (transformIndexHtml). Confirmed kind and scope, return forms, HtmlTagDescriptor fields and injectTo default, order pre/post semantics and the SvelteKit note. Nothing removed.

Method: documentation only; no commands were run.
