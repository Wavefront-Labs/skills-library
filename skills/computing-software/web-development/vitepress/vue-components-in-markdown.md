---
id: computing-software.web-development.vitepress.vue-components-in-markdown
name: vue-components-in-markdown
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, vue-components, global-components, component-naming, components-in-headers, code-splitting, hydration-mismatch]
level: practitioner
status: docs-checked
description: "Import or globally register Vue components for Markdown, name them to avoid p-tag hydration errors, and use them in headings."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/using-vue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Import locally** when a component is used by few pages so it is code-split and loaded only when needed:

```md
<script setup>
import CustomComponent from '../components/CustomComponent.vue'
</script>

# Docs

<CustomComponent />
```

**Register globally** when most pages use it, in the theme's `enhanceApp` (`app.component('MyGlobalComponent', ...)`; see the global components skill). Vite glob imports can auto-register a folder.

**Naming rule (important).** A component name must contain a hyphen or be PascalCase. Otherwise it is treated as an inline element and wrapped in a `<p>`, which causes a hydration mismatch because `<p>` cannot contain block elements.

**Components in headings.** `# text <Tag/>` renders the component in the `<h1>` but the parsed header (used for sidebar and document title) is just `text`. Wrapping in backticks, `# text \`<Tag/>\``, shows the tag literally and the parsed header is `text <Tag/>`. HTML inside code is displayed as-is; only unwrapped HTML is parsed by Vue. The output HTML comes from markdown-it, while headers for the sidebar and title are parsed by VitePress.

**Teleports.** Only teleports to `body` have SSG support. For other targets wrap the content in `<ClientOnly>` or inject the markup via the `postRender` hook.

Verify: load the built page and confirm the browser console shows no hydration mismatch warning.

## Checked

Read the Using Vue in Markdown guide in full. Confirmed local import and code splitting, global registration with a Vite glob import, the hyphen or PascalCase naming rule and its hydration cause, the heading table, and the teleport limits. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
