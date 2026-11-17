---
id: computing-software.devops-ci-cd.renovate.dependency-dashboard
name: dependency-dashboard
category: computing-software
field: devops-ci-cd
product: renovate
tags: [dependency-dashboard, dashboard-issue, deprecated-packages, renovate]
level: practitioner
status: docs-checked
description: "Enable the Renovate Dependency Dashboard issue to see pending, closed and deprecated updates in one place."
sources:
  - https://docs.renovatebot.com/key-concepts/dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Dependency Dashboard is a repository issue maintained by Renovate that summarises the state of every dependency update. It needs a platform that supports issues with dynamic Markdown checkboxes.

Enable it with the preset or the option:

```json
{
  "extends": ["config:recommended", ":dependencyDashboard"]
}
```

or `"dependencyDashboard": true`. To switch it off, use `:disableDependencyDashboard` or set the option to `false`.

What the dashboard gives you:

- Warnings for packages their registry marks deprecated, with a column saying whether a community replacement is available.
- Abandonment detection through the `abandonments:recommended` preset (included in `config:best-practices`), which sets an `abandonmentThreshold` of one year and carries community overrides.
- A Closed/Ignored section listing updates you closed, with a checkbox to get a new PR.
- Checkbox-driven approval for updates you gate with `dependencyDashboardApproval`.

Related options include `dependencyDashboardTitle`, `dependencyDashboardLabels`, `dependencyDashboardHeader`, `dependencyDashboardFooter` and `dependencyDashboardAutoclose` (closes the issue when there are no more updates).

## Checked

2026-11-03. Confirmed against the Renovate Dependency Dashboard key-concepts page (platform requirement, enable and disable presets, deprecation warnings, `abandonments:recommended`, Closed/Ignored section, approval) and the configuration options page (the `dependencyDashboard*` options). Removed the unsupported rate-limited and awaiting-schedule bullet.

Method: documentation only; no commands were run.
