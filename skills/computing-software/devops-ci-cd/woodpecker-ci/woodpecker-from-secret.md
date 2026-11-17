---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-from-secret
name: woodpecker-from-secret
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [secrets, from-secret, environment]
level: intro
status: docs-checked
description: "Pass Woodpecker secrets into environment variables and plugin settings with from_secret."
sources:
  - https://woodpecker-ci.org/docs/usage/secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker secrets with from_secret

Woodpecker stores named secrets centrally and passes them to steps with the `from_secret` keyword.

Into an environment variable:

```yaml
steps:
  - name: step name
    image: registry/repo/image:tag
    commands:
      - echo "The secret is $TOKEN_ENV"
    environment:
      TOKEN_ENV:
        from_secret: secret_token
```

Into a plugin setting:

```yaml
steps:
  - name: step name
    image: registry/repo/image:tag
    settings:
      TOKEN:
        from_secret: secret_token
```

The setting `TOKEN` reaches the plugin as the environment variable `PLUGIN_TOKEN`.

Expressions in the config are preprocessed before the pipeline starts. If you reference a secret variable inside a command, escape the dollar sign with `$$` so it is expanded at runtime rather than during preprocessing:

```yaml
commands:
  - echo $${TOKEN_ENV}
```

Woodpecker masks secrets from its own store in logs but cannot mask secrets fetched from external providers inside steps, so those can appear in pipeline logs.

By default secrets are not exposed to pull requests. Enable the `pull_request` event on a secret only after reading the secret filters skill, and consider restricting the secret to plugin images so ordinary steps cannot read it.

## Checked

2026-11-08. Read the Woodpecker Secrets page (woodpecker-ci.org/docs/usage/secrets) in full and confirmed the `from_secret` examples, `PLUGIN_TOKEN`, `$$` escaping, masking of external secrets, the pull request default and the plugins filter. Removed the claim about exact name matching, which the page does not state.

Method: documentation only; no commands were run.
