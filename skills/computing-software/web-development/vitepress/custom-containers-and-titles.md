---
id: computing-software.web-development.vitepress.custom-containers-and-titles
name: custom-containers-and-titles
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, custom-containers, info-tip-warning-danger, details, container-title, callouts]
level: practitioner
status: docs-checked
description: "Use ::: containers (info, tip, warning, danger, details) with default and custom titles, and localize container labels globally."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Containers are fenced with `:::` and a type.

```md
::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details
This is a details block.
:::
```

**Custom title:** put it after the type: `::: danger STOP` or `::: details Click me to toggle the code`.

**Global label override** (useful for non-English sites) in site config:

```ts
export default defineConfig({
  markdown: {
    container: {
      tipLabel: '提示',
      warningLabel: '警告',
      dangerLabel: '危险',
      infoLabel: '信息',
      detailsLabel: '详细信息'
    }
  }
})
```

On multilingual sites the same labels can be overridden per locale under `locales.<code>.markdown.container`.

**Attributes.** `::: details Title {open}` makes a details block open by default; `::: tip {no-title}` removes the title element (has no effect on `details`, which always needs its summary). Attributes come from `@mdit/plugin-attrs` and work on most Markdown elements.

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Custom Containers: default and custom titles, markdown.container labels, Additional Attributes with open and no-title) and the i18n guide (Per-locale Markdown Strings). Removed: the usage guidance paragraph and the Verify step.

Method: documentation only; no commands were run.
