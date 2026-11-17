---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-overview
name: tekton-workspaces-overview
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, storage, taskrun, pipelinerun]
level: intro
status: docs-checked
description: "Understand how Tekton Workspaces let a Task declare filesystem needs while the TaskRun or PipelineRun decides the storage, including optional workspaces."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Workspaces` let a `Task` declare parts of the filesystem that must be supplied at run time. A `TaskRun` can satisfy one with a read-only `ConfigMap` or `Secret`, an existing `PersistentVolumeClaim`, a PVC created from a `volumeClaimTemplate`, or an `emptyDir` discarded when the run ends. They are like Volumes, except the Task author defers the storage class decision to whoever runs it.

Typical purposes: inputs and outputs, sharing data among tasks, a mount point for credentials in Secrets or configuration in ConfigMaps, shared tooling, and build caches.

The split of duties: the Task says where a workspace appears for its steps; the TaskRun supplies the actual volume. The Task declaration stays the same whether a run uses a quick `emptyDir` or a pre-populated PVC. In a Pipeline, the Pipeline shows how storage is shared across tasks (task A clones, task B compiles), and the PipelineRun provides the volume and must make sure the volume type can be shared safely and accessed in the right order.

Both Tasks and Pipelines may mark a workspace `optional`: the run can omit the binding, and behaviour may change when it does (optional credentials, an optional lint config, an optional build cache).

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
