---
id: computing-software.cloud-infrastructure-engineering.kubernetes.csi-migration-in-tree-deprecation
name: csi-migration-in-tree-deprecation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, csimigration, in-tree-plugin, deprecated-provisioner, aws-ebs, gce-pd, azure-disk, cinder, kube-controller-manager, feature-gate, storageclass-provisioner-rename]
level: advanced
status: docs-checked
description: "What CSIMigration actually does when a cluster's in-tree volume plugins (kubernetes.io/aws-ebs etc.) move to CSI, and what breaks if you miss a step."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#migrating-to-csi-drivers-from-in-tree-plugins", "https://kubernetes.io/docs/concepts/storage/storage-classes/", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-storage/625-csi-migration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSI migration — when `kubernetes.io/aws-ebs` quietly becomes `ebs.csi.aws.com`

**Goal:** understand what CSIMigration changes under an unchanged-looking StorageClass,
so an upgrade doesn't surprise you with volumes that stop provisioning.

## 1. What's actually deprecated
In-tree volume plugins (`kubernetes.io/aws-ebs`, `kubernetes.io/gce-pd`,
`kubernetes.io/azure-disk`, `kubernetes.io/cinder`, `kubernetes.io/vsphere-volume`,
`kubernetes.io/portworx-volume`) are the original, built-into-kubelet volume drivers.
In-tree provisioners are deprecated. Some in-tree volume types have been removed entirely
(`awsElasticBlockStore`: deprecated v1.19, removed v1.27; `gcePersistentDisk`: deprecated v1.17,
removed v1.28). **CSIMigration** (stable since v1.25) directs operations against existing in-tree
plugins to the corresponding CSI plugin, so existing StorageClasses, PersistentVolumes and
PersistentVolumeClaims that refer to the in-tree plugin need no configuration changes. Supported
operations: provisioning/delete, attach/detach, mount/unmount and resizing. For example, on current
versions Portworx in-tree volumes are redirected to `pxd.portworx.com` by default.

## 2. What you must have for the shim to work
- The actual CSI driver (e.g. the AWS EBS CSI driver) **installed and configured** in the
  cluster. The Kubernetes documentation states that you or another cluster administrator
  must install it; the core of Kubernetes does not install that software for you.

## 3. What stays the same vs. what changes
- **Existing StorageClasses, PVs and PVCs that refer to an in-tree plugin**: need no
  configuration change. Existing PVs created by an in-tree plugin remain usable, even
  after you upgrade to a version without compiled-in support for that storage type,
  provided the CSI driver is installed. New PVCs and PVs that refer to the legacy
  integrations also keep working once the driver is installed; actual storage management
  happens through the CSI driver. New StorageClasses should name the CSI provisioner
  directly (for AWS EBS, `ebs.csi.aws.com`).
- **`CSINode`/`CSIDriver` objects**: kubelet maintains `CSINode` once a driver registers;
  a missing entry for the driver on a cluster you believe is migrated is the first thing
  to check.
- **New provisioning requests**: go through the CSI driver once it is installed; the
  supported operations are the ones listed above.

## 4. The upgrade sequence that avoids an outage
1. Install the CSI driver (controller + node plugin) **before** upgrading past the
   Kubernetes version that removes the in-tree code for that storage type — verify with
   `kubectl get pods -A` (look for the driver's pods) and `kubectl get csidriver`.
2. Confirm existing PVCs still provision/mount correctly on a canary node pool before
   rolling the upgrade cluster-wide.
3. Only then migrate new StorageClasses to the explicit CSI `provisioner:` name — not
   required for correctness, but keeps new YAML honest about what's actually running.

## Gotchas
- Never assume the driver is already installed on your cluster; check, and follow your
  platform's and the driver's own documentation for installation and for the cloud
  permissions the driver needs.
- After migration, the actual storage management happens through the CSI driver, so look
  in the driver's pods for logs, even if the StorageClass still names the in-tree provisioner.

## Verify
- [ ] Confirmed the actual CSI driver (controller + node) is deployed before any
      cluster upgrade past in-tree removal.
- [ ] Checked `kubectl get csidriver,csinode` exist and report healthy capacity/capabilities.
- [ ] Verified the cloud permissions the driver's documentation requires are in place.
- [ ] Provisioned a new PVC post-migration and confirmed it went through the CSI
      driver's logs, not a silent no-op.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: CSIMigration stable since v1.25 and its documented behaviour (no config changes, driver must be installed by the administrator, supported operations); AWS EBS in-tree deprecated v1.19 removed v1.27; gcePersistentDisk deprecated v1.17 removed v1.28; Portworx redirected to pxd.portworx.com. Removed unconfirmed per-provider feature-gate names, IAM/IRSA details and the claim that every listed in-tree plugin is already removed.

Method: documentation only; no commands were run.
