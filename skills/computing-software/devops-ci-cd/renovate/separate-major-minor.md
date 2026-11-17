---
id: computing-software.devops-ci-cd.renovate.separate-major-minor
name: separate-major-minor
category: computing-software
field: devops-ci-cd
product: renovate
tags: [separate-major-minor, update-types, major-updates, renovate]
level: practitioner
status: docs-checked
description: "How Renovate splits major from minor PRs, and how closing a PR ignores a major line."
sources:
  - https://docs.renovatebot.com/configuration-options/#separatemajorminor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default `separateMajorMinor` is `true`: when both a minor and a major update exist, Renovate opens separate branches. If you use Webpack 2.0.0 and both 2.1.0 and 3.0.0 exist, you get one PR for 2.x and one for 3.x, and can accept the safe one first.

The docs recommend leaving it on. If you apply the 2.x update, Renovate keeps updating the 3.x branch with later 3.x releases. If you apply 3.0.0, it deletes the unneeded 2.x branch next run. If you do not want major 3 for a long time, close the "Update Webpack to version 3.x" PR and it will not be recreated even if 3.x releases continue, while 2.x patches still arrive.

Related options:

- `separateMinorPatch` splits minor and patch updates into different PRs.
- `separateMultipleMajor` creates a PR for each intermediate major, such as v2 and v3, instead of jumping to the latest.
- `separateMultipleMinor` does the same for minors.

```json
{
  "separateMinorPatch": true,
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

`matchUpdateTypes` accepts values such as `major`, `minor`, `patch`, `pin` and `digest` to apply rules per update type. `separateMajorMinor` has priority over groups from `packageRules`, so set it to `false` inside the rule to force a grouped update. `separateMinorPatch` and `separateMultipleMajor` default to `false`.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`separateMajorMinor` default and behaviour, Webpack example, `separateMinorPatch`, `separateMultipleMajor`, `separateMultipleMinor`, `matchUpdateTypes` values). Removed the unsupported schedule, labels and automerge policy remark.

Method: documentation only; no commands were run.
