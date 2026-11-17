---
id: computing-software.devops-ci-cd.renovate.abandoned-packages
name: abandoned-packages
category: computing-software
field: devops-ci-cd
product: renovate
tags: [abandonment-threshold, abandoned, deprecated-packages, renovate]
level: practitioner
status: docs-checked
description: "Flag packages with no recent releases using abandonmentThreshold and the abandonments:recommended preset."
sources:
  - https://docs.renovatebot.com/configuration-options/#abandonmentthreshold
  - https://docs.renovatebot.com/key-concepts/dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`abandonmentThreshold` marks a package as abandoned when it has had no new release for a set time. Renovate sets `isAbandoned` on the lookup result when the threshold is defined and the datasource provides a `mostRecentTimestamp`, the release date of the highest version (counted only if that version also has the newest timestamp, so normal release patterns drive the result). If the latest release date plus the threshold is in the past, the package is abandoned.

The value is a duration string such as `1 year`, `6 months` or `90 days`:

```json
{
  "abandonmentThreshold": "2 years",
  "dependencyDashboardReportAbandonment": true
}
```

The preset `abandonments:recommended`, included in `config:best-practices`, sets a threshold of one year includes community-sourced overrides for packages that look abandoned but are still maintained, and prevents updates to truly abandoned packages while allowing updates to packages with irregular release schedules. Contribute overrides by editing the `abandonments.json` data file in the Renovate repository.

Abandoned packages are listed in a collapsible section of the Dependency Dashboard; `dependencyDashboardReportAbandonment` is enabled by default and set to `false` hides them. The option works inside `packageRules`, for example with `matchDatasources` set to `["npm"]` to apply a threshold to one datasource.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`abandonmentThreshold`, `isAbandoned`, `mostRecentTimestamp`, duration strings, packageRules example, `dependencyDashboardReportAbandonment`) and the Dependency Dashboard key-concepts page (`abandonments:recommended`, one-year default, community overrides, `config:best-practices`, `abandonments.json`). Removed: advice to treat the flag as a replacement prompt, and the claim that abandoned packages are listed prominently.

Method: documentation only; no commands were run.
