---
id: computing-software.cloud-infrastructure-engineering.kubernetes.namespace-provisioning-with-defaults
name: namespace-provisioning-with-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespaces, namespace-provisioning, namespace-template, resourcequota, limitrange, networkpolicy, kyverno-generate, multi-tenancy, generate-rule]
level: practitioner
status: docs-checked
description: "Provision tenant namespaces with a standard bundle (labels, RBAC, ResourceQuota, LimitRange, default-deny NetworkPolicy, PSA) via GitOps templates or Kyverno generate rules."
sources: ["https://kubernetes.io/docs/concepts/security/multi-tenancy/", "https://kyverno.io/docs/policy-types/cluster-policy/generate/", "https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Namespace provisioning with defaults

A bare namespace has no quota, no default limits, allows all traffic and has whatever pod
security the cluster default is. Every tenant namespace should get the same bundle, created
automatically.

## The bundle
1. Namespace with labels: `team`, `cost-center`, `env`, PSA `enforce=baseline` / `warn=restricted`.
2. RoleBindings: team group → `edit` (or a custom role), CI ServiceAccount → deploy role.
3. ResourceQuota (compute + object counts + `services.loadbalancers`).
4. LimitRange (default requests/limits) so quota-bound pods without resources still admit.
5. NetworkPolicy: default-deny ingress (and egress if mature), allow DNS egress, allow from
   ingress controller namespace.
6. Optional: imagePullSecret copy, ServiceAccount with automount off.

## Option A: GitOps template (explicit, reviewable)
A Helm chart or Kustomize base `tenant-namespace` rendered per team from a values file; Argo CD
ApplicationSet (git files generator over `tenants/*.yaml`) creates one Application per tenant.
Pros: everything in git, diffable. Cons: someone has to add the file.

## Option B: Kyverno generate (automatic on namespace creation)
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: tenant-defaults}
spec:
  rules:
  - name: default-deny
    match: {any: [{resources: {kinds: [Namespace], selector: {matchLabels: {tenant: "true"}}}}]}
    generate:
      synchronize: true                     # re-creates if deleted, updates on policy change
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny
      namespace: "{{request.object.metadata.name}}"
      data:
        spec:
          podSelector: {}
          policyTypes: [Ingress]
  - name: quota
    match: {any: [{resources: {kinds: [Namespace], selector: {matchLabels: {tenant: "true"}}}}]}
    generate:
      synchronize: true
      apiVersion: v1
      kind: ResourceQuota
      name: default-quota
      namespace: "{{request.object.metadata.name}}"
      data: {spec: {hard: {requests.cpu: "20", requests.memory: 64Gi, pods: "200"}}}
```
With `synchronize: true` Kyverno reverts edits to the generated objects and recreates them if deleted.
With a `data` source and the default `orphanDownstreamOnPolicyDelete: false`, deleting the policy
also deletes the generated objects. `clone` copies an existing object (e.g. a pull secret) from a
source namespace. Kyverno's background controller needs RBAC permission to create each generated
kind. HNC (see the hierarchical-namespace-controller skill) is another option for delegated
namespace creation.

## Verify
```bash
kubectl create ns t1 && kubectl label ns t1 tenant=true team=x
kubectl get netpol,quota,limitrange,rolebinding -n t1
```
- [ ] New tenant namespaces get the full bundle within seconds; existing ones audited for drift.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Kyverno generate rules: `kyverno.io/v1` ClusterPolicy, `generate.synchronize`, `data` and `clone` sources, namespace
  templating with `{{request.object.metadata.name}}`, revert on modification, recreate on delete, policy deletion removes
  downstream unless `orphanDownstreamOnPolicyDelete: true`, background controller permissions: Kyverno generate documentation
  (website repo, main branch).
- Pod Security Admission labels `pod-security.kubernetes.io/enforce: baseline` and `warn: restricted`: namespace-labels task page.
- Argo CD ApplicationSet Git generator supports a files mode (`Git Generator: Files`): Argo CD documentation.
- Removed: Capsule as an alternative, which was not checked against its documentation.

Method: documentation only; no commands were run.
