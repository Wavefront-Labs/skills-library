---
id: computing-software.web-development.svelte.svelte-head-element
name: svelte-head-element
category: computing-software
field: web-development
product: svelte
tags: [svelte-head, svelte-element, dynamic-tag, document-head, seo-meta]
level: practitioner
status: docs-checked
description: "svelte:head inserts into document.head (separate on SSR); svelte:element renders a tag unknown at author time, with void-element, namespace and nullish rules."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/05-svelte-head.md
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/06-svelte-element.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<svelte:head>` inserts elements into `document.head`. During server-side rendering, head content is exposed separately from body content. Like `<svelte:window>`, it may only appear at the top level of a component.

```svelte
<svelte:head>
  <title>Hello world!</title>
  <meta name="description" content="This is where the description goes for SEO" />
</svelte:head>
```

`<svelte:element this={expression} />` renders an element unknown at author time, for example from a CMS. Properties and event listeners are applied to it.

Rules:
- The only supported binding is `bind:this`; built-in bindings do not work on generic elements.
- A nullish `this` renders neither the element nor its children.
- If `this` names a void element (such as `br` or `hr`) and children are present, development mode throws a runtime error.
- Svelte tries to infer the namespace from surroundings; make it explicit with `xmlns`:

```svelte
<svelte:element this={tag} xmlns="http://www.w3.org/2000/svg" />
```

- `this` must be a valid DOM element tag; `#text` or `svelte:head` will not work.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the svelte:head and svelte:element pages: head insertion, separate SSR exposure, top-level-only rule, bind:this-only binding, nullish this, void-element dev error, xmlns, valid-tag rule. Nothing removed.
