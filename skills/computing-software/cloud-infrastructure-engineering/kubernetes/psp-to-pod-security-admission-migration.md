---
id: computing-software.cloud-infrastructure-engineering.kubernetes.psp-to-pod-security-admission-migration
name: psp-to-pod-security-admission-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, podsecuritypolicy, psp-migration, pod-security-admission, pod-security-standards, cks, upgrade]
level: advanced
status: docs-checked
description: "Migrate a cluster off PodSecurityPolicy to Pod Security Admission before 1.25: replace PSP mutations, map policies to levels, dry-run labels, audit, enforce, remove PSP."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/migrate-from-psp/", "https://kubernetes.io/docs/reference/access-authn-authz/psp-to-pod-security-standards/", "https://kubernetes.io/docs/concepts/security/pod-security-admission/", "https://kubernetes.io/docs/concepts/security/pod-security-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from PodSecurityPolicy to PSA

PSP was deprecated in 1.21 and removed in 1.25. A cluster still on 1.24 or older with PSP enabled
cannot upgrade past it without this migration. Also used when re-platforming old manifests.

## 1. Remove reliance on PSP mutation
PSP could *change* pods (default `runAsUser`, `fsGroup`, added/dropped capabilities,
seccomp/AppArmor annotations, `readOnlyRootFilesystem` defaults). PSA only validates.
Find which PSP admitted each pod and what it mutated:
```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.metadata.annotations.kubernetes\.io/psp}{"\n"}{end}' | sort -k3 | uniq -c -f2
```
Move the mutated fields into the workload manifests (or a Kyverno mutate policy), then
make PSPs non-mutating.

## 2. Pick a level per namespace
Use the PSP-to-PSS mapping table: most app namespaces fit `baseline`, hardened ones
`restricted`, system/agent namespaces `privileged`.

## 3. Dry-run before labelling
```bash
kubectl label --dry-run=server --overwrite ns --all pod-security.kubernetes.io/enforce=baseline
kubectl label --dry-run=server --overwrite ns shop pod-security.kubernetes.io/enforce=restricted
```
The server prints warnings for every existing pod that would violate.

## 4. Audit and warn first
```bash
kubectl label ns shop \
  pod-security.kubernetes.io/warn=restricted pod-security.kubernetes.io/warn-version=v1.24 \
  pod-security.kubernetes.io/audit=restricted pod-security.kubernetes.io/audit-version=v1.24
```
Watch audit logs for `pod-security.kubernetes.io/audit-violations` annotations and CI
`kubectl apply` warnings. Fix workloads.

## 5. Enforce, then remove PSP
```bash
kubectl label ns shop pod-security.kubernetes.io/enforce=restricted pod-security.kubernetes.io/enforce-version=v1.24
```
Then disable the PodSecurityPolicy admission controller in the API server admission configuration
(on 1.24 and older), delete PSP objects and their RBAC (`use` verb on `podsecuritypolicies`).

## Exemptions and defaults
Cluster defaults and exemptions go in the API server AdmissionConfiguration:
```yaml
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults: {enforce: baseline, enforce-version: latest, audit: restricted, warn: restricted}
    exemptions: {namespaces: [kube-system], usernames: [], runtimeClasses: []}
```

## Gotchas
- PSA enforce mode applies to pods only; the audit and warn modes are also applied to workload
  resources such as Deployments. An enforcement failure happens when the controller creates the
  pod, so look at the controller's events rather than at the Deployment object.
- Pin `*-version` labels during migration so a control-plane upgrade does not tighten rules.
- Fine-grained rules PSP had (allowed host paths, specific UID ranges) need Kyverno/Gatekeeper/CEL policies.

## Verify
- [ ] Every namespace has an `enforce` label (or relies on a deliberate default); no PSP objects remain; upgrade to 1.25 pre-checks pass.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: PodSecurityPolicy deprecated 1.21 and removed 1.25; PSP is mutating while PSA is not; the `kubernetes.io/psp` pod
annotation for finding which PSP admitted a pod; `kubectl label --dry-run=server --overwrite ns ...` returns warnings for existing
pods; audit and warn modes; `pod-security.kubernetes.io/audit-violations`; AdmissionConfiguration `PodSecurity` plugin
configuration with defaults and exemptions. Removed the unconfirmed `FailedCreate` event name.
Method: documentation only; no commands were run.
