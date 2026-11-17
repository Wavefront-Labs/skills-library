---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-runasuser-runasgroup-supplementalgroups
name: pod-runasuser-runasgroup-supplementalgroups
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, securitycontext, runasuser, supplementalgroups, fsgroup, runasnonroot]
level: practitioner
status: docs-checked
description: "Set runAsUser, runAsGroup, supplementalGroups and supplementalGroupsPolicy correctly, how they interact with image USER, volumes and runAsNonRoot checks."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# runAsUser, runAsGroup, supplementalGroups

```yaml
spec:
  securityContext:
    runAsUser: 10001
    runAsGroup: 10001
    runAsNonRoot: true
    fsGroup: 10001
    supplementalGroups: [2000]
    supplementalGroupsPolicy: Strict
  containers:
  - name: app
    image: app:1.0
    securityContext:
      allowPrivilegeEscalation: false
```

## Semantics
- `runAsUser`: the user ID for processes in the container (container-level values override
  the pod's).
- `runAsGroup`: primary group ID. If omitted, the primary group ID of the containers is root (0).
- `fsGroup` adds that GID to the container processes' supplementary groups and sets group
  ownership of supported volumes and files created in them.
- `supplementalGroups`: additional group IDs; omitted means empty.
- `supplementalGroupsPolicy`: `Merge` (default) merges group membership from `/etc/group` in the
  image for the container's primary user, which the docs warn can cause security problems
  with volumes; `Strict` attaches only the IDs in `fsGroup`, `supplementalGroups` and
  `runAsGroup`. The field was alpha in 1.31, beta in 1.33 and stable in 1.35, per the
  feature gate definition.
- `runAsNonRoot: true`: the kubelet refuses to start a container that would run as UID 0. With an
  image `USER appuser` (a name, not a number) and no `runAsUser`, the kubelet cannot verify
  it and fails with `image has non-numeric user (appuser), cannot verify user is non-root`.
  Use a numeric `USER` in the image or set `runAsUser`.

## Volumes
- By default Kubernetes recursively changes ownership and permissions of each volume's
  contents to match `fsGroup` when the volume is mounted; this can slow Pod startup on large
  volumes. `fsGroupChangePolicy: OnRootMismatch` only changes them if the volume root does not
  match, `Always` is the default behaviour. The field applies only to volume types that support
  `fsGroup`-controlled ownership and has no effect on `secret`, `configMap` and `emptyDir`.
- A CSI driver that supports the `VOLUME_MOUNT_GROUP` capability applies `fsGroup` itself; then
  `fsGroupChangePolicy` has no effect.

## Verify
```bash
kubectl exec <pod> -- id        # for the example: uid=10001 gid=10001 groups include 10001 and 2000
```
The restricted Pod Security Standard requires running as non-root and forbids `runAsUser: 0`.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Configure a Security Context for a Pod or
Container", "Pod Security Standards", the kubelet `security_context_others.go` source and the
`SupplementalGroupsPolicy` gate definition in `kube_features.go` (latest release v1.37.1).
Confirmed: default root primary group, `/etc/group` merging and `Strict` semantics, `fsGroup`
behaviour and `fsGroupChangePolicy` values and limits, non-numeric USER error, restricted
profile rule. Corrected the policy stage to stable in 1.35 and removed the unconfirmed
hostPath and NFS `fsGroup` claim.
Method: documentation only; no commands were run.
