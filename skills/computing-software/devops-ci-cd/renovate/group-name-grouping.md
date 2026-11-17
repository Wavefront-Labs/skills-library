---
id: computing-software.devops-ci-cd.renovate.group-name-grouping
name: group-name-grouping
category: computing-software
field: devops-ci-cd
product: renovate
tags: [group-name, grouping, monorepos, renovate]
level: practitioner
status: docs-checked
description: "Reduce PR noise by grouping related dependency updates into one branch with groupName, and when not to group."
sources:
  - https://docs.renovatebot.com/noise-reduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Setting `groupName` to a non-null string in a `packageRules` entry puts every matching update into one branch and PR. The name is free text with no special meaning. Internally Renovate uses the same mechanism for branches like "Pin Dependencies" and "Lock File Maintenance".

```json
{
  "packageRules": [
    {
      "matchPackageNames": ["/eslint/"],
      "groupName": "eslint"
    },
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "groupName": "devDependencies (non-major)"
    }
  ]
}
```

The default `:app` and `:library` style presets include `group:monorepos`, so packages from a known monorepo such as Angular or React already arrive together.

Grouping has costs, which the docs list plainly:

- A bigger group is more likely to break the build.
- It takes longer to find which package broke it.
- One failing member blocks every other update in the PR.
- A major bump in one member holds back the rest.

Use `groupSlug` to control the branch name (by default it is the slugified `groupName`) and `groupSingleUpdates` (default `false`) to apply group settings even when the group holds one update. `minimumGroupSize` (default 1) postpones branch creation until at least that many updates are available. Replacement updates are never grouped, and lock file maintenance is never grouped with other updates.

## Checked

2026-11-03. Confirmed against the Renovate Noise Reduction page (`group:monorepos` in `:app` and `:library`, the grouping trade-offs) and the configuration options page (`groupName`, `groupSlug`, `groupSingleUpdates`, `minimumGroupSize`). Removed the padded closing advice and renamed the example group to the documented one.

Method: documentation only; no commands were run.
