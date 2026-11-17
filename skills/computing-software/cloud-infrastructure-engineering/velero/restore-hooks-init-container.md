---
id: computing-software.cloud-infrastructure-engineering.velero.restore-hooks-init-container
name: restore-hooks-init-container
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [initcontainer-restore-hook, restore-hooks, init-container, restore-wait, restore-spec-hooks]
level: practitioner
status: docs-checked
description: "Add init containers to restored pods through pod annotations or the Restore spec, and know their order relative to restore-wait."
sources:
  - https://velero.io/docs/main/restore-hooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An InitContainer restore hook adds an init container to the pod before it is restored, for setup needed before application containers start. It becomes the first init container in the pod spec. If the pod had volumes backed up with File System Backup, it is added after the `restore-wait` init container. Mutating webhooks in the cluster can alter this order.

Annotation form (all optional):
- `init.hook.restore.velero.io/container-image`
- `init.hook.restore.velero.io/container-name`
- `init.hook.restore.velero.io/command`: the ENTRYPOINT; not run in a shell, and the image ENTRYPOINT is used if absent. Use a JSON array.

```bash
kubectl annotate pod -n <POD_NAMESPACE> <POD_NAME> \
    init.hook.restore.velero.io/container-name=restore-hook \
    init.hook.restore.velero.io/container-image=alpine:latest \
    init.hook.restore.velero.io/command='["/bin/ash", "-c", "date"]'
```

The docs add the annotations to pods before taking the backup.

Restore spec form, under `spec.hooks.resources[].postHooks[].init.initContainers`:

```yaml
hooks:
  resources:
  - name: restore-hook-1
    includedNamespaces: [app]
    postHooks:
    - init:
        initContainers:
        - name: restore-hook-init1
          image: alpine:latest
          volumeMounts:
          - mountPath: /restores/pvc1-vm
            name: pvc1-vm
          command: [/bin/ash, -c, "echo -n FOOBARBAZ >> /restores/pvc1-vm/foobarbaz"]
```

This adds an init container to every pod in the `app` namespace.

## Checked

2026-11-08. Read in full: the Restore Hooks page. Every remaining claim was confirmed there. Removed or reworded: the unstated reason for annotating before backup.

Method: documentation only; no commands were run.
