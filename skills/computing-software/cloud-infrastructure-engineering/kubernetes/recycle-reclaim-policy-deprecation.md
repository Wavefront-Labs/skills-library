---
id: computing-software.cloud-infrastructure-engineering.kubernetes.recycle-reclaim-policy-deprecation
name: recycle-reclaim-policy-deprecation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, access-modes-reclaim, recycle-reclaim-policy, nfs, persistentvolume, deprecation]
level: practitioner
status: docs-checked
description: "Recognise PVs using the deprecated Recycle reclaim policy (NFS and hostPath scrub with rm -rf), and migrate them to dynamic provisioning or Retain."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#recycle", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#reclaim-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recycle reclaim policy

`persistentVolumeReclaimPolicy: Recycle` is deprecated; the docs recommend dynamic provisioning instead. If the volume plugin supports it, Recycle performs a basic scrub (`rm -rf /thevolume/*`) and makes the volume available for a new claim. kube-controller-manager has recycler settings only for NFS and hostPath.

## Problems
- A basic `rm` scrub is not a secure wipe; do not rely on it for tenant isolation.
- The recycler is a Pod created from a template. An administrator can supply a custom recycler Pod template through kube-controller-manager flags (`--pv-recycler-pod-template-filepath-nfs`, `--pv-recycler-pod-template-filepath-hostpath`, plus timeout flags such as `--pv-recycler-minimum-timeout-nfs`). The template must include a `volumes` entry; its path is replaced with the volume being recycled.

## Find them
```bash
kubectl get pv -o jsonpath='{range .items[?(@.spec.persistentVolumeReclaimPolicy=="Recycle")]}{.metadata.name}{"\n"}{end}'
```

## Migrate
- NFS: use dynamic provisioning, for example the NFS CSI driver (`kubernetes-csi/csi-driver-nfs`), which creates a subdirectory per volume and has an `onDelete` parameter (`delete` default, `retain`, `archive`), or `nfs-subdir-external-provisioner` (`archiveOnDelete`; its repository was last updated in March 2026, check its status before adopting it).
- Existing PVs: patch to `Retain` and clean up by hand once released:
```bash
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
```
- hostPath PVs: hostPath is for single-node testing only; use `local` volumes instead.

## Verify
No PV reports `Recycle`, and new PVCs get fresh directories or volumes from a provisioner.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: Recycle deprecation and scrub command, kube-controller-manager recycler flags in source, NFS CSI onDelete parameter, nfs-subdir-external-provisioner archiveOnDelete.

Method: documentation only; no commands were run.
