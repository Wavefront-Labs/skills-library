---
id: computing-software.devops-ci-cd.renovate.dashboard-approval-workflow
name: dashboard-approval-workflow
category: computing-software
field: devops-ci-cd
product: renovate
tags: [dependency-dashboard-approval, approval, manual-approval, renovate]
level: practitioner
status: docs-checked
description: "Require a human tick on the Dependency Dashboard before Renovate creates a branch or PR for selected updates."
sources:
  - https://docs.renovatebot.com/configuration-options/#dependencydashboardapproval
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Set `dependencyDashboardApproval` to `true`, at the top level or inside `packageRules`, and Renovate waits for you to tick the update's checkbox on the Dependency Dashboard before it creates the branch or PR. Setting it automatically creates the dashboard issue, so you do not also need `dependencyDashboard`.

You can gate:

- all updates,
- major, minor or patch levels,
- named packages,
- updates from particular package managers.

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

The docs call dashboard approval far superior to disabling major updates, because pending updates stay visible on the dashboard instead of being invisible. Requiring approval for all updates is not recommended, since you must check the dashboard regularly. Vulnerability remediation PRs are still created immediately.

A related setting is `prCreation=approval`: Renovate creates branches immediately and CI runs, but the PR waits for dashboard approval. Other `prCreation` values are `immediate` (default), `not-pending` (wait for checks to finish) and `status-success` (only when tests pass). Do not use `prCreation=approval` together with `dependencyDashboardApproval=true`. With `not-pending` and no branch-level checks, PR creation relies on the `prNotPendingHours` fallback (default 25 hours), so avoid combining it with `rebaseWhen=never`, which can prevent PR creation altogether.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`dependencyDashboardApproval`, `prCreation` values and default, `prNotPendingHours`, `rebaseWhen`) and the Dependency Dashboard key-concepts page. Removed the unsupported "recommended way" claim.

Method: documentation only; no commands were run.
