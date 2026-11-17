---
id: computing-software.web-development.biome.linter-config-presets-groups-severity-fix
name: linter-config-presets-groups-severity-fix
category: computing-software
field: web-development
product: biome
tags: [biome, linter-config, rules-preset, rule-groups, severity, rule-options, fix-kind, safe-unsafe, biome-explain, domains]
level: advanced
status: docs-checked
description: "Configure linter rules: preset recommended/all/none, group-level and rule-level severity, rule options objects, fix safe/unsafe, and domains."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Linter object:** `enabled` (default true), `includes` (can only narrow `files.includes`), `domains`, `rules`.

**Presets.** `linter.rules.preset` is `"recommended"` (default, non-nursery recommended rules), `"all"` (all non-nursery rules) or `"none"`. `linter.rules.recommended` still works but is deprecated and will be removed next major version; run `biome migrate`. Precedence from weakest to strongest: global preset, group `preset`/`recommended` (preset wins if both), explicit rule setting. So with preset `none` you can still enable a single rule.

**Groups:** `a11y`, `complexity`, `correctness`, `nursery` (unstable, opt-in), `performance`, `security`, `style`, `suspicious`. A group takes a level string or an object with `preset`, `recommended` and rule keys. Levels: `off`, `on` (rule's default severity), `info`, `warn`, `error`.

```json
{ "linter": { "rules": { "a11y": "info" } } }
```

**A rule** takes a level string or an object `{ level, options?, fix? }`:

```json
{ "linter": { "rules": { "complexity": { "noExcessiveCognitiveComplexity": {
  "level": "warn", "options": { "maxAllowedComplexity": 15 } } } } } }
```

Run `biome explain <RULE>` for documentation and default severity.

**`fix`** (`none`, `safe`, `unsafe`) overrides how a rule's code fix is classified or emitted, for rules with a configurable fix. `none` emits no fix; `safe` lets `--write` apply it; `unsafe` applies only when unsafe fixes are enabled. It does not change the fix itself, so review before marking safe. Also valid inside `overrides`.

**`domains`** (`Record<string, "recommended" | "all" | "none">`) configures framework, project and type rules. Enabling `project` or `types` makes Biome scan project dependencies; `types` also enables type-aware resolution.

Verify: set `suspicious.noDoubleEquals` to `error` and run `biome lint`.

## Checked

2026-11-08. Read the linter section of the Biome configuration reference (linter through rules fix); the rest of that page was not read for this skill. Confirmed presets, deprecation of recommended, precedence, groups, levels, rule objects, fix values, domains and biome explain. Nothing removed.

Method: documentation only; no commands were run.
