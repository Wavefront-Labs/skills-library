---
id: computing-software.cloud-infrastructure-engineering.kubernetes.user-namespaces-hostusers
name: user-namespaces-hostusers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, securitycontext, user-namespaces, hostusers, pod-security-standards]
level: practitioner
status: docs-checked
description: "Run pods in user namespaces with hostUsers false so container root maps to an unprivileged host UID, with kernel and runtime requirements and limitations."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/user-namespaces/", "https://kubernetes.io/docs/tasks/configure-pod-container/user-namespaces/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User namespaces (hostUsers: false)

```yaml
apiVersion: v1
kind: Pod
spec:
  hostUsers: false
  containers:
  - name: app
    image: app:1.0
```
UID 0 inside the container maps to an unprivileged UID range on the host; the kubelet picks a range per pod so
no two pods on a node share a mapping (65536 IDs per pod by default; `userNamespaces.idsPerPod` in
`KubeletConfiguration` can raise it in multiples of 65536 from 1.33). A container breakout lands as an unprivileged
user on the node. The docs say several HIGH or CRITICAL vulnerabilities were not exploitable with user namespaces active.

## Status and requirements
- Feature `UserNamespacesSupport`: alpha 1.28, beta 1.30 (off), beta on by default 1.33, stable 1.36.
- Linux only, with idmap-mount support on the filesystem under `/var/lib/kubelet/pods/` and on every pod volume
  filesystem: in practice Linux 6.3 or later, because tmpfs gained idmap support then (service account tokens and Secrets use tmpfs).
- Runtime: containerd 2.0+ or CRI-O 1.25+ with a supporting OCI runtime (runc 1.2+, crun 1.9+; 1.13+ recommended).
- `runAsUser`, `runAsGroup` and `fsGroup` refer to IDs inside the container, so volume file ownership is unchanged when you toggle `hostUsers`.

## Limitations
- With `hostUsers: false` you cannot use other host namespaces (`hostNetwork`,
  `hostPID`, `hostIPC`), and no container can use `volumeDevices` (raw block volumes).
- Every volume filesystem must support idmap mounts; NFS volumes cannot be mounted because the Linux NFS client lacks idmap support.
- Capabilities granted to the pod are valid only inside its user namespace (for example `CAP_SYS_MODULE` has no effect and
  `CAP_SYS_ADMIN` is limited to the namespace); keep dropping capabilities you do not need.
- Pod Security admission: for pods using user namespaces the `runAsNonRoot` and `runAsUser` checks are not applied under
  Baseline or Restricted, and under Baseline `procMount` validation is relaxed too (Restricted still requires the default `procMount`).
- IDs outside the pod's range appear as the overflow ID (usually 65534) and cannot be modified.
- A custom host ID range needs a `kubelet` user, `getsubids` on the PATH and a single-line `/etc/subuid` and `/etc/subgid`
  entry for `kubelet` starting at a multiple of 65536 (at least 65536) with a count of at least `65536 x maxPods`.

## Verify
```bash
kubectl exec <pod> -- cat /proc/self/uid_map      # e.g. 0 833617920 65536; last number 65536, host start is a larger number
kubectl exec <pod> -- id                          # uid=0(root) inside
# on the node, ps shows a user different from the one `id` shows in the container
```

## Rollout
Enable per workload, starting with ones that run as root because of legacy images; that is
where the gain is largest.

## Checked

2026-10-26: kubernetes.io user-namespaces concept and task pages (v1.37 docs, kubernetes/website main 2026-10-25) and the UserNamespacesSupport feature-gate page. Confirmed: stage history (stable 1.36), kernel 6.3 idmap requirement, runtime versions, hostUsers field, per-pod non-overlapping ranges, idsPerPod from 1.33, capability limits, Pod Security relaxations, custom range requirements, uid_map verification. Corrected: the old skill said beta; the feature is stable since 1.36. Removed the unconfirmed named CVE examples and the stateless-pods remark.

Method: documentation only; no commands were run.
