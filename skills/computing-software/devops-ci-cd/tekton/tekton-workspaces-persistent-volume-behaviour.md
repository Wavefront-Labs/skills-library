---
id: computing-software.devops-ci-cd.tekton.tekton-workspaces-persistent-volume-behaviour
name: tekton-workspaces-persistent-volume-behaviour
category: computing-software
field: devops-ci-cd
product: tekton
tags: [workspaces, access-modes, storageclass, availability-zones]
level: advanced
status: docs-checked
description: "Pick storage class and access mode for PVC-backed Tekton workspaces and avoid availability-zone and parallel-task conflicts."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Storage class: a PVC with no `storageClassName` uses the cluster default. In regional clusters (nodes in several availability zones) a default class is typically available in one zone only; a regional class exists but costs more (replicated volumes) and may have higher latency.

Access modes:
- `ReadWriteOnce` is the most common but mounts on one node at a time, which hurts pipelines with parallel tasks on the same volume. The Affinity Assistant schedules all tasks using the same PVC onto the same node.
- `ReadOnlyMany` is rare in CI and usually needs data prepared first; dynamically provisioned volumes often cannot be used read-only.
- `ReadWriteMany` is the least commonly available. If the volumes are available to all nodes you may want to disable the Affinity Assistant. Any pod allowed to mount a RWX PVC sees the same filesystem concurrently, so never share one across trust boundaries.

Availability zones: in clouds with zonal volumes (the docs mention GKE) a pod in another zone cannot reach the volume. For zonal clusters or ReadWriteOnce, set `coschedule: workspaces` so each TaskRun pod lands in the zone of its PVC. When `coschedule` is `workspaces` or `disabled`, binding multiple PVC-backed workspaces to the same TaskRun in a PipelineRun is not allowed.

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): workspaces.md. Removed: nothing.

Method: documentation only; no commands were run.
