---
id: computing-software.web-development.hono.hono-html-helper
name: hono-html-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, html, templating, xss]
level: practitioner
status: docs-checked
description: "Write HTML with the html tagged template and raw() in Hono, embed it in JSX, build function components, and know raw() output is not escaped."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/html.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# html helper

Import: `import { html, raw } from 'hono/html'`.

```ts
app.get('/:username', (c) => {
  const { username } = c.req.param()
  return c.html(html`<!doctype html><h1>Hello! ${username}!</h1>`)
})
```

`raw()` renders its content as is, and you must escape those strings yourself:

```ts
const name = 'John &quot;Johnny&quot; Smith'
return c.html(html`<p>I'm ${raw(name)}.</p>`)
```

## Inline script inside JSX
No `dangerouslySetInnerHTML` needed; it is not escaped:

```tsx
<head><title>Test Site</title>{html`<script>/* not escaped */</script>`}</head>
```

## As a function component
`html` returns an `HtmlEscapedString`, so it can act as a fully functional component without JSX. The docs have a section titled Use `html` to speed up the process instead of `memo`:

```ts
const Footer = () => html`<footer><address>My Address...</address></footer>`
```

With props:

```tsx
const Layout = (props: SiteData) => html`
<html><head><title>${props.title}</title></head>
<body>${props.children}</body></html>`

const Content = (props) => (
  <Layout {...props.siteData}><h1>Hello {props.name}</h1></Layout>
)
```
The docs note more elements slow down JSX, but not template literals.

## Gotcha
`raw()` content is rendered as is: the page says you have to escape these strings yourself.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/html.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the claim that interpolated values are escaped and the "safe path" advice (the page never states either).

Method: documentation only; no commands were run.
