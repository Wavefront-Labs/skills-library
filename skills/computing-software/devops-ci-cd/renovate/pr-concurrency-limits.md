---
id: computing-software.devops-ci-cd.renovate.pr-concurrency-limits
name: pr-concurrency-limits
category: computing-software
field: devops-ci-cd
product: renovate
tags: [pr-concurrent-limit, pr-hourly-limit, branch-concurrent-limit, renovate]
level: practitioner
status: docs-checked
description: "Throttle Renovate with prConcurrentLimit, prHourlyLimit and branchConcurrentLimit, especially while onboarding."
sources:
  - https://docs.renovatebot.com/configuration-options/#prhourlylimit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three options cap how much work Renovate opens at once:

- `prConcurrentLimit` limits open PRs per repository. `branchConcurrentLimit` limits branches; if unset it inherits `prConcurrentLimit`, which defaults to 10. Many repositories work better with 3 or 5. You can allow more branches than PRs, such as `branchConcurrentLimit` 5 and `prConcurrentLimit` 3.
- `prHourlyLimit` limits how many PRs are created in each clock hour (`:00` to `:59`).
- `commitHourlyLimit` does the same for commits.

```json
{
  "prHourlyLimit": 2,
  "prConcurrentLimit": 5,
  "branchConcurrentLimit": 3
}
```

Why it matters: after you merge the onboarding and "Pin Dependencies" PRs, Renovate may create every pending update at once, overwhelming CI, and each merge rebases the others and triggers more test runs. An hourly limit of 1 or 2 spreads the work over a day or so.

Security PRs are exempt: Renovate always creates PRs with `[SECURITY]` in the title even when the concurrent limit is reached.

Leaving limits unlimited or high slows processing, especially rebasing out-of-date branches, so lower `branchConcurrentLimit` when runs are slow. The defaults are 2 for `prHourlyLimit` and 10 for `prConcurrentLimit`; `0` means no limit, and the limits are enforced per repository.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`prConcurrentLimit`, `branchConcurrentLimit`, `prHourlyLimit`, `commitHourlyLimit`, onboarding rationale, security PR exemption). Nothing removed.

Method: documentation only; no commands were run.
