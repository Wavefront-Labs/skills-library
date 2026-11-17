---
id: computing-software.web-development.nuxt.nuxt-client-and-server-components
name: nuxt-client-and-server-components
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, client-components, server-components, clientonly, island]
level: advanced
status: docs-checked
description: "Use .client.vue suffix and the ClientOnly component for browser-only rendering, with the onMounted and nextTick caveat."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.components.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/1.components/1.client-only.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add the `.client` suffix (`Comments.client.vue`) to render a component only on the client side. This works only through Nuxt auto-imports and `#components` imports; explicitly importing the file from its real path does not make it client-only.

`.client` components are rendered only after being mounted. To access the rendered template using `onMounted()`, add `await nextTick()` in the callback of the hook.

Alternative: the `<ClientOnly>` component renders its default slot only on the client. The slot content is tree-shaken out of the server build, so CSS used by components inside it may not be inlined in the initial HTML. Server-side placeholder: props `placeholderTag` / `fallbackTag` (a tag) and `placeholder` / `fallback` (content), or the `#fallback` slot, shown until `<ClientOnly>` is mounted in the browser. To reach elements inside it, watch a template ref (`useTemplateRef`) rather than reading the DOM immediately.

```vue
<ClientOnly fallback-tag="span" fallback="Loading comments...">
  <Comment />
</ClientOnly>
```

Server components use the `.server` suffix (`HighlightedMarkdown.server.vue`). A standalone server component is always rendered on the server (an Islands component), so its libraries stay out of the client bundle; when its props update, a network request updates the rendered HTML in place. They use `<NuxtIsland>` under the hood (the `lazy` prop and `#fallback` slot are passed down) and must have a single root element (HTML comments count as elements). A `.server` plus `.client` pair of the same name is two halves of one component: the server half renders on the server, the client half once mounted in the browser.

## Checked

2026-11-04. Confirmed against the Nuxt components directory page and the ClientOnly page: .client suffix and its auto-import-only limit, the onMounted/nextTick note, ClientOnly props, #fallback slot, tree-shaking note and template-ref approach, .server standalone and paired behaviour, single-root rule. Removed: the claim that nothing is produced on the server, the third-party window/document advice, the hydration-mismatch remark, the general advice paragraph, the cited server-components guide path (not among the sources read) and the Verify step.

Method: documentation only; no commands were run.
