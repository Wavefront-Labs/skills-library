---
id: computing-software.cloud-infrastructure-engineering.kubernetes.fsgroup-and-volume-permission-fixes
name: fsgroup-and-volume-permission-fixes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, fsgroup, fsgroupchangepolicy, securitycontext, volume-permissions, csi, ckad]
level: practitioner
status: docs-checked
description: "Fix 'permission denied' on volumes for non-root pods with fsGroup, speed up slow mounts with fsGroupChangePolicy, and know when CSI fsGroupPolicy or NFS ignore it."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes-csi.github.io/docs/support-fsgroup.html", "https://kubernetes-csi.github.io/docs/csi-driver-object.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fsGroup and fsGroupChangePolicy volume permissions

## Symptom
Non-root container (`runAsUser: 1000`) gets `permission denied` writing to a freshly
provisioned volume, because the filesystem root is owned by root:root 755.

## Fix: fsGroup
```yaml
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 2000
    fsGroupChangePolicy: OnRootMismatch
```
By default, Kubernetes recursively changes ownership and permissions of the volume's contents
to match `fsGroup` when the volume is mounted, and all container processes are also part of
supplementary group 2000. This only applies to volume types that support `fsGroup`-controlled
ownership and permissions.

## Slow pod starts on big volumes
For large volumes, checking and changing ownership and permissions can take a lot of time and
slow pod startup. `fsGroupChangePolicy: OnRootMismatch` only changes permissions and ownership if the
root directory does not match the expected ownership and permissions. `Always` (the default behaviour)
changes them every time the volume is mounted. The field is stable since Kubernetes 1.23.

## When fsGroup does nothing
- **CSI driver `fsGroupPolicy`** (in the CSIDriver object):
  - `ReadWriteOnceWithFSType` (default): applied only if the volume's `fsType` is defined and the PV's accessModes contain `ReadWriteOnce`.
  - `File`: Kubernetes may apply fsGroup regardless of fstype or access mode.
  - `None`: volumes are mounted with no modifications.
  `kubectl get csidriver -o custom-columns=NAME:.metadata.name,FSGROUP:.spec.fsGroupPolicy`
- **Volume types that do not support fsGroup-controlled ownership**: the setting has no effect;
  set ownership on the storage side or with an init container.
- **Drivers that support the CSI `VOLUME_MOUNT_GROUP` node capability** (stable since Kubernetes 1.26):
  the driver, not Kubernetes, applies the `fsGroup`, and `fsGroupChangePolicy` does not take effect.

## Alternatives when fsGroup is not possible
- Init container running as root that runs `chown -R 1000:1000 /data` once, guarded by a marker file.
- Build the image so the app's UID matches the volume's existing owner.
- SELinux: a CSIDriver with `seLinuxMount: true` (feature gate `SELinuxMountReadWriteOncePod`) lets
  Kubernetes mount a ReadWriteOncePod volume with `-o context=<label>`.

## Verify
```bash
kubectl exec <pod> -- id                       # groups include the fsGroup
kubectl exec <pod> -- ls -ld /data             # group = fsGroup
kubectl exec <pod> -- touch /data/.w && echo writable
kubectl describe pod <pod>                     # events show mount timing
```

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed: fsGroup recursive ownership change and supplementary group, fsGroupChangePolicy values and stable v1.23, VOLUME_MOUNT_GROUP delegation stable v1.26 (fsGroupChangePolicy then has no effect), fsGroupPolicy values and default, seLinuxMount semantics. Removed unconfirmed claims: group-write/setgid bits, NFS root squash advice, SMB/Azure File examples, Pod Security exemption note and the events grep.

Method: documentation only; no commands were run.
