---
id: computing-software.web-development.biome.html-vue-svelte-astro-options-reference
name: html-vue-svelte-astro-options-reference
category: computing-software
field: web-development
product: biome
tags: [biome, html-config, experimentalfullsupportenabled, whitespacesensitivity, selfclosevoidelements, indentscriptandstyle, html-parser-vue, interpolation]
level: advanced
status: docs-checked
description: "Reference for html options: full-support switch, legacy handling, Vue and interpolation parsing, whitespace sensitivity, void elements, script indentation."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTML support and its formatter are experimental, and bug fixes may change output.

- `html.experimentalFullSupportEnabled` (default false): full parsing of `.html`, `.vue`, `.svelte`, `.astro`. When false, `.vue`, `.svelte` and `.astro` use **legacy handling**: only the JavaScript/TypeScript parts are extracted, the rest left unchanged. It does not enable the formatter.
- `html.formatter.enabled` (default true, but formatting whole HTML/Vue/Svelte/Astro files also requires full support to be true).
- `html.parser.interpolation` (false): parse `{{ expression }}` in `.html` files.
- `html.parser.vue` (false): parse Vue syntax such as `v-if` and `v-bind` in `.html` files; also turns on interpolation. `.vue` files are recognised automatically, and this does not change how `.vue`, `.svelte` or `.astro` parse.
- `html.formatter.whitespaceSensitivity`: `css` (default; whitespace significant for elements that are inline by default), `strict` (significant for every element; existing whitespace kept as at least one character, none added), `ignore` (insignificant; use only when it cannot change rendering).
- `html.formatter.indentScriptAndStyle` (false): indent `<script>`/`<style>` content one level.
- `html.formatter.selfCloseVoidElements`: `never` (default; `<img src="image.png">`) or `always` (`<img src="image.png" />`).
- `html.formatter.attributePosition` (`auto` or `multiline`) and `bracketSameLine` (false; also affects self-closing HTML elements), plus indentStyle, indentWidth, lineEnding, lineWidth.
- `html.formatter.trailingNewline` (true) does **not** inherit `formatter.trailingNewline`, unlike the other languages.
- `html.linter.enabled` and `html.assist.enabled` default to true.

Typical opt-in: `{ "html": { "experimentalFullSupportEnabled": true, "formatter": { "enabled": true } } }`.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
