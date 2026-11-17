---
id: computing-software.devops-ci-cd.github-actions.dependabot-yml-groups-and-schedules
name: dependabot-yml-groups-and-schedules
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, dependency-pinning, dependabot, dependabot-config, dependabot-groups, dependabot-yml, version-updates, security-updates, schedule, open-pull-requests-limit, ignore-rules, cooldown, multi-ecosystem, private-registries]
level: practitioner
status: docs-checked
description: "Write a dependabot.yml that teams can live with: ecosystems and directories, schedules, groups to cut PR noise, ignore rules, cooldown, limits, and security update grouping."
sources: ["https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference", "https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates", "https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dependabot.yml: groups and schedules

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directories: ["/", "/packages/*"]        # glob support; `directory` for a single path
    schedule:
      interval: weekly                        # daily | weekly | monthly | quarterly | semiannually | yearly | cron (with cronjob)
      day: monday
      time: "06:00"
      timezone: Europe/London
    open-pull-requests-limit: 10              # default 5; 0 disables version updates
    cooldown:                                 # wait before proposing fresh releases
      default-days: 3
      semver-major-days: 14
    groups:
      dev-dependencies:
        dependency-type: development
        update-types: [minor, patch]
      aws-sdk:
        patterns: ["@aws-sdk/*"]
      production-minor-patch:
        dependency-type: production
        update-types: [minor, patch]
        exclude-patterns: ["react*"]
    ignore:
      - dependency-name: "typescript"
        update-types: ["version-update:semver-major"]
    labels: [dependencies]
    commit-message: { prefix: "chore(deps)", include: scope }

  - package-ecosystem: github-actions
    directory: "/"                             # scans .github/workflows
    schedule: { interval: monthly }
    groups:
      actions: { patterns: ["*"] }

  - package-ecosystem: docker
    directory: "/"
    schedule: { interval: weekly }
```

## Groups
- A dependency goes into the **first** group it matches; unmatched ones get individual PRs.
- Majors usually stay ungrouped (each needs its own review); group minor/patch.
- `applies-to: security-updates` on a group makes **security** PRs grouped too
  (default groups apply to version updates).

## Security vs version updates
- `open-pull-requests-limit` (default 5) caps open **version update** PRs; `0` disables version updates
  for that ecosystem. Security update PRs have a separate fixed limit of 10 open PRs.
- `cooldown` applies to version updates only, not security updates; without a `cooldown` block Dependabot still applies a 3-day default cooldown to version updates.
- `semver-*-days` cooldown keys work only for package managers that support SemVer.

## Private registries
```yaml
registries:
  npm-internal:
    type: npm-registry
    url: https://npm.pkg.github.com
    token: ${{ secrets.DEPENDABOT_NPM_TOKEN }}
updates:
  - package-ecosystem: npm
    directory: "/"
    registries: [npm-internal]
    schedule: { interval: weekly }
```

## Gotchas
- `directories` supports globbing and `*`; the single `directory` key does not.
- For `github-actions`, use `/`: Dependabot searches `/.github/workflows` and the root `action.yml`/`action.yaml`.
- If a dependency matches more than one group rule, it joins the first group that matches.

## Verify
The next scheduled run opens one grouped PR per group instead of one per package.

## Checked

2026-10-31. Confirmed against the GitHub Dependabot options reference: schedule.interval values (daily, weekly, monthly, quarterly, semiannually, yearly, cron), day, time, timezone and cronjob keys, directories globbing versus directory, open-pull-requests-limit default 5 and zero disabling version updates, the separate fixed limit of 10 for security updates, cooldown (version updates only, 3-day default, default-days and semver-*-days keys), group keys (applies-to, dependency-type, patterns, exclude-patterns, update-types), first-matching-group rule, ignore update-types values, commit-message prefix and include, the github-actions directory rule, npm-registry registry type and the secrets syntax.
Removed: the @dependabot comment commands, the claim that security updates ignore schedule, the Insights error path, the Dependabot-PR restricted-token claim and the Renovate comparison.

Method: documentation only; no commands were run.
