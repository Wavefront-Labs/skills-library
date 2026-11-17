---
id: computing-software.cloud-infrastructure-engineering.velero.backup-hooks-annotations
name: backup-hooks-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-hooks, pre-hook, post-hook, fsfreeze, pod-annotations]
level: practitioner
status: docs-checked
description: "Run pre and post commands in pods during a Velero backup using pod annotations, with defaults for on-error and timeout."
sources:
  - https://velero.io/docs/main/backup-hooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backup hooks run a command in a container of a pod being backed up. Pre hooks run before custom action processing; post hooks run after all custom actions and their extra items are backed up. Commands are not run in a shell. Since 1.15, related items are grouped into ItemBlocks: if a block has several pods (for example an RWX volume mounted by multiple pods), all pre hooks run, then the items are backed up, then all post hooks run.

Annotations (use `pre.` or `post.` prefix, same keys):
- `pre.hook.backup.velero.io/container`: defaults to the first container.
- `pre.hook.backup.velero.io/command`: use a JSON array for arguments, for example `["/usr/bin/uname", "-a"]`.
- `pre.hook.backup.velero.io/on-error`: `Fail` (default) or `Continue`.
- `pre.hook.backup.velero.io/timeout`: default 30s; exceeding it counts as an error.

fsfreeze example:

```shell
kubectl annotate pod -n nginx-example -l app=nginx \
    pre.hook.backup.velero.io/command='["/sbin/fsfreeze", "--freeze", "/var/log/nginx"]' \
    pre.hook.backup.velero.io/container=fsfreeze \
    post.hook.backup.velero.io/command='["/sbin/fsfreeze", "--unfreeze", "/var/log/nginx"]' \
    post.hook.backup.velero.io/container=fsfreeze
```

Test with `velero backup create nginx-hook-test`, then `velero backup logs nginx-hook-test | grep hookCommand`. Hooks can also be declared in the Backup spec instead of annotations.

## Checked

2026-11-08. Read in full: the Backup Hooks page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
