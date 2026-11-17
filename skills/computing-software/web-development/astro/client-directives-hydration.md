---
id: computing-software.web-development.astro.client-directives-hydration
name: client-directives-hydration
category: computing-software
field: web-development
product: astro
tags: [client-load, client-idle, client-visible, client-media, client-only]
level: practitioner
status: docs-checked
description: "Choose a client:* directive to hydrate UI framework components: load, idle, visible, media, only, plus timeout and rootMargin options."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/directives-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without a `client:*` directive a framework component renders HTML only, with no JavaScript. Directives work only on a framework component directly imported into an `.astro` file, not on dynamic tags or components passed via the MDX `components` prop.

- `client:load` (priority high): hydrate immediately on page load.
  ```astro
  <BuyButton client:load />
  ```
- `client:idle` (medium): hydrate after initial load and `requestIdleCallback`; falls back to the `load` event. Optional `timeout` in ms:
  ```astro
  <ShowHideButton client:idle={{timeout: 500}} />
  ```
- `client:visible` (low): hydrate when entering the viewport (IntersectionObserver). Optional `rootMargin` hydrates when a margin around it enters, which can reduce layout shifts:
  ```astro
  <HeavyImageCarousel client:visible={{rootMargin: "200px"}} />
  ```
- `client:media={string}` (low): hydrate when a media query is met.
  ```astro
  <SidebarToggle client:media="(max-width: 50em)" />
  ```
- `client:only={string}`: skips server rendering entirely and renders only on the client. You must name the framework:
  ```astro
  <SomeReactComponent client:only="react" />
  <SomeSolidComponent client:only="solid-js" />
  ```
  Show loading content with `slot="fallback"`:
  ```astro
  <ClientComponent client:only="vue">
    <div slot="fallback">Loading</div>
  </ClientComponent>
  ```

Integrations can add custom `client:*` directives via `addClientDirective`.

## Checked

2026-11-04. Confirmed against the Astro template directives reference: each client:* directive, priorities, requestIdleCallback and load fallback, timeout and rootMargin options, client:only framework values and fallback slot, addClientDirective. Nothing removed.

Method: documentation only; no commands were run.
