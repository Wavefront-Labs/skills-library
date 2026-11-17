---
id: computing-software.web-development.htmx.htmx-pattern-web-components
name: htmx-pattern-web-components
category: computing-software
field: web-development
product: htmx
tags: [htmx, web-components, shadow-dom, htmx-process, custom-elements]
level: advanced
status: docs-checked
description: "Use htmx inside web components and shadow DOM: call htmx.process(root) after rendering, and reach outside the shadow tree with the host and global selector prefixes."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/web-components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make hx- attributes work inside a custom element's shadow DOM.

htmx does not see inside shadow DOM by default. After you create the content, tell htmx about the shadow root with `htmx.process`:

```js
customElements.define('my-component', class MyComponent extends HTMLElement {
  // runs when the custom element is added to the page
  connectedCallback() {
    const root = this.attachShadow({ mode: 'closed' })
    root.innerHTML = `
      <button hx-get="/my-component-clicked" hx-target="next div">Click me!</button>
      <div></div>
    `
    htmx.process(root) // tell htmx about this component's shadow DOM
  }
})
```

After that most features work as normal.

Selector scope. Selectors such as the one in `hx-target` only see elements inside the same shadow DOM. To reach outside it:
- `host` selects the element hosting the current shadow DOM.
- `global`, used as a prefix, selects from the main document instead of the current shadow DOM.

No shadow DOM. The same principles generally apply to web components that do not use shadow DOM: selectors are not encapsulated, but you still point htmx at the component's content by calling `htmx.process`.

## Checked

2026-11-07. Confirmed against the htmx Web Components example page (`htmx.process(root)`, the component code, same-shadow-DOM selector scope, `host` and `global` prefixes, non-shadow-DOM note). Removed the invented Verify step.
Method: documentation only; no commands were run.
