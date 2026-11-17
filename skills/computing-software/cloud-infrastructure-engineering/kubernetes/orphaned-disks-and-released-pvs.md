---
id: computing-software.cloud-infrastructure-engineering.kubernetes.orphaned-disks-and-released-pvs
name: orphaned-disks-and-released-pvs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, access-modes-reclaim, orphaned-disks, released-pv, cost-optimisation, cleanup]
level: practitioner
status: docs-checked
description: "Find Released PVs and cloud disks left unattached after clusters, namespaces or PVCs were deleted, map them back to their PVCs, and clean up safely."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#retain", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/tagging.md", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Released PVs and orphaned cloud disks

## In the cluster
```bash
kubectl get pv
kubectl get pv <pv> -o jsonpath='{.spec.claimRef.namespace}/{.spec.claimRef.name} {.spec.csi.volumeHandle}{"\n"}'
```
In the `kubectl get pv` output look for STATUS `Released` or `Failed` (both are PV phases). A PV with
reclaim policy `Retain` is not deleted or reused automatically: the Kubernetes docs call this manual
reclamation, so its backing disk stays until someone acts.

## In the cloud
Disks whose cluster or PV is gone are found with your cloud's CLI or console, by listing
unattached disks and then matching each against the cluster. Use the identifiers the driver records:
- AWS EBS CSI driver: tags `CSIVolumeName` (set to the PV name, for example `pvc-<uid>`) and
  `ebs.csi.aws.com/cluster=true` on every volume it creates; `kubernetes.io/cluster/<id>=owned` when
  the driver's `k8s-tag-cluster-id` argument is set. PVC namespace and name are **not** tagged by
  default: add them with `tagSpecification` StorageClass parameters using the
  `{{ .PVCNamespace }}`, `{{ .PVCName }}` and `{{ .PVName }}` placeholders, which need the
  external-provisioner's `--extra-create-metadata` flag (the Helm chart enables it by default).
- Other clouds: use the labels or tags your CSI driver documents, or set your own through
  StorageClass parameters if the driver supports it.
Compare volume IDs against `kubectl get pv -o jsonpath='{..volumeHandle}'` in every live cluster
before deleting anything.

## Clean up
1. Snapshot anything with unknown value (cheap compared to the disk).
2. Tag it `pending-delete=<date>` and wait a notice period.
3. Delete the PV object, then the disk.

## Prevent
- Default `Delete` policy for scratch classes; `Retain` only for data that has an owner.
- Delete PVCs before tearing down clusters, or use a cluster-delete script that lists retained disks.
- Cost reports filtered on unattached volumes.

## Verify
No unattached disks older than the notice period remain, and every Released PV has a ticket or owner.

## Checked

Checked 2026-10-27. Documentation checked: aws-ebs-csi-driver tagging.md and install.md (master) and the Kubernetes website main tree persistent volumes page (v1.38 dev; v1.37 latest release). Confirmed: PV phases `Released` and `Failed`, `Retain` means manual reclamation, `claimRef` and `csi.volumeHandle` fields, EBS CSI automatic tags `CSIVolumeName` and `ebs.csi.aws.com/cluster`, `kubernetes.io/cluster/<id>` tag with `k8s-tag-cluster-id`, `tagSpecification` placeholders and the `--extra-create-metadata` requirement. Fixed: the skill used `kubernetes.io/created-for/pvc/...` tags that the EBS CSI driver does not add by default (it tags the PV name and, only with `tagSpecification`, PVC details). Removed as unconfirmed because the provider CLI documentation is not in a readable repository: the `aws ec2`, `gcloud` and `az` listing commands and the OpenCost reference.

Method: documentation only; no commands were run.
