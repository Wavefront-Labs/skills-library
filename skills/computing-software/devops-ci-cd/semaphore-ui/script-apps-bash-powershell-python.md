---
id: computing-software.devops-ci-cd.semaphore-ui.script-apps-bash-powershell-python
name: script-apps-bash-powershell-python
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [bash, powershell, python, scripts, task-templates, semaphore-ui]
level: intro
status: docs-checked
description: "Run Bash, PowerShell and Python scripts from a repository with variable groups injected as environment variables."
sources:
  - https://semaphoreui.com/docs/user-guide/apps/bash
  - https://semaphoreui.com/docs/user-guide/apps
  - https://semaphoreui.com/docs/user-guide/apps/python
  - https://semaphoreui.com/docs/user-guide/apps/powershell
  - https://semaphoreui.com/docs/faq/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Script templates: Bash, PowerShell, Python

Goal: run non-Ansible scripts with the same project workflow.

Create a template with the matching app: Bash Script (`/bin/bash`), PowerShell Script (`pwsh`, on Windows hosts or from a Windows runner) or Python Script (`python3`). Fields: Name, Repository, Playbook/Script path relative to the repository (for example `scripts/deploy.sh`, `scripts/deploy.ps1`, `scripts/deploy.py`) and Variable Groups. Then Create and Run. The New Task dialog has only an optional message, plus survey variables and prompts if defined.

Variables from the selected variable groups are injected as environment variables. Read them in scripts:

```bash
echo "Deploying to $TARGET_ENV"
```

```python
import os
target = os.environ["TARGET_ENV"]
```

The interpreter must be installed on the machine that runs the task. The official Docker image contains Ansible, Terraform, OpenTofu, Bash and Python.

Survey variables reach these scripts as `name=value` command-line arguments (or as environment variables if the target is set so).

Gotcha: very short Bash scripts may lose the last lines of output on older versions because buffered output was not read before completion. Upgrade server and runners.

The Applications page lets administrators enable or disable apps and register custom apps; built-in apps are Ansible, Terraform, OpenTofu, Terragrunt, Bash, PowerShell and Python.

## Checked

2026-11-07. Read in full: user-guide/apps/bash.md, apps/README.md, apps/python.md and apps/powershell.md, and the Bash output entry of faq/troubleshooting.md (in the semaphore-docs repository). Confirmed: app binaries, template fields, New Task dialog, environment-variable injection, the image contents, the Windows note, the Applications page and built-in app list, the short-script output gotcha. Removed: the "common ones" claim and the invented Verify step.
Method: documentation only; no commands were run.
