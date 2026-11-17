---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-variables-and-defaults
name: tekton-workspaces-variables-and-defaults
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, variables, default-binding, config-defaults]
level: practitioner
status: docs-checked
description: "Use workspaces.NAME.path, bound, claim and volume variables in Tekton and set a default TaskRun workspace binding in config-defaults."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables available inside a Task:
- `$(workspaces.<name>.path)`: the path; an empty string when the workspace is optional and not provided.
- `$(workspaces.<name>.bound)`: `true` or `false`; always `true` for a required workspace. Handy in `when` expressions to guard a task on an optional workspace.
- `$(workspaces.<name>.claim)`: name of the PVC used as the volume source; empty for other volume source types.
- `$(workspaces.<name>.volume)`: name of the Volume provided for the workspace.

Default binding: an organisation can let users run Tasks without knowing workspace specifics. Add a default workspace binding to the `config-defaults` ConfigMap under the key `default-task-run-workspace-binding`. Any required workspace the TaskRun leaves unbound gets that configuration. Optional workspaces are never filled by the default, because a Task usually behaves differently when an optional workspace is bound.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
