---
id: computing-software.cloud-infrastructure-engineering.kubernetes.securitycontext-pod-vs-container-precedence
name: securitycontext-pod-vs-container-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-security-standards, securitycontext-precedence, securitycontext, runasuser, cks]
level: practitioner
status: docs-checked
description: "Know which securityContext fields live at pod level, container level or both, how container values override pod values, and what the image USER contributes."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod vs container securityContext

## Precedence
Security settings on a Container apply only to that Container and override settings made at the
Pod level when there is overlap; container settings do not affect the Pod's volumes. The pod
value applies to containers that do not set their own. The table follows the `PodSecurityContext`
and `SecurityContext` fields in the core/v1 API.

| Field | Pod | Container |
|---|---|---|
| runAsUser, runAsGroup, runAsNonRoot | yes | yes (overrides) |
| seLinuxOptions, seccompProfile, appArmorProfile, windowsOptions | yes | yes (overrides) |
| fsGroup, fsGroupChangePolicy, supplementalGroups, supplementalGroupsPolicy, sysctls, seLinuxChangePolicy | yes | no |
| privileged, allowPrivilegeEscalation, capabilities, readOnlyRootFilesystem, procMount | no | yes |

## Example
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile: {type: RuntimeDefault}
  containers:
  - name: app
    image: acme/app:1
    securityContext:
      allowPrivilegeEscalation: false
      capabilities: {drop: [ALL]}
      readOnlyRootFilesystem: true
  - name: migrator
    image: acme/migrate:1
    securityContext:
      runAsUser: 10002          # overrides the pod's 10001 for this container only
      allowPrivilegeEscalation: false
      capabilities: {drop: [ALL]}
```

## Image USER
If `runAsUser` is unset at both levels, the container runtime uses the image's `USER`. With
`runAsNonRoot: true`, the kubelet cannot verify an image whose USER is a name rather than a
number: the container fails with `container has runAsNonRoot and image has non-numeric user (...),
cannot verify user is non-root`. Set a numeric `runAsUser` or use a numeric USER in the image.

## Pod Security Admission
The Pod Security Standards list both pod-level and container-level fields (including
`initContainers` and `ephemeralContainers`). The restricted profile requires
`allowPrivilegeEscalation` false on every container, containers to drop `ALL` capabilities,
non-root settings, and a seccomp profile set (not `Unconfined`) at pod or container level.

## Verify
```bash
kubectl exec <pod> -c migrator -- id
```
shows uid 10002, while the app container shows 10001.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Configure a Security Context for a Pod or
Container" and "Pod Security Standards", the core/v1 `PodSecurityContext` and `SecurityContext`
type definitions, and the kubelet `security_context_others.go` source (latest release v1.37.1).
Confirmed: container-over-pod override rule, which fields exist at which level, the non-numeric
USER error, restricted profile requirements. The kubelet check and error text are from source,
not the website.
Method: documentation only; no commands were run.
