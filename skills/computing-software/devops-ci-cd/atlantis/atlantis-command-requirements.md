---
id: computing-software.devops-ci-cd.atlantis.atlantis-command-requirements
name: atlantis-command-requirements
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [approved, mergeable, undiverged, apply-requirements, plan-requirements, import-requirements]
level: advanced
status: docs-checked
description: "Gate plan, apply, import and state rm on approved, mergeable and undiverged requirements, with per-VCS semantics."
sources: ["https://www.runatlantis.io/docs/command-requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis command requirements

Requirements are checked before `atlantis apply`, `import` and `state rm` (and, if set, `plan`). `state rm` must satisfy both `apply_requirements` and `import_requirements`; there is no `state_rm_requirements`.

Set them in `repos.yaml` (`plan_requirements`, `apply_requirements`, `import_requirements`) and let repos override via `allowed_overrides` so `atlantis.yaml` can set per-directory values, for example `staging` with `[]` and `production` with `[mergeable]`. Server flags that set the same requirement override both files.

- `approved`: at least one person other than the author approved. GitHub: any user with read access can approve; Atlantis uses each reviewer's latest approve or request-changes review and ignores comment-only reviews. GitLab: approvers set in repo settings. Bitbucket Cloud: self-approval does not count. Approval is checked when `apply` runs, not relative to the latest plan, so enable dismiss-stale-reviews or `--discard-approval-on-plan` (GitHub, GitLab).
- `mergeable`: the PR can be merged. GitHub with protected branches also enforces status checks, CODEOWNERS and up-to-date branches; if `atlantis/apply` is a required check use `--gh-allow-mergeable-bypass-apply`. Bitbucket and Azure DevOps only check conflicts.
- `undiverged`: blocks apply if the base branch changed since the last plan; meaningful only with the `merge` checkout strategy. If `autoplan.when_modified` is set, only matching changes count.

Once requirements pass, anyone who can comment can run `atlantis apply`.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Command Requirements. Removed or fixed: fixed: `--checkout-strategy` is not a requirements flag; the page says flags that set requirements override the files.

Method: documentation only; no commands were run.
