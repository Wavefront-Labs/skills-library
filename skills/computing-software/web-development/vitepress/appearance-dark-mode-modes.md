---
id: computing-software.web-development.vitepress.appearance-dark-mode-modes
name: appearance-dark-mode-modes
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, appearance, dark-mode, force-dark, force-auto, vitepress-theme-appearance, usedark, flicker]
level: practitioner
status: docs-checked
description: "Control dark mode with the appearance option: true, 'dark', false, 'force-dark', 'force-auto', or UseDarkOptions, and avoid flicker."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `appearance` site option sets how the `.dark` class is applied to `<html>`. Type: `boolean | 'dark' | 'force-dark' | 'force-auto' | UseDarkOptions` (from `@vueuse/core`); default `true`.

- `true`: follow the user's preferred colour scheme and show the toggle.
- `'dark'`: dark by default unless the user toggles it.
- `false`: no toggle, users cannot change the theme.
- `'force-dark'`: always dark, no toggle.
- `'force-auto'`: always follows the OS preference, no toggle.

```ts
export default defineConfig({ appearance: 'dark' })
```

The option injects an inline script that restores the saved setting from local storage under the `vitepress-theme-appearance` key before rendering, so the `.dark` class is applied early and the page does not flicker. With the object form, `appearance.initialValue` can only be `'dark'` or `undefined`; refs and getters are not supported.

Read the live state from the runtime API: `const { isDark } = useData()`. Dark-specific CSS can target the `.dark` class on `<html>`.

Mobile menu text for the switch is `darkModeSwitchLabel` in themeConfig; the view-transition animation for toggling is covered in the global components and overrides skill.

## Checked

2026-11-04. Confirmed against the VitePress site-config page (appearance: type, default, each mode, vitepress-theme-appearance storage key, initialValue limit), the runtime-api page (useData returns isDark) and the default-theme-config page (darkModeSwitchLabel is shown in mobile view only). Removed: the invented CSS colour example and the Verify step.

Method: documentation only; no commands were run.
