---
id: computing-software.web-development.frontend-development.declarative-shadow-dom-ssr
name: declarative-shadow-dom-ssr
category: computing-software
field: web-development
product: frontend-development
tags: [web-components, custom-elements, declarative-shadow-dom, shadowrootmode, web-components-ssr, lit-ssr, sethtmlunsafe]
level: practitioner
status: docs-checked
description: "Server-rendering web components with declarative shadow DOM (template shadowrootmode), hydration with the existing root, and parsing caveats."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/template#shadowrootmode
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/attachShadow
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTMLUnsafe
  - https://lit.dev/docs/ssr/overview/
  - https://lit.dev/docs/ssr/client-usage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative shadow DOM for SSR

**Goal:** components with shadow roots render styled HTML on first paint, before JavaScript loads.

## 1. Markup
```html
<x-card>
  <template shadowrootmode="open">
    <style>:host{display:block;border:1px solid #ddd;border-radius:8px;padding:1rem}</style>
    <slot name="title"></slot><slot></slot>
  </template>
  <h2 slot="title">Order #42</h2>
  <p>Shipped</p>
</x-card>
```
The HTML parser attaches the shadow root immediately; no JS needed for rendering. `shadowrootmode` shipped in Chrome 111, Firefox 123 and Safari 16.4; the old non-standard `shadowroot` attribute (Chrome 90-110) was removed. Other options: `shadowrootdelegatesfocus`, `shadowrootclonable` and `shadowrootserializable` (Chrome 123-125, Firefox 123-128, Safari 18).

## 2. Hydrate without re-creating
```js
class XCard extends HTMLElement {
  constructor() {
    super();
    const internals = this.attachInternals();
    this.root = internals.shadowRoot ?? this.attachShadow({ mode: 'open' });   // reuse SSR root
    if (!internals.shadowRoot) this.root.innerHTML = TEMPLATE;                   // client-only render
  }
}
```
Calling `attachShadow()` with a matching `mode` on an element that already has a declarative root **clears** that root and returns it, discarding the server-rendered content; a different `mode` throws `NotSupportedError`. Check `internals.shadowRoot` first, as above.

## 3. Parsing caveats
- Only the HTML parser processes it. `innerHTML = '<template shadowrootmode…>'` does **not** create a shadow root; use `Element.setHTMLUnsafe()` (Chrome 124, Firefox 123, Safari 26) or `Document.parseHTMLUnsafe()`. If one host has several declarative roots only the first is created.
- `<style>` is duplicated per instance in SSR output - many instances bloat HTML. Keep component styles small or share via `adoptedStyleSheets` after hydration.
- Serialising back: `element.getHTML({ serializableShadowRoots: true })` for roots marked serializable.

## 4. With Lit
`@lit-labs/ssr` (labs, a low-level Node library) renders Lit components to DSD on the server; there are Eleventy, Astro and Next.js integrations. Load `@lit-labs/ssr-client/lit-element-hydrate-support.js` first on the client, before the component definitions.

## Verify
- [ ] With JS disabled, components render styled.
- [ ] After hydration there is one shadow root and event handlers work.
- [ ] No layout shift between SSR paint and hydrated state.

## Checked

Checked 2026-10-26 against mdn/content (main) template, Element.attachShadow, Element.setHTMLUnsafe and Element.getHTML pages, mdn/browser-compat-data and the Lit SSR docs (overview and client usage).

- Fixed: `attachShadow()` on an element with a declarative root always clears and returns it when the mode matches (it is not "in some cases"), and throws `NotSupportedError` on a mode mismatch.
- Replaced "all current engines" with the browser-compat-data versions; `setHTMLUnsafe` does not skip declarative roots (unlike `innerHTML`); only the first root per host is created.
- Confirmed: `shadowrootmode` options, `ElementInternals.shadowRoot`, `getHTML({ serializableShadowRoots: true })`, Lit hydrate-support load order and the Eleventy, Astro and Next.js integrations.

Method: documentation only; no commands were run.
