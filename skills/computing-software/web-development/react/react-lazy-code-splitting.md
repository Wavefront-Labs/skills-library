---
id: computing-software.web-development.react.react-lazy-code-splitting
name: react-lazy-code-splitting
category: computing-software
field: web-development
product: react
tags: [react, react-lazy, code-splitting, dynamic-import, suspense, bundle-size, preloading, web-development]
level: practitioner
status: docs-checked
description: "Code splitting React apps with React.lazy and Suspense: route and modal splitting, named exports, preloading, error handling for failed chunks."
sources:
  - https://react.dev/reference/react/lazy
  - https://react.dev/reference/react/Suspense
  - https://vite.dev/guide/build#load-error-handling
  - https://nextjs.org/docs/app/guides/lazy-loading
  - https://reactrouter.com/start/data/route-object
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React.lazy code splitting

**Goal:** ship less JavaScript up front by loading routes and heavy widgets on demand.

## 1. Basic split
```jsx
import { lazy, Suspense } from "react";
const Settings = lazy(() => import("./Settings"));   // module must default-export a component

<Suspense fallback={<Spinner />}>
  <Settings />
</Suspense>
```
Declare `lazy` at module top level. Declaring it inside a component creates a new type each render and resets state.

## 2. Named exports
```jsx
const Chart = lazy(() => import("./charts").then(m => ({ default: m.LineChart })));
```

## 3. What to split
- Routes (React Router has a route `lazy` option; frameworks split routes for you).
- Heavy, rarely used UI: rich text editors, charts, maps, admin panels, modals.
- Not tiny components - each chunk adds a request and a loading state.

## 4. Preload to hide latency
```jsx
const loadEditor = () => import("./Editor");
const Editor = lazy(loadEditor);
<button onMouseEnter={loadEditor} onFocus={loadEditor} onClick={() => setOpen(true)}>Edit</button>
```
Modules are cached, so the later `lazy` call resolves instantly.

## 5. Failed chunk loads
After a deploy, old clients request chunk hashes that no longer exist. Wrap lazy areas in an error boundary with a reload action; Vite emits a `vite:preloadError` event when a dynamic import fails to load; the Vite docs handle it with `window.location.reload()`, and `event.preventDefault()` stops the error being thrown. Keep previous build assets on the CDN for a while.

## 6. Fallback placement
Place Suspense boundaries where a loading state makes sense (page body, panel), not around every component. Transitions (router navigation) keep old UI on screen instead of showing the fallback.

## 7. SSR
In Next.js use `next/dynamic`, a composite of `React.lazy()` and Suspense; its `ssr: false` option only works in Client Components.

## Verify
- [ ] Bundle analyser (for example `rollup-plugin-visualizer` with Vite) shows the heavy module in its own chunk.
- [ ] Network tab: chunk loads only when the feature is used (or on hover preload).
- [ ] Simulated chunk 404 shows a recoverable error, not a white screen.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the Vite build guide (Vite 8.3.5), the Next.js lazy-loading guide (Next.js 16.4.3) and the React Router route object docs. Confirmed: `lazy` takes a function returning a Promise of a module with a default export and must be declared at module top level (inside a component it resets state); `vite:preloadError` and its `preventDefault` behaviour; transitions keep already revealed content instead of re-showing a fallback; `next/dynamic` composes `React.lazy()` and Suspense and `ssr: false` only works in Client Components; React Router's route `lazy` property. Removed the streaming SSR version claim, "biggest win" and the `source-map-explorer` tool name (its repository was last updated in 2023).

Method: documentation only; no commands were run.
