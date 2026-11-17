---
id: computing-software.web-development.wordpress.style-variations-and-global-styles
name: style-variations-and-global-styles
category: computing-software
field: web-development
product: wordpress
tags: [style-variations, global-styles, theme-json, block-themes, wordpress]
level: practitioner
status: docs-checked
description: "Block theme style variations and global styles: styles/*.json variations, colour and typography presets, section styles, Site Editor customisations, export."
sources:
  - https://github.com/WordPress/gutenberg/blob/trunk/docs/reference-guides/theme-json-reference/theme-json-living.md
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/class-wp-theme-json-resolver.php
  - https://github.com/WordPress/wordpress-develop/blob/trunk/src/wp-includes/global-styles-and-settings.php
  - https://developer.wordpress.org/themes/global-settings-and-styles/style-variations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style variations and global styles

## 1. The layers
Global styles merge in this order (`WP_Theme_JSON_Resolver::get_merged_data`): core defaults, block data, theme `theme.json`, then **user data** saved from the Site Editor in a `wp_global_styles` post. Later layers win. A style variation chosen in the Site Editor is saved as user data, so it overrides the theme's base `theme.json`.

## 2. Theme style variations
Files in `styles/` override parts of `theme.json`:
```json
// styles/midnight.json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "title": "Midnight",
  "settings": { "color": { "palette": [
    { "slug": "base", "color": "#0b1020", "name": "Base" },
    { "slug": "contrast", "color": "#f5f7ff", "name": "Contrast" },
    { "slug": "accent", "color": "#8ab4ff", "name": "Accent" } ] } },
  "styles": { "color": { "background": "var(--wp--preset--color--base)", "text": "var(--wp--preset--color--contrast)" } }
}
```
- Keep preset **slugs identical** across variations (base, contrast, accent) so content using `has-accent-color` classes adapts when users switch.
- A `styles/*.json` file with a `blockTypes` property is a block style variation partial: its styles are scoped to the listed block types (for example `"blockTypes": ["core/group"]`). Core registers these from the theme's `styles` directory since WordPress 6.6.0; files without `blockTypes` are theme-scope style variations.

## 3. Global styles in the Site Editor
Users edit colours, typography and spacing per site and per block in the Site Editor Styles panel. Changes save to the database (a `wp_global_styles` post), not the theme files.
- User customisations are merged after the theme, so they override `theme.json`; reset user styles if a theme update seems to "not apply".
- Lock options for clients: `settings.color.custom: false` and `settings.typography.customFontSize: false` stop users choosing custom colours and font sizes (both default to true). `settings.appearanceTools` is the opt-in switch for a group of design tools; see its reference entry.

## 4. Fonts
Register presets in `settings.typography.fontFamilies` (each entry has `name`, `slug`, `fontFamily` and optional `fontFace`). Variations can swap families by slug.

## 5. Debugging
CSS custom properties (`--wp--preset--color--accent`) in DevTools show resolved values; `wp_get_global_settings()` / `wp_get_global_styles()` in PHP return merged results (`wp_get_global_stylesheet()` returns the generated CSS).

## Verify
- [ ] Switching variations restyles all templates without broken colours; slugs consistent; user customisations exportable to theme files.

## Checked

2026-10-25: against the Gutenberg trunk theme.json version 3 reference (works with WordPress 6.6 or later) and wordpress-develop trunk source (`class-wp-theme-json-resolver.php`, `global-styles-and-settings.php`), last commits 2026-10-25. Confirmed: merge order and the `wp_global_styles` post type, `blockTypes` partial scoping and the 6.6.0 registration of block style variations from the `styles` directory, `settings.color.custom` and `settings.typography.customFontSize` defaults, `fontFamilies` entry shape, `wp_get_global_settings`/`wp_get_global_styles`. Removed unconfirmed claims: colour-only and typography-only partial pickers, Font Library 6.5 gate, Create Block Theme plugin steps, export menu paths, `file:` font sources and the exact Site Editor menu path.

Method: documentation only; no commands were run.
