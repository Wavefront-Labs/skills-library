---
id: computing-software.devops-ci-cd.forgejo.pull-request-token-and-pull-request-target
name: pull-request-token-and-pull-request-target
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [pull-request-target, pull-request-event, workflow-token-permissions, fork-pull-requests]
level: advanced
status: docs-checked
description: "Compare the read-only token of pull_request workflows with pull_request_target running in the base context."
sources:
  - https://forgejo.org/docs/latest/user/actions/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workflows triggered by the `pull_request` event are an exception to the normal token rules. The token generated for them has no write permission on the repository, because a pull request is unverified and may contain an untested or malicious workflow.

`pull_request_target` is the alternative. It runs in the context of the base of the pull request, not the incoming commits, so the proposed changes are not available to the workflow. You therefore cannot use it to check the incoming changes. Since no untrusted code reaches the runner, the token restrictions are lifted and the workflow can write to the repository, for example to change labels or add comments.

The administrator security guide warns about the trade-off: a repository with an `on: pull_request_target` workflow stops an attacker modifying the executed code until their pull request is merged, but such workflows have access to secrets and can still make mistakes when interacting with the pull request's code.

The Security page says a `pull_request_target` workflow cannot be used to check incoming changes, and gives changing labels or placing comments as examples of what it can do.

## Checked

2026-11-04. Confirmed against the Forgejo Actions Security page (Pull requests and pull_request_target) and the administrator guide section Preventing Arbitrary Workflow Execution for the secrets trade-off. Replaced the closing rule of thumb with what the page says.

Method: documentation only; no commands were run.
