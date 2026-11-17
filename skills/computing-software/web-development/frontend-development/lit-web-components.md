---
id: computing-software.web-development.frontend-development.lit-web-components
name: lit-web-components
category: computing-software
field: web-development
product: frontend-development
tags: [lit-element, lit, web-components, reactive-properties, lit-html, custom-elements]
level: practitioner
status: docs-checked
description: "Building web components with Lit 3: reactive properties and state, template bindings, styles, update lifecycle, decorators and TypeScript class-field pitfalls."
sources:
  - https://lit.dev/docs/components/overview/
  - https://lit.dev/docs/components/properties/
  - https://lit.dev/docs/components/decorators/
  - https://lit.dev/docs/components/lifecycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lit web components

## 1. Component
```ts
import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";

@customElement("x-counter")
export class XCounter extends LitElement {
  static styles = css`:host { display: inline-flex; gap: .5rem; } button { font: inherit; }`;
  @property({ type: Number, reflect: true }) count = 0;     // public: attribute <-> property
  @property({ attribute: "step-size", type: Number }) step = 1;
  @state() private pressed = false;                          // internal, triggers render

  render() {
    return html`
      <button ?disabled=${this.count <= 0} @click=${() => this.change(-this.step)}>-</button>
      <output>${this.count}</output>
      <button @click=${() => this.change(this.step)}>+</button>`;
  }
  private change(d: number) {
    this.count += d;
    this.dispatchEvent(new CustomEvent("count-changed", { detail: this.count, bubbles: true, composed: true }));
  }
}
declare global { interface HTMLElementTagNameMap { "x-counter": XCounter } }
```
Binding prefixes: text/attribute `${}`, property `.value=${v}`, boolean attribute `?hidden=${b}`, event `@input=${fn}` (auto-bound to `this`).

## 2. Update lifecycle
Property set -> batched async update (microtask) -> `willUpdate(changed)` (derive state) -> `render()` -> `updated(changed)` / `firstUpdated()` (DOM ready). `await el.updateComplete` in tests before asserting. Never set reactive properties in `updated()` unconditionally (infinite loop).

## 3. TypeScript decorator gotchas
- Lit supports both TypeScript experimental decorators and standard decorators. Its docs currently recommend experimental decorators for production (`experimentalDecorators: true`); standard decorators generally need the `accessor` keyword, as in `@property() accessor count = 0;`.
- With experimental decorators, set `"useDefineForClassFields": false` (needed when `target` is ES2022 or later): class fields are defined on the instance and shadow Lit's prototype accessors, so nothing re-renders.
- Without TS: `static properties = { count: { type: Number } }` and initialise in the constructor.

## 4. Ecosystem
`@lit/context` (dependency injection), `@lit/task` (async data with pending/error render), `@lit/react` `createComponent` (React wrapper), `@lit-labs/ssr` (declarative shadow DOM SSR).

## Gotchas
- Objects/arrays: mutate-in-place does not trigger updates; assign a new reference or call `this.requestUpdate()`.
- Attribute values are strings; declare `type` so `count="5"` converts to a number.
- Events must be `composed: true` to escape the shadow root.

## Verify
- [ ] `@open-wc/testing` or Vitest browser mode test awaits `updateComplete` and checks rendered shadow DOM.

## Checked

Checked 2026-10-26 against the lit.dev v3 docs (lifecycle, properties, decorators, SSR, React frameworks, context, task) from the lit/lit.dev repository.

- Confirmed: updates are batched at microtask timing; `willUpdate`, `updated`, `firstUpdated` and `updateComplete`; changing a property after `render()` (for example in `updated()`) triggers another update; mutating an object or array does not trigger an update (assign a new reference or call `requestUpdate()`); `reflect` defaults to false and `attribute: false` disables the attribute; `@lit/context`, `@lit/task` and `createComponent({ tagName, elementClass, events })` from `@lit/react`.
- Confirmed from the templates docs: `?attr`, `.prop` and `@event` binding prefixes, with listeners bound to the component.
- Fixed: decorator guidance now follows the docs (experimental decorators recommended, `useDefineForClassFields: false`, `accessor` for standard decorators).

Method: documentation only; no commands were run.
