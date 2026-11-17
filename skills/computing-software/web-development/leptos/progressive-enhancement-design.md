---
id: computing-software.web-development.leptos.progressive-enhancement-design
name: progressive-enhancement-design
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, progressive-enhancement, graceful-degradation, ssr, forms]
level: practitioner
status: docs-checked
description: "Design a Leptos app that keeps working without WASM or JS: SSR, native HTML elements, URL-driven state, SsrMode choice and form-based mutations."
sources: [https://book.leptos.dev/progressive_enhancement/index.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Progressive enhancement and graceful degradation in Leptos

Goal: make most of the app work when WASM, JS or the network is missing.

Progressive enhancement starts with plain HTML and layers on CSS, JS, then WASM. Graceful degradation is handling failure when a layer is missing: old browser without WASM, WASM or JS disabled, JS unsupported (some accessibility devices), assets never arrived because the connection dropped, or later navigations failing (for example on a subway). WASM is the newest, least-supported layer, so degradation matters most for WASM apps.

## Practices

1. Use server-side rendering. Without it the app is blank unless both JS and WASM load (acceptable perhaps for internal apps behind login).
2. Prefer native HTML elements: `<a>` for navigation (including in-page hashes), `<details>` for accordions, `<form>` to persist state in the URL.
3. Store state in the URL (route params or query string) so the server can render it and `<a>`/`<form>` can change it with no JS/WASM.
4. Choose an `SsrMode` deliberately (`PartiallyBlocked` or `InOrder` for robustness):
   - Out-of-order streaming needs a little inline JS and fails if the connection breaks mid-response or JS is unsupported.
   - Async streaming sends a complete page but only after all resources load.
   - In-order streaming shows pieces top-down sooner.
   - Partially-blocked builds on out-of-order, replacing `<Suspense/>` fragments that read blocking resources on the server; costs a little response time (O(n) string replacement) for a more complete first HTML. Good when there is a clear important/less-important split (blog post vs comments). Blocking on everything recreates async rendering.
5. Lean on `<form>`: a `<form method="GET">` persisting state in the URL works with pure HTML and enhances to client-side navigation.

For mutations use `<ActionForm/>`: computing-software.web-development.leptos.action-form.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/progressive_enhancement/index.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
