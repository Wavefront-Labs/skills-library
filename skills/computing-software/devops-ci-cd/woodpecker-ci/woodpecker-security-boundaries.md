---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-security-boundaries
name: woodpecker-security-boundaries
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [security, trust-model, approval, trusted-repositories]
level: sme
status: docs-checked
description: "Understand what Woodpecker trusts the forge with and what each trust level allows."
sources:
  - https://woodpecker-ci.org/docs/usage/security-boundaries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker security boundaries

Woodpecker trusts what the forge reports: who a user is, their permissions (read, push, admin), and webhook data such as event, author and whether a pull request is from a fork.

Permissions: instance admins (from `WOODPECKER_ADMIN`) administer every org and repository. Users with push access can start, restart, cancel and approve pipelines and manage crons; read access allows viewing pipelines and logs. Permissions are cached for up to an hour.

Webhooks: each repository gets a random secret; the webhook URL carries a non-expiring signed token that does not cover the body. Keep the URL private. If leaked, use Repair repository in the settings to rotate the secret.

Approval: pull requests from forks wait for approval by default. Manual pipelines, crons, restarts and deployments never need approval. An approved pipeline runs the configuration it was created with but gets current secrets and the approver's Git credentials.

Workflow files come from the commit being built, so pull request authors control them when they run without approval.

Trusted repositories, set only by instance admins:

- Network: `dns`, `dns_search`, `extra_hosts`, `network_mode`
- Volumes: `volumes`, `devices`, `tmpfs`
- Security: `privileged` and Git credentials in every step

Only enable these for people you trust; they can compromise agent hosts. The local backend has no isolation at all.

## Checked

2026-11-08. Read the Woodpecker Security boundaries page in full and confirmed every claim; nothing was removed.

Method: documentation only; no commands were run.
