---
id: computing-software.devops-ci-cd.renovate.labels-reviewers-assignees
name: labels-reviewers-assignees
category: computing-software
field: devops-ci-cd
product: renovate
tags: [labels, reviewers, assignees, renovate]
level: intro
status: docs-checked
description: "Add labels and route Renovate PRs to reviewers and assignees, including code owners and sampling."
sources:
  - https://docs.renovatebot.com/configuration-options/#labels
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default Renovate adds no labels. Define `labels` to add some; use `addLabels` to append labels instead of replacing, which is useful in package rules.

```json
{
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "addLabels": ["breaking"]
    }
  ],
  "reviewers": ["alice"],
  "assignees": ["alice"],
  "reviewersSampleSize": 1
}
```

- `reviewers` and `assignees` list valid usernames (or emails, depending on the platform). On Azure DevOps, prefix a reviewer with `required:` to make them required; on GitHub and Forgejo, assign a team with the `team:` prefix and the last part of the team name. Reviewers are added only when the PR is created, not modified afterwards.
- `labels` is non-mergeable (the last matching package rule wins); on Forgejo, Gitea, GitHub and GitLab Renovate keeps PR labels in sync unless another account changes them. Labels are usually truncated to 50 characters (255 on GitLab).
- `reviewersFromCodeOwners` and `assigneesFromCodeOwners` derive people from the CODEOWNERS file; `expandCodeOwnersGroups` expands group owners.
- `reviewersSampleSize` and `assigneesSampleSize` pick that many random people from the list.
- `additionalReviewers` appends to existing lists.
- `ignoreReviewers` lists accounts to exclude from the check described below.
- `filterUnavailableUsers` filters out unavailable users.

When automerge is on, Renovate does not add reviewers or assignees at PR creation, to reduce noise. If tests fail, it adds them, unless the PR already has some. Set `assignAutomerge` to add them always. `keepUpdatedLabel` and `stopUpdatingLabel` let humans control whether Renovate keeps touching a PR.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`labels`, `addLabels`, `reviewers`, `assignees`, `reviewersFromCodeOwners`, `reviewersSampleSize`, `additionalReviewers`, `ignoreReviewers`, `expandCodeOwnersGroups`, `filterUnavailableUsers`, `assignAutomerge`, `keepUpdatedLabel`, `stopUpdatingLabel`) and the Automerge key-concepts page. The reviewer name in the example is a placeholder. Nothing removed.

Method: documentation only; no commands were run.
