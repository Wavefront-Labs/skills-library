---
id: computing-software.devops-ci-cd.forgejo.differences-from-github-actions
name: differences-from-github-actions
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [github-actions-compatibility, workflow-differences, enable-openid-connect, runner-default-image]
level: practitioner
status: docs-checked
description: "Plan GitHub workflow migration around Forgejo's familiarity-not-compatibility policy and its known differences."
sources:
  - https://forgejo.org/docs/latest/user/actions/github-actions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo Actions aims for familiarity, not compatibility: many GitHub Actions features translate one to one, but small differences mean 100% compatibility is not claimed, and workflows should work with minimal changes. Forgejo also has things GitHub lacks, such as running workflows in LXC containers.

The documented, possibly incomplete, list of differences:

- The default environment differs greatly. Most Forgejo Runners use a Debian bookworm image with just Node.js, while GitHub uses a larger Ubuntu image.
- Some keys in the `github` context are missing.
- Some subkeys of a job are ignored, such as `permissions` and `continue-on-error`.
- OIDC ID token generation is enabled with the `enable-openid-connect` key in the workflow file, not with `permissions: id-token: write`.

## Checked

2026-11-04. Confirmed against the Forgejo Actions GitHub Actions comparison page: the familiarity-not-compatibility policy, LXC as a Forgejo-only feature, and all four listed differences. Removed: the closing practical-steps paragraph, which the page does not contain.

Method: documentation only; no commands were run.
