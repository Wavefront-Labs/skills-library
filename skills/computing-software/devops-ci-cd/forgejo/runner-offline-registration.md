---
id: computing-software.devops-ci-cd.forgejo.runner-offline-registration
name: runner-offline-registration
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [offline-registration, forgejo-cli-actions-register, runner-secret, ephemeral-runner]
level: advanced
status: docs-checked
description: "Register runners from infrastructure code with a pre-generated 40-character secret and the forgejo-cli actions register command."
sources:
  - https://forgejo.org/docs/latest/admin/actions/registration/
  - https://forgejo.org/docs/latest/admin/actions/security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Offline registration suits Infrastructure as Code (Ansible, Kubernetes), where one tool generates a secret and shares it with Forgejo and the runner. It needs system administrator access, so it is not available on hosted services such as Codeberg.

Generate a 40-character hexadecimal string, then on the Forgejo machine:

`forgejo forgejo-cli actions register --name runner-name --scope myorganization --secret 7c31591e8b67225a116d4a4519ea8e507e08f71f`

The command prints the runner UUID. Put the instance `url`, that `uuid` and the secret as `token` into the runner's `server.connections` configuration.

The secret has two parts: the first 16 characters identify the runner and the remaining 24 are the secret value. Run the command again with the same first 16 characters and a new tail to update an existing runner's secret.

Runner modes: persistent (default) runners handle many jobs; ephemeral runners run at most one job before Forgejo deletes them, enabled with `--ephemeral` at registration (also an `ephemeral` property in the HTTP API). Forgejo enforces it. Ephemeral runners can only use `forgejo-runner one-job` (stated on the security page).

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Runner Registration" page, read in full including its code blocks: the Infrastructure as Code use case, the system administrator requirement (not applicable to hosted services such as Codeberg), the 40-character hexadecimal secret, the `forgejo forgejo-cli actions register --name ... --scope ... --secret ...` example, the printed UUID, the `server.connections` url/uuid/token layout, the 16-character identifier plus 24-character secret split and the update-by-rerun procedure, and the persistent/ephemeral runner modes with `--ephemeral` and the HTTP API `ephemeral` property. The `forgejo-runner one-job` restriction for ephemeral runners was confirmed on the "Securing Forgejo Actions Deployments" page (read in full), which is now listed in `sources`.
Corrected: added the second source for the `one-job` claim; nothing else needed changing.
Method: documentation only; no commands were run.
