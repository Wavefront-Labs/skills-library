---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-secret-scopes
name: woodpecker-secret-scopes
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [secret-scopes, global-secrets, priority]
level: practitioner
status: docs-checked
description: "Understand Woodpecker repository, organization and global secret scopes and their priority."
sources:
  - https://woodpecker-ci.org/docs/usage/secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker secret scopes

Secrets exist at three scopes. When the same name is defined at several scopes, the highest priority wins:

1. Repository secrets, available to all pipelines of that repository.
2. Organization secrets, available to all pipelines of the organization.
3. Global secrets, set only by instance administrators and available to pipelines of the entire Woodpecker instance, so use them with caution.

So a repository secret named `deploy_token` overrides an organization or global secret of the same name.

External providers can also be used by calling them from within pipeline steps, with access configured through Woodpecker secrets.

Secrets can be managed in the UI or with `woodpecker-cli`.

Limit exposure with the event and plugin filters described in the secret filters skill.

## Checked

2026-11-08. Read the Woodpecker Secrets page (woodpecker-ci.org/docs/usage/secrets) in full and confirmed the three scopes, their priority order, global secrets being admin-only, external providers and UI or CLI management. Removed the secret-extension merge claim, the `WOODPECKER_DISABLE_USER_AGENT_REGISTRATION` rationale and the database note, which that page does not state.

Method: documentation only; no commands were run.
