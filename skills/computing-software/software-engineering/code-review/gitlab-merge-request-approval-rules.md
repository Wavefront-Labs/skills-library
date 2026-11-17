---
id: computing-software.software-engineering.code-review.gitlab-merge-request-approval-rules
name: gitlab-merge-request-approval-rules
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, merge-request-approvals, gitlab, codeowners, approval-rules, protected-branches]
level: practitioner
status: draft
description: "Configure GitLab merge request approval rules: required approvals, eligible approvers, code owner sections, separation of duties settings and protected branch merge permissions."
sources: ["https://docs.gitlab.com/user/project/merge_requests/approvals/rules/", "https://docs.gitlab.com/user/project/merge_requests/approvals/settings/", "https://docs.gitlab.com/user/project/codeowners/", "https://docs.gitlab.com/user/project/repository/branches/protected/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GitLab merge request approval rules

Settings > Merge requests > **Merge request approvals** (multiple rules need Premium/Ultimate;
Free has optional approvals only).

## Rules
- **Approval rules**: name, required count, eligible approvers (users/groups), target branches
  (e.g. only `main` and `release/*`). Example: "Backend: 1 of @backend", "Security: 1 of
  @appsec for MRs to main".
- **Code Owners**: `CODEOWNERS` (in root, `docs/` or `.gitlab/`) plus protected branch option
  "Require approval from code owners". Sections with required counts:
  ```
  [Database][2] @dba-team
  db/migrations/
  ^[Docs] @tech-writers        # ^ = optional section
  docs/
  ```
- **Any approver** rule with count N for general review.
- Security policies (Ultimate): merge request approval policies that require security approval when
  scanners find new vulnerabilities or licences.

## Settings that matter (separation of duties)
- **Prevent approval by author**: authors can't approve their own MR.
- **Prevent approvals by users who add commits**: someone who pushed to the MR can't approve it.
- **Prevent editing approval rules in merge requests**: MR authors can't lower requirements.
- **Remove all approvals when commits are added** (or "remove approvals by Code Owners if their
  files changed"): new pushes reset approval.
- **Require user re-authentication to approve** (password/SAML) for regulated environments.

## Protected branches
Repository > Protected branches: who can merge/push (`Maintainers`, specific users, deploy keys),
"Allowed to force push" off, "Code owner approval" on. Combine with "Pipelines must succeed" and
"All threads must be resolved" in Merge request settings.

## API / as code
`POST /projects/:id/approval_rules`, the GitLab Terraform provider (`gitlab_project_approval_rule`,
`gitlab_branch_protection`) to manage rules consistently across many projects; group-level rules
for compliance.

## Verify
Open a test MR as a non-owner: approval widget shows required rules; merging is blocked until
satisfied; pushing a commit resets approvals as configured.
