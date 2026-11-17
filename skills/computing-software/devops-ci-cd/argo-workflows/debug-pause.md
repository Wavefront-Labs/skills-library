---
id: computing-software.devops-ci-cd.argo-workflows.debug-pause
name: debug-pause
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [debug-pause, argo-debug-pause-after, ephemeral-containers, marker-file, kubectl-debug]
level: advanced
status: docs-checked
description: "Pause a step before or after execution with ARGO_DEBUG_PAUSE_BEFORE and ARGO_DEBUG_PAUSE_AFTER and release it by touching a marker file from an ephemeral container."
sources: ["https://argo-workflows.readthedocs.io/en/latest/debug-pause/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug pause
Debug pause freezes an individual container so you can inspect it, then lets it continue. Set an environment variable on the container:
- `ARGO_DEBUG_PAUSE_BEFORE: 'true'` pauses before the user code runs
- `ARGO_DEBUG_PAUSE_AFTER: 'true'` pauses after it finishes

```yaml
container:
  image: argoproj/argosay:v2
  env:
    - name: ARGO_DEBUG_PAUSE_AFTER
      value: 'true'
```

Release with a marker file inside the container: `/var/run/argo/ctr/main/before` or `/var/run/argo/ctr/main/after`, matching the pause. Where the image has no shell, attach an ephemeral container:

```bash
argo submit -n argo --watch pause-after.yaml
kubectl debug -n argo -it POD_NAME --image=busybox --target=main --share-processes
```

`--share-processes` is needed to reach the step's filesystem. With process namespace sharing, other containers' filesystems appear under `/proc/$pid/root`, so when finished run:

```bash
touch /proc/1/root/var/run/argo/ctr/main/after
```
The workflow step then proceeds. Use `before` instead of `after` when pausing before execution. Replace `POD_NAME` with the pod shown in the workflow.

The example pauses the `argosay` step after execution. Ephemeral containers are useful when the container in use has no shell. The page says steps can be paused before, after or both, so both variables may be defined on the same container.

## Checked
2026-11-03. Confirmed against the Argo Workflows Debug Pause page: both environment variables, the marker file paths, the example workflow, the kubectl debug command with --share-processes and the /proc/1/root touch command. Nothing removed.
Method: documentation only; no commands were run.
