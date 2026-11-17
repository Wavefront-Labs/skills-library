---
id: computing-software.devops-ci-cd.gitlab-runner.runner-autoscaler-connector
name: runner-autoscaler-connector
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [connector-config, autoscaler, ssh, keepalive, use-external-addr]
level: sme
status: docs-checked
description: "How the autoscaler connects to instances via [runners.autoscaler.connector_config]."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autoscaler connector configuration

`[runners.autoscaler.connector_config]` controls how the runner manager reaches each instance.

Options documented include:
- `keepalive`: the connection keepalive duration.
- `timeout`: the connection timeout duration.
- `use_external_addr`: whether to use the external address provided by the plugin; default `false`. If the plugin returns only an internal address, that address is used regardless.

Other settings depend on the fleeting plugin.

## Checked

2026-11-03. Confirmed against keepalive, timeout and use_external_addr on Advanced configuration. Removed unsourced advice.

Method: documentation only; no commands were run.
