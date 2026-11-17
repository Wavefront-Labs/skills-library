---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.dependency-update-and-licence-drift
name: dependency-update-and-licence-drift
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [dependency-update-and-licence-drift, software-composition-analysis, licence drift, dependabot, renovate, licence change detection, dependency review, github dependency review, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Detect licence changes in new dependency versions with automated update PRs and alerts before merging."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency updates and licence drift monitoring

Goal: catch licence changes at upgrade time.

Method:
- Enable Dependabot version updates (a dependabot.yml checked into the repo opens automated PRs for outdated dependencies), or an equivalent tool; add a CI job running actions/dependency-review-action, which fails PRs that introduce licences outside allow-licenses. Its deny-licenses option is deprecated for possible removal, so prefer allow-licenses.
- Use GitHub dependency review on the PR (Files changed tab) to see added, removed and updated dependencies, including indirect ones from lock files.
- Maintain a lock file; review transitive additions.
- Alert on relicensing events of critical packages (monitor project announcements).
- Pin or fork when licence changes are unacceptable.
- Record dates when a version was adopted for historical reasoning.

Gotchas:
- Check the licence of every updated version, not only major bumps.
- Monorepos produce huge diffs; focus on added or changed licences.

Verify: dependency-review check fails on a test PR adding a licence outside allow-licenses.

## Checked

2026-11-08. Confirmed in the dependency-review-action README: allow-licenses fails PRs introducing licences not on the list; deny-licenses is deprecated for possible removal; the action raises an error for vulnerabilities or invalid licences introduced by a PR. Confirmed in GitHub docs: Dependabot version updates open PRs to keep dependencies updated and are enabled with dependabot.yml; dependency review shows added, removed and updated dependencies and indirect changes from lock files. Removed: Renovate-specific claim, ecosyste.ms and deps.dev, and the patch-release relicensing anecdote (not in the pages read).

Method: documentation only; no commands were run.
