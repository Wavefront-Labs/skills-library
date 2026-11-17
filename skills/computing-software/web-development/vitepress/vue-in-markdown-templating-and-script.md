---
id: computing-software.web-development.vitepress.vue-in-markdown-templating-and-script
name: vue-in-markdown-templating-and-script
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, vue-in-markdown, interpolation, script-setup, style-module, usedata, vue-sfc]
level: practitioner
status: docs-checked
description: "Use Vue interpolation, directives, script setup and style module inside Markdown pages, and avoid style scoped."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/using-vue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each Markdown file is compiled to HTML and then processed as a Vue single-file component, so Vue features work in content. The compiler detects purely static parts and removes them from the JS payload and from hydration; you pay only for dynamic bits.

**Interpolation and directives**

```md
{{ 1 + 1 }}

<span v-for="i in 3">{{ i }}</span>
```

**Root-level `<script>` and `<style>`** behave like SFCs (including `<script setup>` and `<style module>`), except there is no `<template>`; everything else is Markdown. They must come **after** the frontmatter.

```html
---
hello: world
---

<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

## Markdown Content

The count is: {{ count }}

<button :class="$style.button" @click="count++">Increment</button>

<style module>
.button { color: red; font-weight: bold; }
</style>
```

Avoid `<style scoped>` in Markdown: it forces a special attribute on every element on the page and bloats it; use `<style module>`.

VitePress runtime APIs like `useData()` work in pages:

```html
<script setup>
import { useData } from 'vitepress'
const { page } = useData()
</script>
<pre>{{ page }}</pre>
```

All Vue usage must be SSR-compatible (see the SSR skill).

Verify: click the button in dev and see the count change.

## Checked

Read the Templating, script and style, and SSR note sections of the Using Vue in Markdown guide. Confirmed static-content optimisation, interpolation and directives, root-level `<script>` and `<style>` after frontmatter with no `<template>`, the `<style scoped>` warning, and `useData`. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
