---
id: computing-software.devops-ci-cd.tekton.tekton-pipeline-when-expressions
name: tekton-pipeline-when-expressions
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipeline, when, conditional, skipped-tasks]
level: practitioner
status: docs-checked
description: "Guard a Tekton PipelineTask with when expressions using input, operator and values, including params, results and optional workspace checks."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `when` list guards a task. Each expression has `input` (a static value or a variable such as `$(params.image)` or `$(tasks.task1.results.image)`; defaults to an empty string), `operator` (`in` or `notin`) and `values` (a non-empty array of strings, which may be an array param like `["$(params.images[*])"]`).

Expressions are evaluated before the task runs. If all are true the task runs; if any is false the task is not run and appears under skipped tasks in the PipelineRun status. Using a result in `when` creates a dependency on the producing task.

```yaml
- name: run-lint
  when:
    - input: "$(workspaces.lint-config.bound)"
      operator: in
      values: ["true"]
  taskRef:
    name: lint-source
---
- name: deploy-in-blue
  when:
    - input: "blue"
      operator: in
      values: ["$(params.deployments[*])"]
```

Useful for: matching a git branch name, checking a previous result, checking whether files changed, whether an image exists in the registry, matching a CI job name, or whether an optional workspace was provided (the `workspaces.<name>.bound` variable).

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelines.md. Removed: nothing.

Method: documentation only; no commands were run.
