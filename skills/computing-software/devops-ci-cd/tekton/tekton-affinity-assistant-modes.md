---
id: computing-software.devops-ci-cd.tekton.tekton-affinity-assistant-modes
name: tekton-affinity-assistant-modes
category: computing-software
field: devops-ci-cd
product: tekton
tags: [affinity-assistant, coschedule, workspaces, scheduling]
level: advanced
status: docs-checked
description: "Configure Tekton Affinity Assistant coschedule modes so PipelineRun pods sharing a volume run on the same node."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/affinityassistants.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Affinity Assistant coschedules a PipelineRun's pods onto one node, using Kubernetes pod affinity, so parallel TaskRuns can share a volume. The mode is set by the `coschedule` feature flag:

- `workspaces` (default, stable): when a PVC is the volume source of a workspace, all TaskRun pods sharing it are scheduled to the same node. Only one PVC-backed workspace can be mounted per TaskRun in this mode.
- `pipelineruns` (alpha): all TaskRun pods of the PipelineRun go to the same node.
- `isolate-pipelinerun` (alpha): same node, and only one PipelineRun is allowed on a node at a time.
- `disabled`: no coscheduling.

It is incompatible with other affinity rules on the TaskRun pods: affinity from a custom PodTemplate is overwritten. If the PipelineRun has a PodTemplate, its `nodeSelector` and `tolerations` are also set on the Affinity Assistant pod. The assistant is deleted when the PipelineRun completes.

The older `disable-affinity-assistant` flag was deprecated and removed after release v0.68; use only `coschedule`.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): affinityassistants.md. Removed: nothing.

Method: documentation only; no commands were run.
