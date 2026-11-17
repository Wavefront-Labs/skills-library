---
id: computing-software.web-development.vitepress.mpa-mode-client-scripts
name: mpa-mode-client-scripts
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, mpa, mpa-mode, script-client, zero-javascript, multi-page-app, experimental, vue-ssr]
level: advanced
status: docs-checked
description: "Enable experimental MPA mode for zero-JS pages and opt into browser code with the VitePress-only script client tag."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/mpa-mode.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MPA (multi-page application) mode is experimental. Enable it with `vitepress build --mpa` or `mpa: true` in config.

**What changes**
- Pages ship with no JavaScript by default, which usually improves audit-tool performance scores for the initial visit.
- No SPA navigation: links between pages cause full reloads, so later navigations feel less instant than in SPA mode.
- Vue is used purely as a server-side templating language. No event handlers are attached, so there is no interactivity unless you opt in.

**Opt in with `<script client>`**

```html
<script client>
document.querySelector('h1').addEventListener('click', () => {
  console.log('client side JavaScript!')
})
</script>
# Hello
```

`<script client>` is a VitePress feature, not Vue's. It works in `.md` and `.vue` files, but only in MPA mode. Client scripts from all theme components are bundled together, while a page's own client script is split for that page only. It is processed as a plain JavaScript module and is **not evaluated as Vue component code**, so there is no `ref`, reactivity or component lifecycle inside it. For that reason use MPA mode only when the site needs minimal client interactivity.


Verify: a built page ships no JavaScript unless it uses `<script client>`.

## Checked

2026-11-08. Read the VitePress docs source pages mpa-mode and site-config (mpa). Confirmed enabling by --mpa or mpa: true, the experimental label, no JavaScript by default, full page reloads, Vue as a server-side template, the script client tag rules (VitePress-only, .md and .vue, MPA only, bundling, plain module). No claims removed.

Method: docs-only read of cited pages, 2026-11-08
