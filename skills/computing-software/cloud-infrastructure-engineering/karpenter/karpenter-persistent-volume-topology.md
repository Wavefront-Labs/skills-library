---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-persistent-volume-topology
name: karpenter-persistent-volume-topology
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [persistent-volume, pvc, storageclass, waitforfirstconsumer, ebs-csi, topology, zone]
level: advanced
status: docs-checked
description: "How Karpenter honours volume zone constraints: allowedTopologies, WaitForFirstConsumer, existing PV zone reuse, the EBS CSI zone key, and the unsupported region key."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/scheduling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Persistent volume topology

Karpenter follows Pod to PersistentVolumeClaim to StorageClass and adds the storage zone constraints to node launch decisions.

Flow with a `WaitForFirstConsumer` StorageClass allowing `us-west-2a` and `us-west-2b`:
1. Pod created; Karpenter sees storage is needed in those two zones.
2. It randomly picks one (say `us-west-2a`), launches a node there, and waits for kube-scheduler to bind the pod.
3. The CSI driver creates a PV with node affinity for `us-west-2a`.
4. When the pod is recreated against the same claim, Karpenter finds the existing PV and pins the pod to `us-west-2a`.

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: ebs
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: topology.ebs.csi.aws.com/zone
    values: ["us-west-2a", "us-west-2b"]
```

AWS specifics: the EBS CSI driver uses `topology.ebs.csi.aws.com/zone` instead of `topology.kubernetes.io/zone`; Karpenter aliases it internally, and StorageClasses for EBS CSI must use the CSI key.

Unsupported: `topology.kubernetes.io/region` (set by legacy in-tree providers). Move to an out-of-tree CSI driver.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Removed the closing paragraph about consolidation across zones, which the page does not state.
