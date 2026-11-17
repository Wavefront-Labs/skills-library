---
id: computing-software.web-development.biome.assist-config-actions-and-presets
name: assist-config-actions-and-presets
category: computing-software
field: web-development
product: biome
tags: [biome, assist-config, assist-actions, source-group, usesortedkeys, organizeimports, preset, action-options]
level: practitioner
status: docs-checked
description: "Configure assist: enabled, includes, presets, the source group and individual actions with level and options such as useSortedKeys."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`assist` holds `enabled` (default true), `includes` (can only narrow `files.includes`; `[]` selects none) and `actions`.

**Presets.** `assist.actions.preset` is `"recommended"` (default), `"all"` or `"none"`; `assist.actions.recommended` (default true) is the older boolean. Group presets and explicit action settings override the global preset, so an action can be enabled while the preset is `none`.

**Groups.** `source` contains source-level actions such as organizing imports and sorting supported declarations; they can be exposed as editor source actions and checked or applied by the CLI. A group takes `preset`, `recommended` and action keys. The group `preset` wins over group `recommended`.

**Actions.** Each action is `"on"`, `"off"`, or `{ level, options }` where `options` depend on the action. An explicit action setting beats group and global presets.

```json
{ "assist": { "actions": { "source": {
  "useSortedKeys": { "level": "on", "options": { "sortOrder": "natural" } }
} } } }
```

To switch assist off for all files use `"assist": { "enabled": false }`; per language use `<language>.assist.enabled`.

The options each action supports are documented under the assist section, along with source-rule origins.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
