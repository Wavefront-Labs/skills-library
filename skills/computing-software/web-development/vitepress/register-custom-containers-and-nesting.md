---
id: computing-software.web-development.vitepress.register-custom-containers-and-nesting
name: register-custom-containers-and-nesting
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, customcontainers, nested-containers, container-fence, css-variables, success-container, code-group-nesting]
level: advanced
status: docs-checked
description: "Register new container names with customContainers, style them via .custom-block classes, and nest containers using longer fences."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/i18n.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Registering new containers.** Map names to default titles:

```ts
export default defineConfig({
  markdown: {
    container: {
      customContainers: { success: 'SUCCESS' }
    }
  }
})
```

Then use `::: success`, with custom titles and attributes, and the GitHub alert syntax `> [!SUCCESS] Custom title`. New containers ship **without styling**: add CSS in your theme, using the container name as a class.

```css
/* .vitepress/theme/custom.css */
.custom-block.success {
  border-color: transparent;
  color: var(--vp-c-text-1);
  background-color: var(--vp-c-success-soft);
}
```

The default palette already provides `--vp-c-success-soft`.

**Nesting.** `:::` markers follow fenced-code rules: a fence closes only on a matching fence at least as long as the opener. So make the outer fence longer:

```md
:::: info Outer container
This box contains another container.

::: details Inner container
Content
:::
::::
```

The same trick lets you nest containers around `::: code-group` blocks.

**Per-locale titles.** Locale entries may override titles of containers registered at root level only; registering new containers per locale is unsupported, and since the renderer is created once, locale markdown strings must be in the main config file, not additional configs.

Verify: the new container renders with your colours in light and dark mode.

## Checked

Read the Registering New Containers and Nesting sections of the markdown guide and the Per-locale Markdown Strings section of the i18n guide. Confirmed `customContainers`, the unstyled default, the `.custom-block.success` CSS with `--vp-c-success-soft`, the longer-fence nesting rule with code groups, and the root-level-only and main-config-only locale limits. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
