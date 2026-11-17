---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-runafter-ordering
name: tekton-pipeline-runafter-ordering
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, runafter, ordering, dag]
level: intro
status: docs-checked
description: "Control Tekton PipelineTask execution order with runAfter when there is no result or workspace dependency between tasks."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tasks in a Pipeline form a graph. Order is implied by data dependencies (a task consuming another task's results). When there is no such output, use `runAfter` to say that a task must execute after one or more others, whatever order they are written in the Pipeline.

```yaml
tasks:
- name: test-app
  taskRef:
    name: make-test
  workspaces:
  - name: source
    workspace: source
- name: build-app
  taskRef:
    name: kaniko-build
  runAfter:
    - test-app
  workspaces:
  - name: source
    workspace: source
```

Here `build-app` waits for `test-app` even though `test-app` produces no result that `build-app` reads. Tasks without ordering links may run in parallel. Note that `finally` tasks cannot be ordered among themselves: the docs list "Cannot configure the finally task execution order" as a known limitation, as they always run in parallel after the main tasks complete.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
