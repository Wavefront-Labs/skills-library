---
id: computing-software.devops-ci-cd.renovate.immortal-prs
name: immortal-prs
category: computing-software
field: devops-ci-cd
product: renovate
tags: [immortal-prs, closed-prs, pr-ignore, renovate]
level: practitioner
status: docs-checked
description: "Why closing some Renovate PRs does not stop them, and how Renovate matches closed PRs by branch name and title."
sources:
  - https://docs.renovatebot.com/key-concepts/pull-requests/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate keeps no database of PRs. It finds existing ones through the platform API, matching both the branch name (for example `renovate/lodash-4.x`) and the PR title (for example `Update lodash to v4.17.21`).

Ordinary PRs have a unique version in the title. When you close one, Renovate assumes you do not want that version, and only opens a new PR when a new unique title appears, such as lodash 4.17.22. For a major PR titled "Update lodash to v4", closing it means no more PRs for v4 at all.

An immortal PR shows a note that it will be recreated if closed unmerged. The branch name and title are a cache key: if a closed PR with the same key exists, Renovate ignores it, but that cannot work for a title with no unique version, such as a group PR titled "All non-major updates". Ignoring it would mean you never get a non-major update again, so Renovate recreates it.

How to avoid immortality:

- Use specific titles with a version, for example grouped PRs where a single version applies.
- Do not group updates whose versions differ if you want to be able to dismiss them.
- For immortal PRs you want to stay closed, set `"recreateWhen": "never"`.
- Set `"dependencyDashboardApproval": true` for major updates so you control when they are created.

The dependency dashboard lists closed updates so you can bring them back.

## Checked

2026-11-03. Confirmed against the Renovate Pull Requests key-concepts page (branch and title matching, normal and major PRs, immortal PRs, cache-key explanation, `recreateWhen`, `dependencyDashboardApproval`) and the Dependency Dashboard page (Closed/Ignored section). Removed the `ignoreDeps` and `allowedVersions` advice, which is not on the Pull Requests page.

Method: documentation only; no commands were run.
