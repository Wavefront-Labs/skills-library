---
id: computing-software.web-development.ghost.ghost-theme-custom-settings
name: ghost-theme-custom-settings
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, custom-settings, package-json, custom-object, handlebars]
level: advanced
status: docs-checked
description: "Define Ghost theme custom settings in package.json config.custom: five types, groups, descriptions and the 20 setting limit."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/custom-settings.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let site owners configure a theme from Ghost Admin.

Declare settings in `package.json` under `config.custom`. Five types: `select`, `boolean`, `color`, `image`, `text`. Read them in templates via `@custom`, for example `{{#if @custom.cta_text}}{{@custom.cta_text}}{{/if}}`. A theme may define at most 20 custom settings.

Keys: lowercase, no special characters, snake_case. The key becomes the display name (`cta_text` shows as CTA Text) and the property on `@custom`. Renaming a key in a new theme version is a breaking change: the old setting and its value are removed and a new one starts at the default.

Groups: settings appear on the Theme tab of Design and branding under Site wide (default), Homepage or Post. Use the optional `"group": "homepage"` or `"post"`.

Description: optional, fewer than 100 characters.

Type rules: `select` needs `options` (array of strings) and a `default` that matches one option, and is used with the `match` helper; `boolean` needs `default` true or false and works with `{{#if}}`; `color` needs a `default` that is a valid hexadecimal string; `image` does not allow a `default` (output is blank or a URL, and works with `img_url`); `text` has an optional `default` and may be blank, so wrap output in `{{#if}}`. An unknown `type` causes a theme validation error.

Fallbacks: put the default text in `package.json`, not as a template fallback; only add an `{{else}}` fallback when the theme must have text for that setting.

Visibility: add `"visibility": "header_style:[Landing, Search]"` (NQL syntax, as in the get helper) to show a setting only when its parent has those values. When the condition is not met, the setting renders as null in the theme.

Custom fonts: when a user selects fonts, `{{ghost_head}}` loads them and sets CSS variables `--gh-font-heading` and `--gh-font-body`; selected font names are also added to `{{body_class}}`, such as `gh-font-heading-fira-mono`. Fallback form: `var(--gh-font-body, Helvetica)`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 475 lines, code samples inline, no imported snippets): themes/custom-settings.mdx. Overview, key, group, description and select/boolean rules match. Removed the invented Verify step. Added color, image and text rules, fallbacks, visibility and custom fonts from the page.
Method: documentation only; no commands were run.
