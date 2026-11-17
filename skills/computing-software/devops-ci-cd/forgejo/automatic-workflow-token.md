---
id: computing-software.devops-ci-cd.forgejo.automatic-workflow-token
name: automatic-workflow-token
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [forgejo-token, github-token-alias, workflow-token, automatic-token]
level: practitioner
status: docs-checked
description: "Use the per-run automatic token as FORGEJO_TOKEN, forgejo.token or the GITHUB_TOKEN aliases."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
At the start of each workflow Forgejo creates a unique authentication token and destroys it when the workflow completes. It can read the repositories associated with the workflow, even private ones.

It is available as:

- the environment variable `FORGEJO_TOKEN` in every step
- `forgejo.token`
- `env.FORGEJO_TOKEN`
- `secrets.FORGEJO_TOKEN`

For reusing actions written for GitHub, aliases exist: `GITHUB_TOKEN` equals `FORGEJO_TOKEN`, `github.token` equals `forgejo.token`, and `env.GITHUB_TOKEN` equals `env.FORGEJO_TOKEN`.

The troubleshooting page covers a related pitfall: `actions/checkout` writes git credentials into the git config on the fly, and that automatic credential may be preferred over your own API key when you talk to other repositories. Setting `persist-credentials: false` in the checkout step avoids this.

The GitHub comparison page notes that the `permissions` job key is ignored in Forgejo workflows, so the token's reach is not tuned through it.

The token is created at the start of each workflow and destroyed when the workflow completes. Changes it authors never trigger further workflows, to avoid infinite recursion.

## Checked

2026-11-04. Confirmed against the Forgejo Actions basic concepts page (Automatic token), the Troubleshooting page (git credentials and persist-credentials) and the GitHub Actions comparison page (permissions key ignored). Nothing removed.

Method: documentation only; no commands were run.
