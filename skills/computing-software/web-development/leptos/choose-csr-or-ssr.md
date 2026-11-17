---
id: computing-software.web-development.leptos.choose-csr-or-ssr
name: choose-csr-or-ssr
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, csr, ssr, hydration, cargo-leptos, trunk, architecture]
level: practitioner
status: docs-checked
description: "Decide between Leptos client-side rendering with Trunk and full-stack SSR with cargo-leptos, using the trade-offs the Leptos book lists."
sources: [https://book.leptos.dev/getting_started/, https://book.leptos.dev/01_introduction.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose CSR (Trunk) or SSR (cargo-leptos) for a Leptos app

Goal: pick the right Leptos rendering model before starting a project.

## Option 1: Client-side rendering with Trunk

Trunk compiles the Leptos app to WebAssembly and runs it in the browser like a typical JS single-page app.

- Pros: faster build times, quicker iteration loop, simpler mental model, more deployment options. Good for a snappy website, or when you already have a server or API.
- Cons: slower initial load for end users than SSR, the usual SEO challenges of a JS SPA, and JavaScript must be enabled because a generated JS snippet loads the WASM bundle.

## Option 2: Full-stack SSR with cargo-leptos

The app is rendered to HTML on the server, then WebAssembly instruments the HTML so it becomes interactive; this step is called hydration. The server side integrates with Actix-web (`leptos_actix`) or Axum (`leptos_axum`).

- Pros: best initial load times and SEO, good for CRUD-style sites and custom web apps where Rust powers frontend and backend, and server functions let client code call server code transparently.
- Cons: slower developer loop (both server and client recompile on Rust changes) and extra complexity from hydration.

## Analogy for JS developers

CSR mode is like React or SolidJS (a UI you can pair with any server stack). SSR mode is like Next.js or SolidStart (one language for UI and server).

## Where the book goes

The introduction describes a path from a simple browser-rendered app toward full-stack SSR with hydration. Part 1 of the book uses CSR with Trunk to teach reactive UIs; cargo-leptos is introduced in Part 2.

## Related

- CSR setup: `computing-software.web-development.leptos.csr-trunk-setup`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/getting_started/, https://book.leptos.dev/01_introduction.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
