---
id: computing-software.cloud-infrastructure-engineering.kubernetes.default-serviceaccount-hardening
name: default-serviceaccount-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-account, default-serviceaccount, automountserviceaccounttoken, rbac]
level: practitioner
status: docs-checked
description: "Lock down every namespace's default ServiceAccount: disable token automount, keep it unbound in RBAC, enforce per-workload ServiceAccounts with policy."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/", "https://kubernetes.io/docs/concepts/security/service-accounts/", "https://kyverno.io/docs/policy-types/cluster-policy/validate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening the default ServiceAccount

Every namespace gets a `default` ServiceAccount; pods without `serviceAccountName` use it and,
by default, get its token mounted at `/var/run/secrets/kubernetes.io/serviceaccount/token`.

## Disable automount
```bash
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  kubectl patch serviceaccount default -n $ns -p '{"automountServiceAccountToken": false}'; done
```
New namespaces need it too: add to namespace provisioning templates (Kyverno generate/mutate,
Capsule, or GitOps namespace charts). If the pod spec sets `automountServiceAccountToken`, the pod
setting takes precedence over the ServiceAccount's, so a pod can still opt in with `true`.

## Keep it permissionless
```bash
kubectl get rolebindings,clusterrolebindings -A -o json | jq -r '.items[] | select(any(.subjects[]?; .kind=="ServiceAccount" and .name=="default")) | "\(.metadata.namespace // "cluster")/\(.metadata.name) -> \(.roleRef.name)"'
```
Any hit is a finding: create a dedicated SA for that workload and bind there.

## Enforce per-workload ServiceAccounts
Kyverno example:
```yaml
spec:
  rules:
  - name: no-default-sa
    match: {any: [{resources: {kinds: [Pod]}}]}
    validate:
      message: "Use a dedicated ServiceAccount"
      pattern:
        spec:
          serviceAccountName: "!default"
```
Exclude system namespaces where needed. In Kyverno patterns a leading `!` means "not equal". Test
the policy with a pod that omits `serviceAccountName` as well as one that sets `default`.

## Verify
```bash
kubectl get sa default -n shop -o jsonpath='{.automountServiceAccountToken}'     # false
kubectl run t -n shop --image=busybox:1.36 --restart=Never -- sleep 60
kubectl exec -n shop t -- ls /var/run/secrets/kubernetes.io/serviceaccount 2>&1   # no such file
```
The CIS Kubernetes Benchmark has controls for default service accounts and token mounting; confirm
the control numbers in the benchmark version you audit against.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and the Kyverno docs source.
Confirmed: every namespace has a `default` ServiceAccount; `automountServiceAccountToken: false` on the ServiceAccount and the
pod-spec-takes-precedence rule; token mount path `/var/run/secrets/kubernetes.io/serviceaccount`; Kyverno `!` not-equals pattern
operator. Removed the specific CIS control numbers (numbering varies by benchmark version).
Method: documentation only; no commands were run.
