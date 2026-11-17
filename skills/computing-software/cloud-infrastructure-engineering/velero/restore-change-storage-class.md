---
id: computing-software.cloud-infrastructure-engineering.velero.restore-change-storage-class
name: restore-change-storage-class
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [change-storage-class, storageclass-mapping, restoreitemaction, plugin-config, configmap]
level: practitioner
status: docs-checked
description: "Map old storage classes to new ones during a Velero restore using a labelled ConfigMap in the velero namespace."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero can change the storage class of persistent volumes and persistent volume claims during a restore. Create a ConfigMap in the Velero namespace; Velero identifies it by labels, not by name.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: change-storage-class-config
  namespace: velero
  labels:
    velero.io/plugin-config: ""
    velero.io/change-storage-class: RestoreItemAction
data:
  <old-storage-class>: <new-storage-class>
```

Rules:
- It must live in the `velero` namespace.
- Use both labels verbatim. `velero.io/plugin-config` is value-less and marks the ConfigMap as configuration for a plugin (here the built-in restore item action plugin); `velero.io/change-storage-class: RestoreItemAction` identifies the name and kind of plugin.
- Add one or more key-value pairs under `data`, key = old storage class name, value = new storage class name.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Changing PV/PVC Storage Classes", read in full). Removed unsourced content: the gp2-to-gp3 example, the requirement that the new class exist, the `kubectl get pvc` check and the delete-after-migration advice.

Method: documentation only; no commands were run.
