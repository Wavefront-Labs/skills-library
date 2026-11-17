---
id: computing-software.web-development.node-express.dependabot-and-renovate
name: dependabot-and-renovate
category: computing-software
field: web-development
product: node-express
tags: [vulnerable-dependencies, dependabot, renovate, dependency-updates, supply-chain, ci]
level: practitioner
status: docs-checked
description: "Automating dependency updates with Dependabot or Renovate: grouping, schedules, automerge for safe updates, security-only PRs, monorepo config and keeping PR noise manageable."
sources:
  - https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
  - https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/automate-dependabot-with-actions
  - https://docs.renovatebot.com/configuration-options/
  - https://docs.renovatebot.com/key-concepts/automerge/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependabot and Renovate

## 1. Dependabot (GitHub native)
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule: { interval: weekly, day: monday }
    open-pull-requests-limit: 10
    groups:
      dev-deps: { dependency-type: development, update-types: [minor, patch] }
      prod-minor: { dependency-type: production, update-types: [minor, patch] }
    ignore:
      - dependency-name: "react"
        update-types: ["version-update:semver-major"]
  - package-ecosystem: github-actions
    directory: "/"
    schedule: { interval: monthly }
```
Security updates are separate from version updates: `allow` update-types and `open-pull-requests-limit` do not apply to them, and they have their own fixed limit of 10 open PRs. Dependabot also applies a default 3 day `cooldown` to version updates (not security updates); set `cooldown` to change it. Automerge via a workflow using `dependabot/fetch-metadata` + `gh pr merge --auto` for patch updates.

## 2. Renovate (more control, any forge)
```json
{
  "extends": ["config:recommended", ":semanticCommits", "group:monorepos"],
  "schedule": ["before 6am on monday"],
  "minimumReleaseAge": "3 days",
  "packageRules": [
    { "matchUpdateTypes": ["patch", "minor"], "matchDepTypes": ["devDependencies"], "automerge": true },
    { "matchPackageNames": ["eslint", "/^@typescript-eslint/"], "groupName": "lint" },
    { "matchUpdateTypes": ["major"], "dependencyDashboardApproval": true }
  ],
  "lockFileMaintenance": { "enabled": true, "schedule": ["before 6am on the first day of the month"] }
}
```
Dependency Dashboard issue tracks everything pending. `minimumReleaseAge` delays brand-new versions (supply-chain buffer).

## 3. Operating rules
- Automerge only with branch protection + required CI checks that actually exercise the code (tests, build, type-check).
- Group related packages (framework + its plugins) so they move together.
- Pin GitHub Actions to commit SHAs (`uses: actions/checkout@<sha> # v4`); Renovate can pin them with the `helpers:pinGitHubActionDigests` preset.
- Assign an owner/rotation; an ignored bot queue is worse than none.
- Majors: read changelogs, schedule them; do not let them rot for years.

## Verify
Weekly PR count stays manageable (<10 open); dashboards show no updates older than a month except approved majors; security PRs merge within your SLA.

## Checked

2026-10-25 against the GitHub Docs Dependabot options reference (github/docs, commit of 2026-10-23) and the Renovate docs and presets source (renovatebot/renovate, main). Confirmed: Dependabot group update-types values are minor, patch and major, and ignore uses version-update:semver-major; security update PRs have a separate fixed limit of 10 and are not governed by open-pull-requests-limit or allow update-types; Dependabot applies a default 3 day cooldown to version updates (not security updates) and cooldown is configurable; dependabot/fetch-metadata with gh pr merge --auto is the documented automerge pattern; Renovate options minimumReleaseAge, lockFileMaintenance, dependencyDashboardApproval, matchUpdateTypes, matchDepTypes, groupName, and presets config:recommended, :semanticCommits, group:monorepos and helpers:pinGitHubActionDigests exist.

Method: documentation only; no commands were run.
