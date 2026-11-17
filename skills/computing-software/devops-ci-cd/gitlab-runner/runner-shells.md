---
id: computing-software.devops-ci-cd.gitlab-runner.runner-shells
name: runner-shells
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [shells, bash, sh, powershell, pwsh]
level: intro
status: docs-checked
description: "Which shells job scripts run in and the defaults per platform."
sources: ["https://docs.gitlab.com/runner/shells/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shells

Runner shell generators produce the scripts for every build step: clone, cache restore, build commands, cache save and artifacts upload. Shells have no configuration options; the steps come from the `script` directive in `.gitlab-ci.yml`.

Supported shells:
- `bash`: default on all Unix systems.
- `sh`: fallback for bash on Unix.
- `powershell`: PowerShell Desktop; default for jobs on Windows with the Kubernetes and docker-windows executors.
- `pwsh`: PowerShell Core; default for new runner registration on Windows and for jobs using the shell executor.

To use a non-default shell, set it in `config.toml`. The shell must exist in the environment where the script runs.

## Checked

2026-11-03. Confirmed against shell list and defaults on the Shells page.

Method: documentation only; no commands were run.
