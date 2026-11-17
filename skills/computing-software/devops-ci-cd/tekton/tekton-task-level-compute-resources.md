---
id: computing-software.devops-ci-cd.tekton.tekton-task-level-compute-resources
name: tekton-task-level-compute-resources
category: computing-software
field: devops-ci-cd
product: tekton
tags: [compute-resources, limitrange, resourcequota, steps]
level: advanced
status: docs-checked
description: "Set Tekton task-level computeResources instead of per-step requests and limits, and avoid the stepOverrides conflict."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/compute-resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Beta feature. Steps run sequentially, but a pod's effective requirements are the sum of all its containers' requirements, so per-step requests must be treated as if steps ran in parallel (Tekton adjusts them to satisfy LimitRanges and ResourceQuotas). Task-level settings avoid that: a task-level request makes the kubelet reserve only that amount, and a task-level limit caps every step.

Configure in `TaskRun.spec.computeResources` or `PipelineRun.spec.taskRunSpecs[].computeResources`:

```yaml
spec:
  computeResources:
    requests:
      cpu: 1
    limits:
      cpu: 2
```

Rules from the docs: task-level values do not apply to sidecars (use `sidecarOverrides` for those); if only limits are given they are also used as requests; they override resource settings on `Step` or `StepTemplate` of the referenced Task; a TaskRun with both `stepOverrides` and task-level `computeResources` is rejected (also in `taskRunSpecs`).

## Checked

Checked 2026-11-08 against docs/compute-resources.md in tektoncd/pipeline (main), read in full. Confirmed beta status, summed effective requirements, task-level request and limit semantics, the four listed rules, the TaskRun and PipelineRun configuration locations, and the stepOverrides conflict. No changes needed to claims.

Method: documentation only; no commands were run.
