---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-security-admission-rollout
name: pod-security-admission-rollout
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-security-admission, pod-security-labels, enforce-audit-warn, admissionconfiguration-podsecurity, psa-exemptions, psa-dry-run, cks]
level: practitioner
status: docs-checked
description: "Roll out Pod Security Admission: enforce/audit/warn namespace labels and versions, cluster defaults and exemptions, and server dry-run before enforcing."
sources: ["https://kubernetes.io/docs/concepts/security/pod-security-admission/", "https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/", "https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-admission-controller/", "https://kubernetes.io/docs/reference/labels-annotations-taints/audit-annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod Security Admission rollout

## Namespace labels
```bash
kubectl label ns team-a \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/enforce-version=v1.31 \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=latest \
  pod-security.kubernetes.io/audit=restricted
```
- `enforce` rejects **pods** (not workload resources such as Deployments: enforce mode is applied
  only to the resulting pods, so a controller's pod creation fails; check the controller's events).
- `warn` returns a user-facing warning but allows the request; `warn` and `audit` are also applied
  to workload resources (their pod templates), not only to pods.
- `audit` adds an audit annotation to the audit event but allows the request.
- Pin `enforce-version` so a cluster upgrade doesn't tighten rules unexpectedly; let `warn`
  run at `latest`.

## Dry-run before enforcing
```bash
kubectl label --dry-run=server --overwrite ns team-a pod-security.kubernetes.io/enforce=restricted
# the server runs the checks against existing pods and returns warnings for any that would violate the level
kubectl label --dry-run=server --overwrite ns --all pod-security.kubernetes.io/enforce=baseline   # whole cluster
```

## Cluster defaults and exemptions (AdmissionConfiguration)
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults:                       # for namespaces without labels
      enforce: baseline
      enforce-version: latest
      audit: restricted
      warn: restricted
    exemptions:
      usernames: []
      runtimeClasses: []
      namespaces: [kube-system, cilium, gpu-operator]
```
apiserver flag `--admission-control-config-file=<file>` (mount it into the static pod).
Exempt usernames, runtimeClasses and namespaces skip all `enforce`, `audit` and `warn` behaviour — keep the list short and tightly RBAC'd; prefer labelling
those namespaces `enforce=privileged` explicitly so it's visible.

## Rollout plan
1. Cluster-wide `audit`/`warn` = restricted; collect violations (audit log annotation
   `pod-security.kubernetes.io/audit-violations`).
2. Fix workloads (securityContext: runAsNonRoot, drop ALL, seccompProfile RuntimeDefault,
   allowPrivilegeEscalation false).
3. Enforce baseline everywhere, restricted per namespace once clean (server dry-run first).
4. Lock label changes: only platform admins may `patch` namespaces (labels are the control!).

## Verify
- [ ] `kubectl get ns -L pod-security.kubernetes.io/enforce` shows no unlabelled app namespace.
- [ ] Creating a privileged pod in an app namespace is rejected.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: label names `pod-security.kubernetes.io/<mode>` and `<mode>-version` with levels privileged/baseline/restricted and
version `vX.Y` or `latest`; mode semantics and workload-resource behaviour; `--dry-run=server` namespace label evaluation (also with
`--all`); AdmissionConfiguration `PodSecurity` plugin with `pod-security.admission.config.k8s.io/v1`, `defaults` keys and
`exemptions` (usernames, runtimeClasses, namespaces); exemptions skip all modes; audit annotation
`pod-security.kubernetes.io/audit-violations`; PodSecurity stable since 1.25. Removed the unconfirmed `FailedCreate` event name and
the invented sample warning text.
Method: documentation only; no commands were run.
