---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-plugin-security
name: woodpecker-plugin-security
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [plugin-security, untrusted-input, trusted-clone]
level: sme
status: docs-checked
description: "Design Woodpecker plugins that safely hold secrets, privileged mode or Git credentials."
sources:
  - https://woodpecker-ci.org/docs/usage/plugins/creating-plugins
  - https://woodpecker-ci.org/docs/usage/security-boundaries
  - https://woodpecker-ci.org/docs/administration/configuration/server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker plugin security

A plugin is just a step running your image; it is not secure on its own. It can, however, get extra trust: secrets limited to it by the plugins filter, privileged mode (via `WOODPECKER_PLUGINS_PRIVILEGED`) and Git credentials as a trusted clone plugin.

Everyone who can change the workflow, for example through a pull request, controls the plugin's settings and the workspace. A plugin that receives such trust must treat both as untrusted input:

- No settings that run commands or scripts.
- No settings loaded from files in the workspace.
- Never print secrets.
- Placeholders in settings are fine only if they cannot reach a secret. Remove your secret settings (for example `PLUGIN_TOKEN`) from the environment before replacing placeholders, or allow only a fixed list of names.

If your plugin is not designed for this, say so in its documentation.

Operator side:

- A step counts as a plugin only if it sets none of `commands`, `entrypoint` and `environment`. The linter rejects `commands` and `entrypoint` next to `settings` but only warns about `environment`.
- List privileged and trusted clone images with their tags, because tags enforce exact matches.
- `WOODPECKER_PLUGINS_TRUSTED_CLONE` controls which images receive Git credentials during clone.

## Checked

2026-11-08. Read the Creating plugins page and the Security boundaries page in full, and the `PLUGINS_PRIVILEGED` and `PLUGINS_TRUSTED_CLONE` entries of the Woodpecker server configuration page. All claims were confirmed; nothing was removed.

Method: documentation only; no commands were run.
