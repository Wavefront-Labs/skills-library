---
id: computing-software.web-development.biome.v2-linter-severity-style-rules-and-all-removal
name: v2-linter-severity-style-rules-and-all-removal
category: computing-software
field: web-development
product: biome
tags: [biome, upgrade-v2, severity, recommended-rules, style-group, rules-all-removed, linter-domains, package-json-format]
level: advanced
status: docs-checked
description: "Adapt to v2 linter behaviour: default severities, style rules not erroring, the removed all option, and expanded package.json formatting."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/upgrade-to-biome-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Linter now works like other linters.** In v1, recommended rules emitted errors only and non-recommended rules were enabled manually with a chosen severity. In v2 every rule has a default severity suggested by Biome, recommended rules can emit diagnostics of different severity, and you may keep the default severity or choose your own. If you relied on recommended rules always erroring, `biome migrate` sets those rules to `"error"`.

**`style` rules do not emit errors anymore** unless configured. Feedback said the recommended set was balanced badly (some found defaults noisy). Migration updates configs so rules you had enabled still error; check the result matches your standards.

**The linter option `all` was removed.** With more than 300 rules, some conflict with each other (one fix triggers another rule and vice versa). It may return later in another form (discussion on Discord and GitHub issue 5764). Limited workaround: recommended on plus all domains on, noting you cannot disable single rules and that the `react` and `solid` domains enable rules that conflict:

```json
{
  "linter": {
    "domains": { "next": "all", "react": "all", "test": "all", "solid": "all", "project": "all" },
    "rules": { "recommended": true }
  }
}
```

**`package.json` formatting changed.** Objects and arrays are always multi-line regardless of width. To keep the compact style add an override:

```json
{ "overrides": [{ "includes": ["package.json"], "json": { "formatter": { "expand": "auto" } } }] }
```

## Checked

2026-11-08. Read the upgrade-to-biome-v2 page in full. Unchanged: default severities, migrate setting error, style rules not erroring, removal of all with the domains workaround, issue 5764, and the package.json expand override. Removed: the invented Verify step.

Method: documentation only; no commands were run.
