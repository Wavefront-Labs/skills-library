---
id: computing-software.cloud-infrastructure-engineering.kubernetes.csi-topology-zonal-provisioning
name: csi-topology-zonal-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csi, csi-topology, topology-aware-provisioning, allowedtopologies, waitforfirstconsumer]
level: practitioner
status: docs-checked
description: "Make CSI volumes provision in the zone where the pod can run, using driver topology keys, CSINode, WaitForFirstConsumer and allowedTopologies."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode", "https://kubernetes.io/docs/concepts/storage/storage-classes/#allowed-topologies", "https://kubernetes-csi.github.io/docs/topology.html", "https://kubernetes-csi.github.io/docs/csi-node-object.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSI topology and zonal provisioning

Zonal disks (EBS, PD, Azure Disk) attach only to nodes in the same zone. Topology tells the
provisioner where to create them.

## How it fits together
1. The node plugin reports its topology in `NodeGetInfo`; see it in CSINode and node labels:
   ```bash
   kubectl get csinode <node> -o jsonpath='{.spec.drivers[*].topologyKeys}'
   kubectl get node <node> -L topology.kubernetes.io/zone
   ```
2. external-provisioner, deployed with `--feature-gates=Topology=true` (per the kubernetes-csi topology page), passes
   the topology requirements to `CreateVolume` (`accessibility_requirements`: `requisite` and `preferred`).
3. The PV carries node affinity for the chosen topology; the scheduler places pods accordingly.

## StorageClass
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: gp3-zonal}
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: topology.kubernetes.io/zone
    values: [eu-west-1a, eu-west-1b]
```
`WaitForFirstConsumer` delays binding and provisioning until a pod using the claim is created, so
the volume is provisioned conforming to the pod's scheduling constraints. With `Immediate`
(the default when `volumeBindingMode` is unset), binding and provisioning happen when the PVC is
created, without knowledge of the pod's scheduling requirements, which can make pods
unschedulable. With `WaitForFirstConsumer`, `allowedTopologies` is usually unnecessary; use it only if you still
need to restrict zones.

## Gotchas
- Drivers report their own topology keys (see `topologyKeys` in CSINode above); use the keys the driver
  documents in `allowedTopologies`.
- A pod that uses a provisioned zonal volume can only run on nodes matching the volume's
  topology, so keep nodes available in every zone that holds volumes.

## Verify
`kubectl get pv <pv> -o jsonpath='{.spec.nodeAffinity}'` shows the volume's topology.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: CSINode topologyKeys, NodeGetInfo accessible_topology, accessibility_requirements requisite/preferred, Topology feature gate on external-provisioner, Immediate default and its risk, WaitForFirstConsumer and allowedTopologies guidance. Removed the unconfirmed claims on random zone choice, the 'volume node affinity conflict' message, StatefulSet zone pinning and the sidecar default.

Method: documentation only; no commands were run.
