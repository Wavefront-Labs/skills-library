---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-parameters
name: tekton-pipeline-parameters
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, params, parameters, pipelinerun]
level: practitioner
status: docs-checked
description: "Declare Pipeline parameters in Tekton with string or array types and defaults, pass them to tasks with variable substitution, and supply values from a PipelineRun."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pipeline `spec.params` are inputs supplied by the `PipelineRun` and substituted into task parameters.

Rules for names: alphanumeric characters, hyphens and underscores only, and the name must begin with a letter or underscore (`fooIs-Bar_` is valid; `barIsBa$` and `0banana` are not). `type` is `string` (the default) or `array`; the supplied value is validated against the declared type. `description` and `default` are optional; a default is used when the `PipelineRun` omits the value.

```yaml
spec:
  params:
    - name: context
      type: string
      default: /some/where/or/other
    - name: flags
      type: array
  tasks:
    - name: build-skaffold-web
      taskRef:
        name: build-push
      params:
        - name: pathToContext
          value: "$(params.context)"
        - name: flags
          value: ["$(params.flags[*])"]
```

An array pipeline parameter passed to a task must land in a task parameter that is also an array. The `PipelineRun` supplies values under `spec.params` (a string for `context`, a list for `flags`). Parameter values can also be used anywhere in the Pipeline through variable substitution.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
