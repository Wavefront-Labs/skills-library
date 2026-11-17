---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-param-enum
name: tekton-pipeline-param-enum
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, params, enum, alpha, validation]
level: advanced
status: docs-checked
description: "Restrict Tekton Pipeline and Task parameters to a fixed set of values with enum, including the subset rule between pipeline-level and task-level enums."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`enum` on a parameter is an alpha feature: set the `enable-param-enum` feature flag to `"true"` first.

A parameter declaration may carry `enum`, a predefined set of accepted values. If it also has a `default`, the default must be in the set. When a `PipelineRun` passes a value outside the list, the run fails with reason `InvalidParamValue`.

```yaml
spec:
  params:
  - name: message
    enum: ["v1", "v2"]
    default: "v1"
```

Subset rule: when a `PipelineTask` references a `Task` whose parameter has an `enum`, the pipeline-level `enum` must be a subset of the task-level one. An empty pipeline-level `enum` is invalid in that case, because an empty set means "universal set" and would allow every value. Example: the Task allows `["v1","v2"]` and the Pipeline narrows it to `["v1"]`.

The subset check only applies when the task-level param is a direct, single reference to a pipeline-level param. If a task param combines several pipeline params (for example `"$(params.message1) and $(params.message2)"`), no subset validation is applied. Tekton validates the user-supplied value against the Pipeline enum, and also validates each resolved task param against the PipelineTask enum before creating the TaskRun.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
