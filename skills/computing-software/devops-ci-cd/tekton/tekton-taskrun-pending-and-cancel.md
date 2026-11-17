---
id: computing-software.devops-ci-cd.tekton.tekton-taskrun-pending-and-cancel
name: tekton-taskrun-pending-and-cancel
category: computing-software
field: devops-ci-cd
product: tekton
tags: [taskrun, pending, cancel, status]
level: practitioner
status: docs-checked
description: "Create Tekton TaskRuns in a pending state, start them later, and cancel them, including how the timeout clock behaves."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/taskruns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A TaskRun can be created pending by setting `spec.status: TaskRunPending`:

```yaml
apiVersion: tekton.dev/v1
kind: TaskRun
metadata:
  name: my-taskrun
spec:
  taskRef:
    name: my-task
  status: "TaskRunPending"
```

While pending: no Pod is created, `status.startTime` is unset and the condition is `Unknown` with reason `TaskRunPending`. Clear `spec.status` to start it, or set `TaskRunCancelled` to cancel without running. The timeout clock does not run while pending, because the timeout check returns false when `startTime` is unset; it starts after pending is cleared. Pending can only be set before the run has started.

Cancelling a running TaskRun is the same field set to `TaskRunCancelled`; this deletes the running pod, so its logs are not preserved, unless `keep-pod-on-cancel` is `"true"` in `feature-flags`.

The docs list uses: external scheduling, approval workflows, queueing tasks until resources are available, and creating many TaskRuns to start together.

## Checked

Checked 2026-11-08 against docs/taskruns.md in tektoncd/pipeline (main), reading the Pending TaskRuns and Cancelling a TaskRun sections in full (partial read of a long file). Confirmed the pending behaviour, timeout clock note and listed uses. Added the cancel behaviour and keep-pod-on-cancel from the same page.

Method: documentation only; no commands were run.
