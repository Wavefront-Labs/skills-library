---
id: computing-software.web-development.biome.html-super-languages-vue-svelte-astro-opt-in
name: html-super-languages-vue-svelte-astro-opt-in
category: computing-software
field: web-development
product: biome
tags: [biome, vue, svelte, astro, html, experimental-full-support, html-formatter, overrides, mixed-indentation]
level: advanced
status: docs-checked
description: "Enable experimental Biome support for HTML, Vue, Svelte and Astro, handle false positives with overrides, and avoid mixed indent settings."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/introduction/language-support.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v2.3.0 Biome formats and lints the HTML, CSS and JavaScript parts of Vue, Svelte and Astro files. Support is **experimental**. v2.4.0 added much better language-specific syntax support (for example Svelte control flow like `{#if}{/if}`), enough for most Svelte 5 projects but not rare syntax. Cross-language lint rules work a bit better since v2.5.0 but may produce false positives.

Because full support is experimental, enable it explicitly, and the formatter separately:

```json
{
  "html": {
    "experimentalFullSupportEnabled": true,
    "formatter": { "enabled": true }
  }
}
```

**Without full support** (`html.experimentalFullSupportEnabled` false) while linting `.svelte`, `.astro`, `.vue`, turn off rules that give false positives from partial support, via `overrides`:

```json
{
  "overrides": [{
    "includes": ["**/*.svelte", "**/*.astro", "**/*.vue"],
    "linter": { "rules": {
      "style": { "useConst": "off", "useImportType": "off" },
      "correctness": { "noUnusedVariables": "off", "noUnusedImports": "off" }
    } }
  }]
}
```

**Mixed settings trap.** Since one file can contain several languages, per-language options can disagree. If `javascript.format.indentStyle` is `tab` while `css.format.indentStyle` is `space` with `indentWidth` 4, an HTML-like file may end up mixing tabs and spaces. The docs track this in a GitHub discussion and advise using the playground to check whether a feature has landed.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the advice to keep indent options aligned and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
