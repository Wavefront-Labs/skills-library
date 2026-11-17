---
id: computing-software.devops-ci-cd.gitlab-runner.runner-autoscaler-state-storage
name: runner-autoscaler-state-storage
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [state-storage, autoscaler, beta, fleeting]
level: sme
status: docs-checked
description: "Persist autoscaler state so restarts do not discard fleeting instances (beta, 17.5)."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autoscaler state storage

`[runners.autoscaler.state_storage]` is beta, introduced in 17.5.

When state storage is disabled (the default) and the runner starts, existing fleeting instances are removed immediately for safety. The reason given: with `max_use_count = 1`, a job could otherwise be assigned to an instance that was already used.

Enable it when you do not want existing fleeting instances removed on runner restart.

## Checked

2026-11-03. Confirmed against beta status, 17.5 version and the restart behaviour on Advanced configuration. Removed unsourced container-storage advice.

Method: documentation only; no commands were run.
