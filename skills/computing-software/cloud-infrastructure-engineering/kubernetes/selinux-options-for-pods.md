---
id: computing-software.cloud-infrastructure-engineering.kubernetes.selinux-options-for-pods
name: selinux-options-for-pods
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, runtime-security, selinux, selinuxoptions, mcs-labels, volume-relabeling]
level: practitioner
status: docs-checked
description: "Use pod and container seLinuxOptions (type, MCS level), understand volume relabeling and the SELinux mount option change, and debug AVC denials."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#assign-selinux-labels-to-a-container", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://github.com/containers/container-selinux"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELinux options for pods

On SELinux-enforcing nodes the container runtime labels each container process and its files;
`seLinuxOptions` in the pod or container `securityContext` lets you set the level, type, user and
role (see the Kubernetes security context docs).

## Setting labels
```yaml
spec:
  securityContext:
    seLinuxOptions:
      level: "s0:c100,c200"        # same level for all pods that must share a volume
  containers:
  - name: agent
    image: acme/agent:1
    securityContext:
      seLinuxOptions:
        type: spc_t               # super-privileged container type; avoid unless required
```
The Pod Security baseline level (and so restricted too) allows only an undefined type,
`container_t`, `container_init_t`, `container_kvm_t` and `container_engine_t` (the last since
Kubernetes 1.31); `spc_t` is not allowed, and setting a custom SELinux `user` or `role` is forbidden.

## Volumes
By default the container runtime relabels volume content recursively, which slows pod start on
large volumes. Kubernetes can instead apply the label with the mount option `-o context=<label>`
when the pod uses a PersistentVolumeClaim, has `seLinuxOptions` set, `seLinuxChangePolicy` is
unset or `MountOption`, and the volume is a CSI volume whose CSIDriver sets `spec.seLinuxMount: true`
(or legacy iscsi/rbd/fc). Stages: `SELinuxMountReadWriteOncePod` stable 1.36; `SELinuxChangePolicy`
stable 1.36; `SELinuxMount` (all eligible volumes) stable 1.37. With the mount option, all pods
that use the volume concurrently on a node must have the same label, otherwise the later pod waits in
`ContainerCreating`; set `spec.securityContext.seLinuxChangePolicy: Recursive` to opt a pod out of
the optimisation.

## Debugging denials
Look for AVC denials in the node's audit log and compare the process and file labels with your
distribution's SELinux tools. Typical denial: two pods with different MCS levels writing the same
NFS or hostPath directory.
Fix by giving both the same level, not by setting `spc_t` or disabling SELinux.

## Verify
Check the process label on the node with your distribution's SELinux tooling and compare it with the
`seLinuxOptions` you set.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: Pod Security baseline SELinux type allow-list (container_engine_t since 1.31) and user/role ban; `seLinuxChangePolicy`
values and the mount-option conditions, CSIDriver `seLinuxMount`; feature gate stages for SELinuxMountReadWriteOncePod,
SELinuxChangePolicy and SELinuxMount. Wrong in the original: the allow-list was attributed to the restricted level (it is the baseline
level) and the volume relabeling stages were vague. Removed unconfirmed node-debug commands and the claim that MCS levels are
unique per container (check your runtime's documentation).
Method: documentation only; no commands were run.
