---
id: computing-software.web-development.hono.hono-jsx-guide
name: hono-jsx-guide
category: computing-software
field: web-development
product: hono
tags: [hono, jsx, tsx, ssr, components]
level: practitioner
status: docs-checked
description: "Use hono/jsx: tsconfig and Deno settings, components, metadata hoisting, memo, context, async components, Suspense, ErrorBoundary and CSP nonces."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/jsx.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hono JSX guide

## Settings
`tsconfig.json`:

```json
{ "compilerOptions": { "jsx": "react-jsx", "jsxImportSource": "hono/jsx" } }
```
or pragmas `/** @jsx jsx */` and `/** @jsxImportSource hono/jsx */`. Deno uses `deno.json`: `"jsx": "precompile"`, `"jsxImportSource": "@hono/hono/jsx"`. Rename the entry to `.tsx` and update the dev script too.

## Components
```tsx
import type { FC } from 'hono/jsx'
const Layout: FC = (props) => <html><body>{props.children}</body></html>
app.get('/', (c) => c.html(<Layout><h1>Hello Hono!</h1></Layout>))
```
Also: `Fragment` or `<></>`, `PropsWithChildren<Post>`, raw HTML with `dangerouslySetInnerHTML={{ __html: 'JSX &middot; SSR' }}`, `memo(() => <header/>)`, and `createContext`/`useContext` with `<ThemeContext.Provider value={...}>`.

## Metadata hoisting
`<title>`, `<link>` and `<meta>` inside any component are hoisted into `<head>` (the page's example uses `c.setRenderer`):

```tsx
c.render(<><title>About Page</title><meta name='description' content='...' />content</>)
```
Existing head elements are not removed: a default `<title>` plus a component title yield BOTH.

## Async and streaming
Async components work; `c.html()` awaits them. Experimental `Suspense` with `renderToReadableStream`:

```tsx
import { renderToReadableStream, Suspense } from 'hono/jsx/streaming'
const stream = renderToReadableStream(<html><body><Suspense fallback={<div>loading...</div>}><Component /></Suspense></body></html>)
return c.body(stream, { headers: { 'Content-Type': 'text/html; charset=UTF-8', 'Transfer-Encoding': 'chunked' } })
```
Experimental `ErrorBoundary fallback={<div>Out of Service</div>}` catches sync and async child errors. `StreamingContext value={{ scriptNonce: 'random-nonce-value' }}` adds a CSP nonce to scripts that Suspense and ErrorBoundary emit.

## Custom elements
```ts
declare module 'hono/jsx' {
  namespace JSX { interface IntrinsicElements { 'my-custom-element': HTMLAttributes & { 'x-event'?: 'click' | 'scroll' } } }
}
```

## Gotcha
The page says a `.ts` entry file must be renamed to `.tsx`, otherwise the application will not run at all. It also shows combining JSX with the `html` helper for templated layouts.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/guides/jsx.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the jsxRenderer attribution for metadata hoisting (page shows only setRenderer).

Method: documentation only; no commands were run.
