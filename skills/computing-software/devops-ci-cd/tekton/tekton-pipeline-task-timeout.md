---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-task-timeout
name: tekton-pipeline-task-timeout
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, timeout, taskrun, pipelinerun]
level: intro
status: docs-checked
description: "Configure the failure timeout of a task inside a Tekton Pipeline and how it interacts with the PipelineRun timeout and taskRunSpecs overrides."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `timeout` on a PipelineTask to cap the TaskRun that executes it. The value is a Go duration such as `1h30m`, `1h`, `1m` or `60s`.

```yaml
spec:
  tasks:
    - name: build-the-image
      taskRef:
        name: build-push
      timeout: "0h1m30s"
```

If no task timeout is set, Tekton honors the timeout of the PipelineRun. If a task timeout is larger than the pipeline timeout set in the PipelineRun, the pipeline times out first and takes the task with it: with `timeouts.pipeline = 1h` and `tasks[0].timeout = 3h`, the task still times out after one hour.

A task timeout declared in the Pipeline can be overridden at run time through `taskRunSpecs` in the PipelineRun, so a specific execution can adjust timeouts without editing the Pipeline.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
