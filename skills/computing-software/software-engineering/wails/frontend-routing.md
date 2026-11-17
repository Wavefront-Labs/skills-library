---
id: computing-software.software-engineering.wails.frontend-routing
name: frontend-routing
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, routing, vue, react, angular, svelte, hash-router]
level: practitioner
status: docs-checked
description: "Choose the recommended router setup for Wails frontends: hash mode for Vue, Angular and React, and svelte-spa-router for Svelte."
sources: [https://wails.io/docs/guides/routing]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side routing in a Wails app

Goal: switch views in the webview with the router configuration the Wails docs recommend per framework. Vue, Angular and React use hash-based routing (the page does not explain why).

## Vue: Hash Mode

```js
import { createRouter, createWebHashHistory } from "vue-router";
const router = createRouter({ history: createWebHashHistory(), routes: [ /* ... */ ] });
```

## Angular: HashLocationStrategy

```ts
RouterModule.forRoot(routes, { useHash: true });
```

## React: HashRouter

```jsx
import { HashRouter, Routes, Route } from "react-router-dom";
<HashRouter basename={"/"}>
  <Routes>
    <Route path="/" element={<Page0 />} exact />
    <Route path="/page1" element={<Page1 />} />
  </Routes>
</HashRouter>
```

## Svelte: svelte-spa-router

```svelte
<script>
  import Router from "svelte-spa-router";
</script>
<Router routes={{
  "/": Home,
  "/products": wrap({ asyncComponent: () => import("./routes/Products.svelte") }),
  "/settings": Settings,
  "*": NotFound,
}} />
```
(The page's snippet uses `wrap` without showing its import.)

## Related

For runtime and display problems see `computing-software.software-engineering.wails.troubleshooting-runtime-and-display`. For SvelteKit see `computing-software.software-engineering.wails.sveltekit-frontend`.

## Gaps

No guidance for other frameworks.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Routing" guide.

Corrected or removed: Limited the hash-routing statement to Vue, Angular and React (svelte-spa-router is not described as hash based); removed the claim that the runtime is lost when navigating to another HTML file, which this page does not state.

Method: documentation only; no commands were run.
