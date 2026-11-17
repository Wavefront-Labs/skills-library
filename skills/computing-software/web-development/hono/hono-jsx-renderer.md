---
id: computing-software.web-development.hono.hono-jsx-renderer
name: hono-jsx-renderer
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, jsx, layout, streaming]
level: practitioner
status: docs-checked
description: "Set page layouts with jsxRenderer and c.render in Hono: docType, streaming, nested layouts, useRequestContext and extending ContextRenderer."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/jsx-renderer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JSX Renderer

Import: `import { jsxRenderer, useRequestContext } from 'hono/jsx-renderer'`. It sets the layout used by `c.render()` without `c.setRenderer()`.

```tsx
app.get('/page/*', jsxRenderer(({ children }) => (
  <html><body><header>Menu</header><div>{children}</div></body></html>
)))
app.get('/page/about', (c) => c.render(<h1>About me!</h1>))
```

## Options
- `docType: boolean | string`: `false` removes the DOCTYPE; a string sets a custom one.
- `stream: boolean | Record<string, string>`: `true` streams and adds `Transfer-Encoding: chunked`, `Content-Type: text/html; charset=UTF-8`, `Content-Encoding: Identity`. A Record overrides header values. Use with `<Suspense fallback={...}>` and async components.
- Function form: `jsxRenderer(Layout, (c) => ({ stream: c.req.header('X-Enable-Streaming') === 'true' }))`. For SSG disable streaming: `(c) => ({ stream: !isSSGContext(c) })`.

## Nested layouts
The `Layout` prop wraps the parent layout:

```tsx
const blog = new Hono()
blog.use(jsxRenderer(({ children, Layout }) => (
  <Layout><nav>Blog Menu</nav><div>{children}</div></Layout>
)))
app.route('/blog', blog)
```

## useRequestContext
`const c = useRequestContext()` inside a component returns the Context (for example `c.req.url`).

## Extend ContextRenderer
```tsx
declare module 'hono' {
  interface ContextRenderer {
    (content: string | Promise<string>, props: { title: string }): Response
  }
}
// layout receives { children, title }; call c.render(<div/>, { title: 'My favorites' })
```

## Gotcha
`useRequestContext()` does not work with Deno's `"jsx": "precompile"`; use `"jsx": "react-jsx"` with `"jsxImportSource": "hono/jsx"`.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/jsx-renderer.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
