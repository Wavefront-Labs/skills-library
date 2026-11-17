---
id: computing-software.devops-ci-cd.forgejo.actions-secrets-scopes
name: actions-secrets-scopes
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-secrets, secrets-key, org-secrets, encrypted-secrets]
level: practitioner
status: docs-checked
description: "Define encrypted workflow secrets at repository, user or organization level and read them as secrets.KEY."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A repository, user or organization can hold secrets: key/value pairs stored encrypted in the Forgejo database and exposed to workflows as `${{ secrets.KEY }}`. Define them in the web interface at:

- `/org/{org}/settings/actions/secrets` for every repository of the organization
- `/user/settings/actions/secrets` for every repository of the logged-in user
- `/{owner}/{repo}/settings/actions/secrets` for a single repository's workflows

Once a secret is added, its value cannot be changed or displayed.

Usage in a step is `${{ secrets.KEY }}`. The automatic token is also reachable through `secrets.FORGEJO_TOKEN`.

Compare with variables: after a variable is added its value can be modified, while a secret's value cannot. The workflow token is also readable as `secrets.FORGEJO_TOKEN`, and for compatibility with GitHub workflows `secrets.GITHUB_TOKEN` is the same value.

## Checked

2026-11-04. Confirmed against the Forgejo Actions basic concepts page (Secrets, Custom variables, Automatic token): the three settings paths, encrypted storage, the value being unchangeable, and the token aliases. Removed: the claim that a secret must be set again to change it, and the advice on repository versus owner level, neither stated on the page.

Method: documentation only; no commands were run.
