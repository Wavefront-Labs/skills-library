---
id: computing-software.web-development.web-performance.hydration-cost-and-islands
name: hydration-cost-and-islands
category: computing-software
field: web-development
product: web-performance
tags: [javascript-performance, islands-architecture, partial-hydration, hydration, server-components, astro]
level: practitioner
status: docs-checked
description: "Reducing hydration cost: islands and partial hydration (Astro), React Server Components, resumability (Qwik) and what each trades off."
sources:
  - https://docs.astro.build/en/concepts/islands/
  - https://react.dev/reference/rsc/server-components
  - https://qwik.dev/docs/concepts/resumable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hydration cost and islands

Per the Qwik docs, hydration means the client framework restores three things for an SSR/SSG page: listeners, the component tree and application state. It is expensive because the framework downloads all component code for the current page and executes the templates to rebuild listener locations and the component tree.

## 1. Strategies
| Approach | How | Source |
|---|---|---|
| Islands / partial hydration | most of the page is static HTML; small islands of JavaScript added where interactivity is needed; also called partial or selective hydration | Astro |
| Server Components | render ahead of time in a separate environment, at build time or per request; their code and dependencies are not in the client bundle | React |
| Resumability | serialize listeners, component boundaries and state into the HTML so the client resumes rather than replays | Qwik |

## 2. Astro islands
- Astro renders every UI component to HTML and CSS and strips client JavaScript by default; a `client:*` directive makes a component an interactive island (for example `<MyReactComponent client:load />`).
- `client:idle` loads the component when the browser becomes idle; `client:visible` loads it once it enters the viewport.
- Islands load in parallel and hydrate in isolation, so a high-priority header need not wait for a heavy carousel. Client islands can still share state and communicate.
- Server islands (`server:defer`) render slow or personalised server content separately, with fallback content shown meanwhile (which can prevent layout shift), letting the outer shell be cached more aggressively.
- It is up to the developer to say which components need to run in the browser.

## 3. React Server Components
- Server Components can run once at build time or per request; the client sees only the rendered output, so libraries used only for rendering (the docs' example: marked and sanitize-html, about 75K gzipped) are not in the bundle and the extra fetch after load disappears.
- They cannot use `useState` or other interactive APIs; compose them with Client Components marked `"use client"`. There is no directive for Server Components (`"use server"` is for Server Functions).
- A Server Component can render a context provider imported from a Client Component module.
- Async Server Components can start a promise on the server and pass it to a Client Component that awaits it with `use` inside Suspense, without blocking the rest of the content.
- Bundler and framework APIs for RSC do not follow semver across React 19.x minors.

## 4. Qwik resumability
- Event listeners are serialized into the DOM (for example `on:click="./chunk.js#handler_symbol"`); Qwikloader sets up a single global listener, so no application code needs to be present at startup.
- Component boundaries and store-to-component subscriptions are serialized into the HTML; components can stay lazy and a component can resume without its parent's code.
- Serialization limits: classes (`instanceof` and prototypes) and streams cannot be serialized; code that cannot be serialized should run on the client only. Applications must be written with serializability in mind.

## Verify
- [ ] Bundle or network view shows client JavaScript only for components that need interactivity, and static sections cause no hydration work in the Performance trace.

## Checked
2026-11-09. Read the Astro islands page, the React Server Components reference page and the Qwik resumable page in full. Removed (not on those pages): Fresh, Eleventy is-land, Next.js and React Router, React 18 Suspense selective hydration, Nuxt and Angular lazy hydration, htmx and Turbo, the INP `loadState` and 4x throttle measuring advice, the practices list on `"use client"` placement and payload size, trade-off claims, and the patterns.dev source (not read).
Method: documentation only; no commands were run.
