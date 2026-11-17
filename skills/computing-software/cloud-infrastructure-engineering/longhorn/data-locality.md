---
id: computing-software.cloud-infrastructure-engineering.longhorn.data-locality
name: data-locality
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [data-locality, best-effort, strict-local, hyper-converged, storageclass]
level: practitioner
status: docs-checked
description: "Set Longhorn dataLocality to disabled, best-effort or strict-local globally, per volume or in a StorageClass, with the RWX incompatibility."
sources:
  - https://longhorn.io/docs/1.13.0/high-availability/data-locality/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a replica on the node running the workload.

Values of `dataLocality`:
- `disabled` (default): a replica may or may not be on the workload's node.
- `best-effort`: Longhorn tries to keep a replica local but does not stop the volume if it cannot, for example due to low disk space or incompatible disk tags.
- `strict-local`: keeps the only replica on the workload's node for higher IOPS and lower latency. Incompatible with ReadWriteMany volumes; the replica count must be 1.

Where to set it:
- Global default in the UI settings: used only when a volume is created without a value; existing volumes are unchanged.
- Per volume in the UI, at creation or later on the volume detail page.
- StorageClass parameter `dataLocality`.

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: hyper-converged
provisioner: driver.longhorn.io
allowVolumeExpansion: true
parameters:
  numberOfReplicas: "2"
  dataLocality: "best-effort"
  staleReplicaTimeout: "2880" # 48 hours in minutes
  fromBackup: ""
```

Use `strict-local` for applications that replicate data themselves.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/high-availability/data-locality/

Page conflict, no skill change needed: the text says two modes but lists three (disabled, best-effort, strict-local); the skill lists three.

Method: documentation only; no commands were run.
