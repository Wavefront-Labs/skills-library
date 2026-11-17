---
id: computing-software.cloud-infrastructure-engineering.kubernetes.local-pv-cleanup-and-recycling
name: local-pv-cleanup-and-recycling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-raw-block-volumes, local-pv-cleanup, local-static-provisioner, local-persistent-volumes, data-sanitisation]
level: practitioner
status: docs-checked
description: "Clean and reuse released local PVs with the local static provisioner's cleaners or by hand, so the next claim gets an empty disk."
sources: ["https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/provisioner.md", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/faqs.md", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md", "https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/deployment/docker/scripts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning and recycling local PVs

## With sig-storage-local-static-provisioner
The provisioner DaemonSet discovers disks under configured directories, creates PVs, and when a
PV becomes Released (reclaim policy Delete) it cleans the disk and recreates the PV.
```yaml
# ConfigMap storageClassMap
local-nvme:
  hostDir: /mnt/disks
  mountDir: /mnt/disks
  volumeMode: Filesystem          # contents removed with rm -rf by fsclean.sh
  # volumeMode: Block
  # blockCleanerCommand: ["/scripts/blkdiscard.sh"]   # or shred.sh, dd_zero.sh, quick_reset.sh
```
The scripts shipped in the provisioner image are `blkdiscard.sh` (runs `blkdiscard`),
`shred.sh` (runs `shred` with an optional iteration count, default 3), `dd_zero.sh`,
`quick_reset.sh` (runs `mkfs` then `wipefs -a`; this is the default when
`blockCleanerCommand` is omitted) and `fsclean.sh` (removes the contents of a Filesystem-mode
volume). Choose by your erasure requirement and device type; if you have a formal data-sanitisation
requirement, check it against what each script actually does.

## By hand (no provisioner)
```bash
kubectl get pv <pv> -o jsonpath='{.spec.local.path} {.spec.nodeAffinity.required.nodeSelectorTerms[0].matchExpressions[0].values[0]}'
kubectl delete pv <pv>
# on the node
sudo find /mnt/disks/nvme1 -mindepth 1 -delete      # filesystem
# or: sudo wipefs -a /dev/nvme1n1 && sudo blkdiscard /dev/nvme1n1   # block
kubectl apply -f pv-nvme1-worker07.yaml            # recreate the PV
```

## Gotchas
- A Released PV with policy Retain is never reused automatically; that is intentional.
- Deleting the PV object does not touch the disk; wipe before recreating or the next tenant
  sees the old data.
- Replaced disks get new device names; use stable `/dev/disk/by-id` symlinks under hostDir.

## Verify
New PV is `Available`, and a test pod mounting it sees an empty filesystem.

## Checked

Checked 2026-10-27. Documentation checked: sig-storage-local-static-provisioner docs (provisioner.md, faqs.md, best-practices.md, getting-started.md) and the cleaner scripts in `deployment/docker/scripts` (master), Kubernetes website main tree persistent volumes page (v1.38 dev; v1.37 latest release). Confirmed: the provisioner cleans a Released PV and recreates it; `storageClassMap` keys `hostDir`, `mountDir`, `volumeMode`, `blockCleanerCommand`; default block cleaner `/scripts/quick_reset.sh`; the five cleaner script names and what each runs; advice to use stable `/dev/disk/by-id` names; Retain PVs need manual reclamation. Fixed: `quick_reset.sh` runs mkfs and wipefs rather than only wiping signatures. Removed as unconfirmed: speed claims for blkdiscard and the "compliance-grade" description of shred (shred results depend on the device type).

Method: documentation only; no commands were run.
