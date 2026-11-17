---
id: computing-software.cloud-infrastructure-engineering.velero.restore-hooks-exec
name: restore-hooks-exec
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [exec-restore-hook, post-hook-restore, wait-for-ready, exec-timeout, wait-timeout]
level: practitioner
status: docs-checked
description: "Run commands in restored containers with post.hook.restore.velero.io annotations or the Restore spec, with timeout and on-error semantics."
sources:
  - https://velero.io/docs/main/restore-hooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Exec restore hooks run a command in a container of a restored pod after it starts. If a pod has the annotation `post.hook.restore.velero.io/command`, that is the only hook run in the pod and no restore-spec hooks run there.

Annotations:
- `.../container`: defaults to the first container.
- `.../command`: JSON array; no shell unless you start with `/bin/sh` or similar.
- `.../on-error`: `Fail` or `Continue` (default `Continue`, failures only logged). With `Fail`, no more restore hooks run in any container of any pod and the Restore becomes `PartiallyFailed`.
- `.../exec-timeout`: default 30 seconds once execution begins.
- `.../wait-timeout`: how long to wait for the container to be ready; it starts at container restore, so allow for image pull and volume mounts. If unset the restore waits indefinitely.
- `.../wait-for-ready`: string boolean, default false. If one hook on a pod sets it to "true", all other hook executions on that pod, whatever their origin (Backup or Restore), also wait for Ready.

```bash
kubectl annotate pod -n <POD_NAMESPACE> <POD_NAME> \
    post.hook.restore.velero.io/container=postgres \
    post.hook.restore.velero.io/command='["/bin/bash", "-c", "psql < /backup/backup.sql"]' \
    post.hook.restore.velero.io/wait-timeout=5m \
    post.hook.restore.velero.io/exec-timeout=45s \
    post.hook.restore.velero.io/on-error=Continue
```

In the Restore spec you can list several hooks per pod. Hooks for one container run sequentially in spec order once it starts, and all hooks for one container finish before another container's hooks.

## Checked

2026-11-08. Read in full: the Restore Hooks page. Every remaining claim was confirmed there. Removed or reworded: the loose 'including backup hooks' wording.

Method: documentation only; no commands were run.
