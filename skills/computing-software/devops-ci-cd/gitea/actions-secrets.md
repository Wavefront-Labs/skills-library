---
id: computing-software.devops-ci-cd.gitea.actions-secrets
name: actions-secrets
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-secrets, gitea, secrets-context, secret-naming-rules, secret-precedence, gitea-token]
level: practitioner
status: docs-checked
description: "Create Gitea Actions secrets at user, organization or repository level, follow the naming rules, use them as secrets.NAME and know which level wins on a clash."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/actions/secrets.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Actions secrets

Secrets hold sensitive values for a user, an organization or a repository. They exist from Gitea 1.19 and are only visible from 1.20 when Actions are enabled. Read them in workflows as `${{ secrets.SECRET_NAME }}`.

## Naming rules
- Only letters, digits and underscores; no spaces.
- Must not start with `GITHUB_` or `GITEA_`.
- Must not start with a number.
- Not case-sensitive.
- Unique at the level they are created at: a repository secret needs a unique name inside that repository, an organization secret inside that organization.

## Precedence
When the same name exists at several levels, the lowest level wins, so a repository secret overrides an organization one. Use this to let an organization provide a default and one repository override it.

## Related
The built-in `GITEA_TOKEN` is also exposed as `secrets.GITEA_TOKEN`; its rights are controlled separately (see `gitea-actions-token-permissions`). Variables for non-sensitive values live in `vars` (see `gitea-actions-variables`).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
