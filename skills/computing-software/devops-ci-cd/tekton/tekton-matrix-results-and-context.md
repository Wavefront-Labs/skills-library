---
id: computing-software.devops-ci-cd.tekton.tekton-matrix-results-and-context
name: tekton-matrix-results-and-context
category: computing-software
field: devops-ci-cd
product: tekton
tags: [matrix, results, context-variables, aggregation]
level: advanced
status: docs-checked
description: "Consume aggregated results from a matrixed Tekton PipelineTask and use matrix length variables and retries."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/matrix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each fanned-out TaskRun that emits a string result has its value aggregated into an array during reconciliation. A later PipelineTask consumes the whole array with the star notation:

```yaml
params:
  - name: url
    value: $(tasks.matrix-emitting-results.results.report-url[*])
```

Support table: a string result consumed by an array parameter works (`$(tasks.<pipelineTaskName>.results.<resultName>[*])`); array and object results are not supported. Known limitation: you cannot consume a single result or a specific combination from the fan-out.

Context variables: `$(tasks.<name>.matrix.length)` is the number of instances created, and `$(tasks.<name>.matrix.<resultName>.length)` is the number of results actually produced, which lets you loop over them. To order a consumer after the matrix use `runAfter` or result consumption in the same PipelineTask.

Retries: `retries` on a matrixed PipelineTask applies per fanned-out run, so three combinations with `retries: 1` can each be retried once.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): matrix.md. Removed: nothing.

Method: documentation only; no commands were run.
