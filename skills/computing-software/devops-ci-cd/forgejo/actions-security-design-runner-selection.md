---
id: computing-software.devops-ci-cd.forgejo.actions-security-design-runner-selection
name: actions-security-design-runner-selection
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-security, runner-selection, runner-pool, secret-redaction]
level: practitioner
status: docs-checked
description: "Understand which runners may pick up a workflow, how the per-run token is scoped, and how isolation differs by runner type."
sources:
  - https://forgejo.org/docs/latest/user/actions/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo Actions has two parts: the Forgejo server, which holds repositories and hands out runs, and the Forgejo Runner, which executes them. When a workflow triggers, the runner is chosen from a pool of three groups: runners registered instance-wide by administrators, runners registered to the user or organization that owns the repository, and runners registered to that specific repository. A workflow is never executed by a runner outside these groups.

The automatic token can read the repositories associated with the workflow, even private ones, and is destroyed at the end. It works only for the repository it was created for; use on other repositories returns a 404.

Isolation by runner kind: Docker, Podman and LXC runners create a new container per workflow, which isolates the host and other containers, but a misconfigured environment could let a workflow escape and compromise the runner and later runs. Host runners have no real isolation; folders are cleaned after a run, but escape is trivial.

Secrets are stored encrypted in the database and the runner tries to redact them from logs.

Advice from the page: never trust a shared host runner, and the safest option is hosting your own runner for trusted repositories. Do not print secrets to output.

## Checked

2026-11-04. Confirmed against the Forgejo Actions Security page: the three runner groups, the automatic token scope and 404, container versus host runner isolation, secret storage and redaction, and the security considerations. Nothing removed.

Method: documentation only; no commands were run.
