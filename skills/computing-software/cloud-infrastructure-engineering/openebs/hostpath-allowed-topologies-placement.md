---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-allowed-topologies-placement
name: hostpath-allowed-topologies-placement
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, allowedtopologies, scheduling, helm-values, node-placement]
level: practitioner
status: docs-checked
description: "Restrict Local PV Hostpath volumes to nodes that actually have the BasePath using allowedTopologies, including the Helm value for the default openebs-hostpath class."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/configuration/hostpath-create-storageclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a Local PV Hostpath volume can be provisioned on any node. If the `BasePath` only exists on some nodes, use Kubernetes `allowedTopologies` on the StorageClass to list where it is available. The guide's example uses a `matchLabelExpressions` entry with key `kubernetes.io/hostname` and values `worker-2` and `worker-3`. Volumes of that class are then provisioned and scheduled on those nodes only.

The important distinction in the docs: unlike `NodeAffinityLabels`, which only changes how the volume identifies its node, **`allowedTopologies` also influences scheduling of the application pod**. Use it whenever placement matters, and use NodeAffinityLabels when the problem is node identity.

To set it on the `openebs-hostpath` class that the Helm chart creates, use the value `localpv-provisioner.hostpathClass.allowedTopologies` in a values file, with the same `matchLabelExpressions` structure nested under `localpv-provisioner` and `hostpathClass`, then apply it:

```
helm upgrade openebs openebs/openebs --namespace openebs -f values.yaml
```

## Checked

2026-11-04. Confirmed against the Create StorageClass(s) page for Local PV Hostpath, section Restrict Volume Placement Using Allowed Topologies: the `worker-2` and `worker-3` example, the contrast with NodeAffinityLabels, the `localpv-provisioner.hostpathClass.allowedTopologies` Helm value and the `helm upgrade` command. Removed the WaitForFirstConsumer and Pending troubleshooting paragraph, which is not in that section.

Method: documentation only; no commands were run.
