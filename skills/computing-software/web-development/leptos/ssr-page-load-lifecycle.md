---
id: computing-software.web-development.leptos.ssr-page-load-lifecycle
name: ssr-page-load-lifecycle
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, ssr, hydration, lifecycle, leptos-axum, leptos-actix]
level: practitioner
status: docs-checked
description: "Explain what happens from request to hydration to client-side navigation in a Leptos SSR app, including ssr and hydrate features and leptos_routes."
sources: [https://book.leptos.dev/ssr/22_life_cycle.html, https://book.leptos.dev/csr_wrapping_up.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand which part of a server-rendered Leptos app runs where, so you can reason about bugs.

## Two build targets
- Server: Actix or Axum, compiled with the Leptos `ssr` feature.
- Browser: WASM, compiled with the `hydrate` feature.
`cargo-leptos` builds both.

## On the server
1. Browser sends GET for the URL.
2. The server checks it can handle that path. `.leptos_routes()` in `leptos_axum` / `leptos_actix` walks the `<Routes/>` tree at startup, lists every route, and tells the server router to hand those requests to Leptos.
3. Leptos renders the root component (e.g. `<App/>`) with the URL, headers and request metadata.
4. The app runs once on the server, building an HTML tree (resources and `<Suspense/>` come later).
5. The HTML is returned with info for loading the WASM build. This HTML is the app "freeze-dried": no reactivity or event listeners.

## In the browser
1. The browser renders the HTML immediately and fetches JS and WASM.
2. Once loaded, the WASM app does the same route matching; `<Routes/>` is identical on both sides, so it renders the same page.
3. Hydration does not recreate DOM nodes; it walks the existing tree, picking up elements and adding interactivity.

## Client-side navigation
After hydration, clicking a link is handled in WASM with no new full-page request: a server-loaded multi-page app upgrades into a single-page app.

## Gotchas
- Before hydration finishes the page looks interactive but is not; e.g. a counter click is ignored.
- To enable the upgrade from server rendering to client rendering, the page says everything in your application must be able to run on both the client and the server; this is why it explains that you cannot just `.await` in a component or call library X directly there as you could in a server function. See `computing-software.web-development.leptos.ssr-hydration-bugs-and-fixes`.
- CSR drawbacks that motivate SSR (blank screen until JS/WASM load, longer load time, bad SEO, broken for users whose JS/WASM do not load) are listed on the book's "Wrapping Up Part 1: Client-Side Rendering" page.

## Checked

2026-11-07: Read in full: ssr/22_life_cycle.md (two build targets, On the Server, In the Browser, Client-Side Navigation) and csr_wrapping_up.md (the three CSR drawbacks). The skill's two build targets, route-walking by .leptos_routes(), freeze-dried HTML, hydration walking existing nodes and the not-yet-interactive caveat all match. Corrections: the gotcha that you 'cannot simply .await' was reworded to the page's actual claim (everything must run on both client and server); the 'csr_wrapping_up' pointer, which had no source, now names the book page and lists its drawbacks as that page words them, and that page was added to sources.

Method: documentation only; no commands were run.
