---
id: computing-software.web-development.leptos.async-execution-stages
name: async-execution-stages
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, async, resources, suspense, hydration, ssr]
level: practitioner
status: docs-checked
description: "Reference table of where server functions, Resources, local resources and Suspend run during SSR, hydration and CSR, and the hydration bugs side effects can cause."
sources: [https://book.leptos.dev/server/28_async_quick_reference.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Where async code runs: SSR vs hydration vs CSR

Goal: predict which stage executes a server function, Resource, local resource, or `Suspend`, to avoid hydration mismatches.

## Reference (from the page's table)

- Server function, server side: during SSR runs as a normal async function with full reactive context; when hit as an HTTP endpoint it is standalone and reactive context is typically unavailable.
- Server function, client side: not executed during hydration (when inside Resource closures); in CSR it makes an HTTP request and deserializes the response. Its body is never compiled into the client.
- Resource: on the server, async closures run in parallel where possible and results are encoded into `<script>` tags in the response. During hydration the closure is not run; the scripts provide results. In CSR it re-runs as the reactive system requires.
- Local Resource (client only): not run during hydration; executed once after hydration for the initial value, then as required.
- `Suspend`: on the server futures run in parallel and `SsrMode` affects polling and output order. On the client they are fully executed again during hydration, and the returned view hydrates the HTML.

There are up to three execution stages split across server and client.

## Pitfalls the page states

- Side effects inside a Resource or `Suspend` may not run at the same time or order in each stage. Example: a Resource closure that sets a signal works in SSR and CSR but not in hydration (the closure body is not executed), causing a hydration mismatch. Fix: have the Resource return the value and `.await` it inside a `Suspend` before setting the signal, so it happens in all three stages.
- One signal written by several `Suspend`s can be set in a different order on server and client (different executors), giving non-deterministic hydration errors.
- Server functions invoked during SSR see all app contexts; their HTTP endpoint counterparts do not. `expect_context`/`use_context` on app-provided types fails there unless the value is provided with `.leptos_routes_with_context()`.
- The table describes the typical setup (server functions awaited only in Resources, Resources awaited only in Suspends); other nesting can behave differently.

Related: computing-software.web-development.leptos.server-state-and-context.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/server/28_async_quick_reference.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
