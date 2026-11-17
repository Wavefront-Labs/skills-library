---
id: computing-software.devops-ci-cd.argo-workflows.progress-and-estimated-duration
name: progress-and-estimated-duration
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-progress, argo-progress-file, estimated-duration, workflow-task-results, progress-reporting]
level: practitioner
status: docs-checked
description: "Read N/M workflow progress, report custom progress from a pod via ARGO_PROGRESS_FILE, and understand why estimated duration can be inaccurate."
sources: ["https://argo-workflows.readthedocs.io/en/latest/progress/", "https://argo-workflows.readthedocs.io/en/latest/estimated-duration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow progress and estimated duration
Progress is `N/M`: `N` completed tasks of `M` total, deterministic for a given workflow shape. A pod node is `1/1` when done else `0/1`; non-leaf nodes sum their children; the workflow total sums leaf nodes. `M` grows as nodes join the graph.

Self-reporting overrides the automatic value: have the pod write `N/M` to the file named by `ARGO_PROGRESS_FILE`, for example:

```sh
echo "$(($i*10))"'/100' > $ARGO_PROGRESS_FILE
```
The executor reads the file every 3s and patches the matching `WorkflowTaskResults` object when it changes; the controller copies it into status every 1m. Tune with `ARGO_PROGRESS_FILE_TICK_DURATION` and `ARGO_PROGRESS_PATCH_TICK_DURATION`. A pod starts at `0/1`; set an initial progress annotation to change that. Workflow RBAC must allow the executor to update task results.

Estimated duration is different: it comes from the most recent successful Workflow from the same WorkflowTemplate, ClusterWorkflowTemplate or CronWorkflow. The controller asks the Kubernetes API first, then the workflow archive if enabled. It can mislead when pods wait long for scheduling, when paths vary with `when`, when `withItems` fans out 100 or 1000 nodes, when pod runtimes are unpredictable, or when parameters change the work.

## Checked
2026-11-03. Confirmed against the Argo Workflows Workflow Progress and Estimated Duration pages: the N/M definition, per-node rules, ARGO_PROGRESS_FILE reporting, 3s and 1m intervals, the tick environment variables, the 0/1 start, the RBAC note and the estimate sources and failure reasons. Nothing removed.
Method: documentation only; no commands were run.
