---
id: computing-software.devops-ci-cd.tekton.tekton-variables-pipeline-and-task
name: tekton-variables-pipeline-and-task
category: computing-software
field: devops-ci-cd
product: tekton
tags: [variables, substitution, context, params]
level: practitioner
status: docs-checked
description: "Reference the Tekton variables available in Pipelines and Tasks: params, results, workspaces, context, step exit codes and credentials paths."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tekton does not escape variable contents; task authors must escape values for the shell, image or language they land in. Common Pipeline variables:
- `params.<name>`, `params['<name>']`, `params.<name>[*]` (whole array or object); element access `params.<name>[i]` and object keys `params.<obj>.<key>` need `enable-api-fields: alpha`.
- `tasks.<task>.results.<result>` (also `[i]`, `[*]`, `.key`); using one can alter execution order. `[*]` cannot be used in `script`.
- `tasks.<task>.matrix.length` and `tasks.<task>.matrix.<result>.length`.
- `workspaces.<name>.bound`.
- `context.pipelineRun.name`, `.namespace`, `.uid`, `context.pipeline.name`, `context.pipelineTask.retries`.
- Only in `finally`: `tasks.<task>.status`, `tasks.<task>.reason` (for example `Failed`, `TaskRunCancelled`, `TaskRunTimeout`, `FailureIgnored`), `tasks.status`.

Task variables add `results.<name>.path`, `workspaces.<name>.path|bound|claim|volume`, `credentials.path` (credentials injected from Secrets with matching annotations), `context.taskRun.name|namespace|uid`, `context.task.name`, `context.task.retry-count`, `steps.step-<stepName>.exitCode.path` (or `steps.step-unnamed-<index>.exitCode.path`) and `artifacts.path`.

## Checked

Checked 2026-11-08 against docs/variables.md in tektoncd/pipeline (main); the variable tables were read in full and the long fields-that-accept-substitution table was skimmed, not used. Confirmed the Pipeline and Task variables listed, the alpha gate on element and object-key access, finally-only status variables and the [*] limit in script. Replaced the unsourced 'plain string replacement' wording with the docs' no-escaping note.

Method: documentation only; no commands were run.
