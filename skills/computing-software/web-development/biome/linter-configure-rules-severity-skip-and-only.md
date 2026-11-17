---
id: computing-software.web-development.biome.linter-configure-rules-severity-skip-and-only
name: linter-configure-rules-severity-skip-and-only
category: computing-software
field: web-development
product: biome
tags: [biome, rule-severity, disable-rule, error-on-warnings, skip-flag, only-flag, group-severity, rule-options, recommended-false]
level: practitioner
status: docs-checked
description: "Turn rules off, set on/info/warn/error at rule or group level, pass options, and use biome lint --skip and --only for ad hoc runs."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Disable a rule:** `"suspicious": { "noDebugger": "off" }`. **Disable all recommended rules:** `"linter": { "rules": { "recommended": false } }` (useful when you only want to enable a few rules).

**Severity.** Each rule has a default severity. `"on"` applies it; for instance `noShoutyConstants` is not recommended and emits information-level diagnostics when on. Override with `"error"`, `"warn"` or `"info"`:
- `error` always makes the CLI exit with an error code, useful to block CI.
- `warn` does not fail the CLI unless `--error-on-warnings` is passed, useful to keep CI green while violations remain.
- `info` never affects the exit code, even with `--error-on-warnings`.

**Group severity.** A group can take a level: `"a11y": "off"` turns off every accessibility rule, e.g. for backend code.

**Rule options.** A rule with options takes an object with `level` and `options`:

```json
{ "linter": { "rules": { "style": { "useNamingConvention": {
  "level": "error", "options": { "strictCase": false } } } } } }
```

**CLI selectors.**
- `biome lint --skip=style --skip=suspicious/noExplicitAny` skips the whole `style` group and one rule.
- `biome lint --only=style/useNamingConvention --only=style/noInferrableTypes --only=a11y` runs only those. If a selected rule is disabled in configuration, its severity becomes `error` for a recommended rule and `warn` otherwise.

## Checked

2026-11-08. Read the linter index page in full. Unchanged: off, on and severity levels with exit-code behaviour, group severity, rule options, --skip and --only. Removed: a pointer to a preset key that this page does not cover, and the invented Verify step.

Method: documentation only; no commands were run.
