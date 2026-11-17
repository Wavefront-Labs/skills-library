---
id: computing-software.web-development.astro.framework-children-and-named-slots
name: framework-children-and-named-slots
category: computing-software
field: web-development
product: astro
tags: [children-prop, named-slots, nested-islands, render-props]
level: advanced
status: docs-checked
description: "Pass children and named slots from Astro into React, Preact, Solid, Svelte and Vue components, nest hydrated components, and avoid render props."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/framework-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inside an Astro file you can pass children to framework components. React, Preact and Solid read a `children` prop; Svelte and Vue use `<slot />`.

Named slots become top-level props in React, Preact and Solid, with `kebab-case` names converted to `camelCase`:

```astro
<MySidebar>
  <h2 slot="title">Menu</h2>
  <p>Here is a sidebar with some text and a button.</p>
  <ul slot="social-links">
    <li><a href="https://github.com/withastro">GitHub</a></li>
  </ul>
</MySidebar>
```

```jsx
// src/components/MySidebar.jsx
export default function MySidebar(props) {
  return (
    <aside>
      <header>{props.title}</header>
      <main>{props.children}</main>
      <footer>{props.socialLinks}</footer>
    </aside>
  )
}
```

Svelte and Vue use named `<slot>` elements and preserve `kebab-case`:

```jsx
<aside>
  <header><slot name="title" /></header>
  <main><slot /></main>
  <footer><slot name="social-links" /></footer>
</aside>
```

Children can themselves be hydrated components, from any framework:

```astro
<MyReactSidebar>
  <p>Here is a sidebar with some text and a button.</p>
  <div slot="actions">
    <MyReactButton client:idle />
    <MySvelteButton client:idle />
  </div>
</MyReactSidebar>
```

Framework component files themselves cannot mix frameworks. Astro components always render to static HTML, so React "render props" from an Astro component will not work; use named slots instead.

## Checked

2026-11-04. Confirmed against the Astro framework components guide: children prop for React, Preact and Solid, slot for Svelte and Vue, kebab-case to camelCase, nested hydrated components, no mixing inside framework files, render props note. Nothing removed.

Method: documentation only; no commands were run.
