---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-secret-filters
name: woodpecker-secret-filters
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [secret-events, plugin-filter, pull-request-secrets]
level: advanced
status: docs-checked
description: "Restrict Woodpecker secrets by pipeline event and by plugin image."
sources:
  - https://woodpecker-ci.org/docs/usage/secrets
  - https://woodpecker-ci.org/docs/usage/security-boundaries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker secret event and plugin filters

Events filter: by default secrets are not exposed to pull requests. You can enable the `pull_request` event on a secret in the UI or CLI. This is risky on public repositories that accept pull requests from anyone, because malicious actors could expose or transfer the secrets. Enabling `pull_request` gives the secret to everybody who can open a pull request that runs without approval.

Plugins filter: restrict a secret to a list of plugin images. Then no other step can read it. Plugins cannot run arbitrary commands, so they are less able to reveal secrets.

- If you specify a tag, the filter takes it into account.
- If the same image appears several times, the least privileged entry wins; an image without a tag allows all tags even if another entry has a tag.

A secret limited to plugins is passed only if the step really is a plugin. A step is a plugin only if it sets none of `commands`, `entrypoint` and `environment`.

Secrets from a secret extension that carry no `events` are passed to all events.

By default a CLI-created secret is available to all images for `push`, `tag` and `deployment` events, not for `pull_request`.

## Checked

2026-11-08. Read the Woodpecker Secrets page and the Security boundaries page in full and confirmed the event filter, plugin filter, tag rule, plugin definition, secret extension rule and CLI defaults. Removed the advice to combine plugin filters with project approval settings, which neither page states.

Method: documentation only; no commands were run.
