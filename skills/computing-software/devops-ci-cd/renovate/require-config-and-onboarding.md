---
id: computing-software.devops-ci-cd.renovate.require-config-and-onboarding
name: require-config-and-onboarding
category: computing-software
field: devops-ci-cd
product: renovate
tags: [require-config, onboarding-config, no-config-repos, renovate]
level: advanced
status: docs-checked
description: "Decide whether repositories need a config file with requireConfig and onboarding global options."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`requireConfig` says whether a repository needs a Renovate config file:

- `"required"` (default): a file must exist before Renovate proposes updates.
- `"optional"`: use a file if present, otherwise run with defaults.
- `"ignored"`: ignore repository config files entirely.

It works together with `onboarding` (default `true`). Docs table summary:

- `required` with `onboarding=true`: an onboarding PR is created if no config file exists; if that PR is closed and there is still no config, the repository is skipped.
- `required` with `onboarding=false`: the repository is skipped unless a config file is added manually.
- `optional` with `onboarding=true`: an onboarding PR is created if no config exists; if it is closed and there is no config, the repository is processed.
- `optional` with `onboarding=false`: the repository is processed regardless of config file presence.
- `ignored`: with `onboarding=true` no onboarding PR is created; either way the repository is processed and any config file is ignored.

Set `onboarding` to `false` only if all three hold: you configure Renovate entirely on the admin side, you want it on every repository it can access, and you want to skip all onboarding PRs.

```json
{
  "onboarding": false,
  "requireConfig": "optional",
  "extends": ["config:recommended"]
}
```

With `"ignored"`, config files in the repository have no effect. `inheritConfig` (default `false`) offers a gentler route: before processing a repository Renovate reads `inheritConfigFileName` (default `org-inherited-config.json`) from `inheritConfigRepoName` (default `{{parentOrg}}/renovate-config`) as config. If the inherited file is missing, Renovate proceeds without warning (unless `inheritConfigStrict` is `true`); if it exists but cannot be parsed, it raises a config warning issue and aborts that job.

## Checked

2026-11-09: read the requireConfig, onboarding and inheritConfig, inheritConfigFileName, inheritConfigRepoName and inheritConfigStrict sections of https://docs.renovatebot.com/self-hosted-configuration/. Corrected the inherited file and repository defaults and expanded the requireConfig and onboarding table; removed the unsourced "organisation-wide policy" claim.

Method: documentation only; no commands were run.
