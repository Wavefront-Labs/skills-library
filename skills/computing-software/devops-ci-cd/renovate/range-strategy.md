---
id: computing-software.devops-ci-cd.renovate.range-strategy
name: range-strategy
category: computing-software
field: devops-ci-cd
product: renovate
tags: [range-strategy, pin, widen, renovate]
level: practitioner
status: docs-checked
description: "Control how Renovate rewrites version ranges with rangeStrategy values auto, pin, bump, replace, widen and update-lockfile."
sources:
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`rangeStrategy` decides what Renovate does to the declared range when it proposes an update:

- `auto`: Renovate decides per manager.
- `pin`: convert ranges to exact versions, `^1.0.0` to `1.1.0`.
- `bump`: raise the range even if the new version satisfies it, `^1.0.0` to `^1.1.0`.
- `replace`: replace the range only when the new version falls outside it.
- `widen`: extend the range, `^1.0.0` to `^1.0.0 || ^2.0.0`.
- `update-lockfile`: update the lock file for in-range updates, otherwise replace; supported for bundler, cargo, composer, gleam, npm, yarn, pnpm, terraform, poetry and uv.
- `in-range-only`: update the lock file for in-range updates and ignore package file updates.

```json
{
  "packageRules": [
    {
      "matchDepTypes": ["devDependencies"],
      "rangeStrategy": "pin"
    }
  ]
}
```

The default is `auto`. For npm, `auto` widens `peerDependencies`; widens a range that already ends in an or-operator (`^1.0.0 || ^2.0.0` becomes `^1.0.0 || ^2.0.0 || ^3.0.0`); otherwise replaces an out-of-range range, so `^2.0.0` becomes `^3.0.0`; and for in-range updates updates the lock file with the new exact version.

Renovate will not deliberately narrow a range: with `^1.0.0` and 1.2.0 latest it changes nothing, because 1.2.0 satisfies the range. Set `bump` if you want `^1.2.0`. Only caret (`^`) and tilde (`~`) ranges are supported. The docs recommend avoiding `in-range-only` unless strictly needed, because you may fall multiple releases behind without knowing.

## Checked

2026-11-09: read the rangeStrategy section of https://docs.renovatebot.com/configuration-options/ in full. Behaviour list matched; removed the sentence attributed to the dependency pinning docs (page not read) and added the default, `auto` details and caveats.

Method: documentation only; no commands were run.
