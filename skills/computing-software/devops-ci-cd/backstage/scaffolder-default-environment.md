---
id: computing-software.devops-ci-cd.backstage.scaffolder-default-environment
name: scaffolder-default-environment
category: computing-software
field: devops-ci-cd
product: backstage
tags: [default-environment, template-secrets, environment-secrets, backstage]
level: advanced
status: docs-checked
description: "Provide shared parameters and secrets to all templates using scaffolder.defaultEnvironment."
sources:
  - https://backstage.io/docs/features/software-templates/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`scaffolder.defaultEnvironment` supplies default parameters and secrets to every template, so each template need not ask for them.

```yaml
scaffolder:
  defaultEnvironment:
    parameters:
      region: eu-west-1
    secrets:
      AWS_ACCESS_KEY: ${AWS_ACCESS_KEY}
```

Use them in template steps:

```yaml
steps:
  - id: deploy
    action: acme:deploy
    input:
      region: ${{ environment.parameters.region }}
      accessKey: ${{ environment.secrets.AWS_ACCESS_KEY }}
```

- Default parameters are available through `environment.parameters.*`.
- Default secrets are resolved from environment variables and are available through `environment.secrets.*` inside template actions.
- Default secrets are only available during action execution, not in frontend forms; default parameters live in their own `environment` context to avoid naming conflicts.

The docs state the point as reducing template complexity and improving security by centralizing common values. Per-user credentials, for example an OAuth token for the signed-in user, use the separate `secretsKey` option of `requestUserCredentials` on the repository picker.

## Checked

2026-11-03. Confirmed against the Backstage scaffolder Configuration and Writing Templates pages: `defaultEnvironment` keys, `environment.parameters.*` and `environment.secrets.*`, env-var resolution, `secretsKey`. Removed: the run-log claim and the secret-store and access-restriction advice (not in the pages).

Method: documentation only; no commands were run.
