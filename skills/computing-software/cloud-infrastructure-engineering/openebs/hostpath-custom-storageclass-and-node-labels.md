---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-custom-storageclass-and-node-labels
name: hostpath-custom-storageclass-and-node-labels
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, storageclass, nodeaffinitylabels, filepermissions, basepath, custom-labels]
level: practitioner
status: docs-checked
description: "Create a custom Local PV Hostpath StorageClass with its own BasePath, stable node-identity labels via NodeAffinityLabels, and a tighter 0770 directory mode."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/configuration/hostpath-create-storageclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default class `openebs-hostpath` uses `/var/openebs/local`, so create your own only when you need a different path or option. The guide's steps: save the definition as `local-hostpath-sc.yaml`, edit `metadata.name` and the `BasePath`, apply it with `kubectl apply -f`, and verify with `kubectl get sc local-hostpath -o yaml`. The provisioner creates a missing `BasePath` when the first volume is scheduled on a node, so make sure the value is a valid absolute path.

A minimal custom class from the guide:

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-hostpath
  annotations:
    openebs.io/cas-type: local
    cas.openebs.io/config: |
      - name: StorageType
        value: hostpath
      - name: BasePath
        value: /var/local-hostpath
provisioner: openebs.io/local
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

**Custom node labels.** Default `kubernetes.io/hostname` labels may not be unique across a cluster. Add a `NodeAffinityLabels` list entry such as `openebs.io/custom-node-unique-id` so the volume's node affinity uses it. This does not influence pod scheduling.

**File permissions.** Volumes default to `0777`. Add `FilePermissions` with `data: mode: "0770"` to narrow that. It cannot be set through Helm values for the default class; use a custom class or a per-PVC annotation.

## Checked

2026-11-04. Confirmed against the Create StorageClass(s) page for Local PV Hostpath: the apply and verify steps, the example class, custom node labels, the 0777 default, the 0770 mode, and the Helm limitation for FilePermissions. Removed the node re-add example, which that page does not give.

Method: documentation only; no commands were run.
