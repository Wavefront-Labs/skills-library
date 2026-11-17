---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-retry-context-variables
name: tekton-pipeline-retry-context-variables
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, retries, context-variables, substitution]
level: advanced
status: docs-checked
description: "Use context.pipelineTask.retries and context.task.retry-count in Tekton to detect the final retry attempt of a PipelineTask."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two variables expose retry state: `context.pipelineTask.retries` is replaced by the configured `retries` of the PipelineTask, and `context.task.retry-count` by the current retry number.

```yaml
params:
- name: pipelineTask-retries
  value: "$(context.pipelineTask.retries)"
taskSpec:
  params:
  - name: pipelineTask-retries
  steps:
  - image: ubuntu
    name: print-if-retries-exhausted
    script: |
      if [ "$(context.task.retry-count)" == "$(params.pipelineTask-retries)" ]
      then
        echo "This is the last retry."
      fi
      exit 1
```

Each PipelineTask can only see its own `retries` and `retry-count`, not those of other tasks. `context.task.retry-count` is substituted in the Task execution context, so a referenced Task must use it inside the Task itself. If that Task also needs the configured retries, pass `$(context.pipelineTask.retries)` through the PipelineTask `params` and consume it as `$(params.<name>)`.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
