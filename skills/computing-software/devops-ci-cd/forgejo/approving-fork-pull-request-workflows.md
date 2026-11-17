---
id: computing-software.devops-ci-cd.forgejo.approving-fork-pull-request-workflows
name: approving-fork-pull-request-workflows
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [workflow-approval, approve-once, approve-always, trust-management]
level: practitioner
status: docs-checked
description: "Approve or deny workflow runs from fork pull requests and manage trust per author."
sources:
  - https://forgejo.org/docs/latest/user/actions/security-pull-request/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pull request can change what Actions runs, for instance by editing a file in `.forgejo/workflows`. When it comes from a fork of a public repository on an instance with open registration, the author might be malicious, so the workflows of such pull requests must be approved before they run. Users with elevated permissions approve or deny them on the pull request conversation page.

Trust is granted or denied per pull request author:

- Approve once lets all currently pending workflows run. Later workflows, for example after a new commit on the same pull request, need another manual approval.
- Approve always trusts the author to run workflows on this repository from then on.

Trust can be revoked at any time. The page for each blocked workflow run links to the pull request's trust management area.

Who needs approval: users who only have read access to the repository need approval before workflows from their pull requests can run.

The administrator security guide (Preventing Arbitrary Workflow Execution) describes the same gate more loosely: a fork author's first pull request needs review and approval before workflows run, and after that future pull requests have their workflows executed, including modifications made in the fork. It also notes that `on: pull_request` workflows have no access to the repository secrets. The user page above is the more precise description, with Approve once covering only the pending workflows.

## Checked

2026-11-04. Confirmed against the Forgejo Actions Security of Pull Requests page: why approval is needed, where elevated users approve, Approve once versus Approve always, revocation, the trust management link and the read-only-access rule. The closing paragraph is confirmed by the administrator security guide, whose wording differs from the user page, and the skill now says so.

Method: documentation only; no commands were run.
