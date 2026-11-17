---
id: computing-software.devops-ci-cd.tekton.tekton-pipelinerun-cancel-stop-pending
name: tekton-pipelinerun-cancel-stop-pending
category: computing-software
field: devops-ci-cd
product: tekton
tags: [pipelinerun, cancel, graceful-stop, pending]
level: practitioner
status: docs-checked
description: "Cancel, gracefully cancel, gracefully stop or hold a Tekton PipelineRun by setting spec.status, and know how finally tasks and retries behave in each case."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/pipelineruns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All four are set through `spec.status`:

- `Cancelled`: TaskRuns are cancelled, pods deleted, retries are not executed, and pending finally tasks are not scheduled.
- `CancelledRunFinally`: graceful cancel. TaskRuns are cancelled and pods deleted with no retries, but finally tasks are scheduled normally.
- `StoppedRunFinally`: graceful stop. Running TaskRuns complete normally, including their retries; no new non-finally task is scheduled; finally tasks run afterwards.
- `PipelineRunPending`: create the run in a pending state so it does not start. Only valid before the run has started. Clear `spec.status` to start it, or set `Cancelled` to cancel.

```yaml
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: go-example-git
spec:
  status: "CancelledRunFinally"
```

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): pipelineruns.md. Removed: nothing.

Method: documentation only; no commands were run.
