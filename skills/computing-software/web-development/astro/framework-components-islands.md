---
id: computing-software.web-development.astro.framework-components-islands
name: framework-components-islands
category: computing-software
field: web-development
product: astro
tags: [ui-frameworks, react, islands, hydration, mixing-frameworks]
level: practitioner
status: docs-checked
description: "Use React, Svelte, Vue and other framework components in Astro: static by default, hydrate with client directives, mix frameworks, and know the limits."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/framework-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Official integrations: React, Preact, Svelte, Vue, SolidJS and AlpineJS. Install via the integrations guide. Import a framework component in the component script and use it in the template. By default it renders only on the server, as static HTML with no JavaScript.

Hydrate with a `client:*` directive. All except `client:only` render on the server first, then send JS per the directive; a shared framework is sent once.

```astro
---
import InteractiveButton from '../components/InteractiveButton.jsx';
import InteractiveCounter from '../components/InteractiveCounter.jsx';
import InteractiveModal from '../components/InteractiveModal.svelte';
---
<InteractiveButton client:load />
<InteractiveCounter client:visible />
<InteractiveModal client:only="svelte" />
```

Mix frameworks inside one `.astro` file; component type is recognized by file extension (React and Preact need extra config since both use JSX). Only `.astro` files can contain components from multiple frameworks.

Hydrated props must be serializable: plain object, `number`, `string`, `Array`, `Map`, `Set`, `RegExp`, `Date`, `BigInt`, `URL`, `Uint8Array`, `Uint16Array`, `Uint32Array`, `Infinity`. Functions cannot be passed to make something interactive.

You cannot import `.astro` components inside a `.jsx` or `.svelte` file, nor hydrate an Astro component (error). Instead pass Astro output as children from an `.astro` file:

```astro
<MyReactComponent>
  <MyAstroComponent slot="name" />
</MyReactComponent>
```

For client JavaScript on Astro components, use `<script>` tags.

## Checked

2026-11-04. Confirmed against the Astro framework components guide: official integrations list, static by default, client directives, framework sent once, mixing frameworks and the .astro-only rule, serializable prop types, no .astro imports in framework files, hydrating an Astro component errors. Nothing removed.

Method: documentation only; no commands were run.
