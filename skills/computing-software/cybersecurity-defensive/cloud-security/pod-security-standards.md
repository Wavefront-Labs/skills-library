---
id: computing-software.cybersecurity-defensive.cloud-security.pod-security-standards
name: pod-security-standards
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, pod-security-standards, pod-security-admission, restricted-profile, baseline-profile, securitycontext, privileged-containers, kyverno]
level: practitioner
status: docs-checked
description: "Enforce Kubernetes Pod Security Standards with Pod Security Admission labels (restricted by default), fix workloads to comply, and add policy engines for gaps."
sources: ["https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://kubernetes.io/docs/concepts/security/pod-security-admission/", "https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod Security Standards

**Goal:** pods cannot run privileged, share host namespaces, or run as root unless explicitly
exempted, closing the easiest container-escape paths.

## Profiles
- **Privileged**: no restrictions (system namespaces only).
- **Baseline**: blocks known privilege escalations (privileged, hostNetwork/PID/IPC, hostPath, added dangerous capabilities, hostPorts).
- **Restricted**: baseline plus must run as non-root, drop ALL capabilities, `allowPrivilegeEscalation: false`, seccomp `RuntimeDefault`, limited volume types.

## Enforce with Pod Security Admission (stable since Kubernetes v1.25)
```
kubectl label ns payments \
  pod-security.kubernetes.io/enforce=restricted pod-security.kubernetes.io/enforce-version=latest \
  pod-security.kubernetes.io/warn=restricted pod-security.kubernetes.io/audit=restricted
```
Roll out: `warn` and `audit` first, check warnings at deploy time and audit annotations,
then `enforce`. Label every namespace, for example through GitOps.

## Compliant pod spec
```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile: {type: RuntimeDefault}
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities: {drop: ["ALL"]}
```
Images must run as a non-root UID (set `USER 10001` in the Dockerfile).

## Gaps and exceptions
- For finer control than one profile per namespace, use **Kyverno** or **Gatekeeper** for
  per-workload exemptions, registries allow-lists, required labels, and auto-adding securityContext defaults.
- System namespaces (CNI, CSI, monitoring agents) often need privileged; isolate them and restrict who can deploy there.

## Gotchas
- Enforcement applies on pod creation; existing pods keep running until recreated - check with `kubectl label --dry-run=server --overwrite ns <ns> pod-security.kubernetes.io/enforce=restricted`, which lists violating pods.

## Checked

2026-10-28: confirmed on kubernetes.io: PSA stable since v1.25, the three profiles, Restricted requires dropping ALL capabilities and the seccomp field (RuntimeDefault allowed), hostPort restricted, the `pod-security.kubernetes.io/enforce` label and the `kubectl label --dry-run=server --overwrite` check. Removed: AdmissionConfiguration default claim, "cannot mutate pods" claim and the ReplicaSet-events tip (not confirmed).

Method: documentation only; no commands were run.

## Verify
- [ ] Every application namespace labelled enforce=restricted (or baseline with documented reason).
- [ ] A privileged test pod is rejected in an application namespace.
