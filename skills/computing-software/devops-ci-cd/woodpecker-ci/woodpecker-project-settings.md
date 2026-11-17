---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-project-settings
name: woodpecker-project-settings
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [project-settings, approval, visibility]
level: practitioner
status: docs-checked
description: "Configure Woodpecker repository settings: pipeline path, hooks, approvals, visibility, timeout."
sources: ["https://woodpecker-ci.org/docs/usage/project-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker project settings

Repository admins on the forge get admin permissions in Woodpecker and can change these settings.

- Pipeline path: empty by default, resolving `.woodpecker/*.{yaml,yml}`, then `.woodpecker.yaml`, then `.woodpecker.yml`. A custom path must exist or loading fails. For multiple workflows use a folder path ending in `/`.
- Repository hooks: choose which webhooks trigger pipelines.
- Allow pull requests: if disabled, pull request webhooks start no pipelines.
- Allow deployments: lets a pipeline start with the `deploy` event from a successful pipeline. Enable only if you trust everyone with push access, because they could steal secrets limited to `deploy` events.
- Require approval for: holds a pipeline until approved. The default is `Approvals for forked repositories`.
- Trusted: grants escalated capabilities such as volumes. Only server admins can set it.
- Custom trusted clone plugins: images that receive netrc Git credentials, on top of `WOODPECKER_PLUGINS_TRUSTED_CLONE`.
- Project visibility: `Public` (everyone), `Internal` (authenticated users) or `Private` (owners only). Settings, secrets and registries are visible to owners only.
- Timeout: a pipeline must finish within it or is treated as timed out.
- Cancel previous pipelines: cancels earlier pipelines of the same event and context when a new one starts.

## Checked

2026-11-03. Confirmed against: project-settings (all listed settings, defaults, visibility values, trusted). Removed: an unsupported closing line about WOODPECKER_DEFAULT_* server defaults.

Method: documentation only; no commands were run.
