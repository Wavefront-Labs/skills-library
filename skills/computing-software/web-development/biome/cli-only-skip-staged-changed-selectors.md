---
id: computing-software.web-development.biome.cli-only-skip-staged-changed-selectors
name: cli-only-skip-staged-changed-selectors
category: computing-software
field: web-development
product: biome
tags: [biome, only-flag, skip-flag, staged, changed, since, plugin-group, domain-selector, ci-incremental]
level: practitioner
status: docs-checked
description: "Select what runs with --only and --skip (rule, group, domain, action, plugin) and limit files with --staged, --changed and --since."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`--only=<GROUP|RULE|DOMAIN|ACTION|PLUGIN>`** (check and ci; lint omits ACTION) runs only the named lint rule, assist action, group or domain. If a selected rule has severity `off`, Biome sets it to `error` for a recommended rule or `warn` otherwise. The pseudo-group `plugin` runs only analyzer plugins.

```shell
biome check --only=correctness/noUnusedVariables --only=suspicious --only=test --only=plugin
```

**`--skip=...`** skips the named items by setting matching lint rules to `off`; `--skip` **takes precedence over `--only`**. `--skip=plugin` skips analyzer plugins, and `--skip=project` skips the project domain.

**File selectors** (check, lint, format, ci):
- `--staged`: only staged files; intended for local use.
- `--changed`: only files with **committed** changes compared with `vcs.defaultBranch` or the ref from `--since`; staged and unstaged changes are not included; intended for CI.
- `--since=REF`: base reference for `--changed`, overriding `vcs.defaultBranch`; requires `--changed`.

```shell
biome check --changed --since=main
```

`--changed` needs VCS integration configured (`vcs.enabled`, `clientKind: git`) and either `defaultBranch` or `--since`, otherwise it fails (see the VCS configuration skill).

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the scanner-cost remark, the pre-commit remark and the 'Typical split' paragraph and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
