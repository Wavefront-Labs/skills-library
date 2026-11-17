---
id: computing-software.cloud-infrastructure-engineering.openebs.troubleshoot-local-pvc-pending-and-install-errors
name: troubleshoot-local-pvc-pending-and-install-errors
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [troubleshooting, pvc-pending, waitforfirstconsumer, nodename, rbac, cluster-admin, multipath, provisioner-logs]
level: practitioner
status: docs-checked
description: "Fix common OpenEBS local storage problems: PVC Pending with WaitForFirstConsumer, RBAC and cluster-admin install failures, multipath.conf, provisioner restarts, xfs mount errors."
sources:
  - https://openebs.io/docs/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with the most frequent symptom.

**PVC Pending with an OpenEBS hostpath class.** The default local classes use `WaitForFirstConsumer`, so the volume is provisioned only after a pod using the claim is scheduled. Deploy an application that uses the PVC and it will bind. If you use this mode, **do not put `nodeName` in the Pod spec**: it bypasses the scheduler and the PVC stays Pending. Use a node selector on `kubernetes.io/hostname` instead.

**Install failures.**

- *Insufficient user rights / AKS.* Some platforms need RBAC enabled before installing, and OpenEBS needs a **cluster-admin** context because it installs service accounts and CRDs that only cluster administrators can create. Check with `kubectl auth can-i`; if you lack the context, create one and set it as current.
- *Provisioner pod restarting continuously.* The page ties this to network component misconfiguration. Check that network pods are healthy, that the provisioner's HTTPS requests reach the apiserver, use current network provider images, or try another CNI such as Calico or kube-router.
- *OpenShift multipath.* A `multipath.conf` without `find_multipaths` or a manual blacklist claims all SCSI devices. Add `find_multipaths yes` under `defaults` in `/etc/multipath.conf`, then run `multipath -w <device>` for the persistent device name.

**Runtime.** Pods that terminate or restart under heavy I/O with termination reason `NodeControllerEviction` signal node resource starvation; the workaround is more memory and CPU. Fetch the Dynamic Local Provisioner logs with `kubectl logs -n openebs -l openebs.io/component-name=openebs-localpv-provisioner`.

**xfs volume will not mount.** If a volume is created but the pod stays in ContainerCreating with a "wrong fs type, bad option, bad superblock" mount error, the `mkfs.xfs` in the driver image may be newer than the node kernel, and `dmesg` shows "Superblock has unknown incompatible features". The page's table: `bigtime` and `inobtcount` are on by default from `mkfs.xfs` 5.15 and need kernel 5.10; `nrext64` is on from `mkfs.xfs` 6.5 and needs kernel 5.19. Upgrading the node kernel is the preferred fix. Otherwise set format options, either node-wide (for LVM, `--set-string 'lvmNode.defaultFormatOptions.xfs=-i nrext64=0'`; ZFS uses `zfsNode.defaultFormatOptions.xfs`) or per StorageClass with `formatOptions`. Options apply only at first format, so an already formatted volume must be recreated.

## Checked

Method: 2026-11-08 read the raw markdown of the cited local storage troubleshooting page in full; PVC Pending, RBAC and cluster-admin, provisioner restart, multipath and eviction entries match. Added the provisioner log command and the xfs mount-failure entry the page also documents.
