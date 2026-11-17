---
id: computing-software.cloud-infrastructure-engineering.kubernetes.capsule-tenant-operator
name: capsule-tenant-operator
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, capsule, tenant-operator, multi-tenancy, namespace-as-a-service, resourcequota, rbac, self-service-namespaces]
level: advanced
status: docs-checked
description: "Run soft multi-tenancy with Capsule: Tenant objects that let teams self-create namespaces under shared quotas, enforced classes, registries and node pools, plus capsule-proxy."
sources: ["https://projectcapsule.dev/docs/operating/setup/installation/", "https://projectcapsule.dev/docs/tenants/namespaces/", "https://github.com/projectcapsule/capsule", "https://github.com/projectcapsule/capsule-proxy"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Capsule tenant operator

## Model
A **Tenant** is a cluster-scoped group of namespaces with owners. Owners create and delete
their own namespaces (no ticket to the platform team); Capsule's webhook stamps every new
namespace with the tenant's policies. Alternatives: HNC (namespace hierarchy) and vcluster
(virtual control plane, harder isolation).

## Install
```bash
helm repo add projectcapsule https://projectcapsule.github.io/charts
helm install capsule projectcapsule/capsule -n capsule-system --create-namespace
# or from OCI: helm install capsule oci://ghcr.io/projectcapsule/charts/capsule -n capsule-system --create-namespace
```
Users must be listed in the `users` property of the `CapsuleConfiguration` (named `default` by the chart;
the chart default is the group `projectcapsule.dev`; the older `userGroups` and `userNames` properties are
deprecated) for their requests to be handled by Capsule; map your IdP group there.

## Tenant
```yaml
apiVersion: capsule.clastix.io/v1beta2
kind: Tenant
metadata: {name: payments}
spec:
  owners:
  - {kind: Group, name: team-payments}
  namespaceOptions: {quota: 10}
  resourceQuotas:
    scope: Tenant                      # one quota shared across all tenant namespaces
    items:
    - hard: {requests.cpu: "40", requests.memory: 80Gi, persistentvolumeclaims: "30"}
  limitRanges:
    items:
    - limits: [{type: Container, default: {cpu: 500m, memory: 512Mi}, defaultRequest: {cpu: 100m, memory: 128Mi}}]
  networkPolicies:
    items:
    - policyTypes: [Ingress]
      podSelector: {}
      ingress: [{from: [{namespaceSelector: {matchLabels: {capsule.clastix.io/tenant: payments}}}]}]
  nodeSelector: {pool: payments}
  storageClasses: {allowed: [gp3]}
  ingressOptions: {allowedClasses: {allowed: [internal]}}
  containerRegistries: {allowed: [ghcr.io/acme]}
```
`v1beta2` is the storage version of the Tenant CRD and `v1beta1` is still served. Field names evolve between
releases (newer releases add fields such as `rules` and `permissions`); confirm with `kubectl explain tenant.spec`.

## Owner experience
```bash
kubectl create ns payments-dev        # as a member of team-payments
kubectl get tenant payments -o jsonpath='{.status.namespaces}'
```
Plain `kubectl get ns` is forbidden for tenants (cluster-scoped list). **capsule-proxy** in
front of the API server filters cluster-scoped lists (namespaces, nodes, storage classes)
to what the tenant may see; point tenant kubeconfigs at it.

## Gotchas
- `resourceQuotas.scope` accepts `Tenant` (the default, shared across the tenant's namespaces) or `Namespace`.
- Tenants share nodes and the kernel unless `nodeSelector`/taints dedicate pools; pair with
  PSA restricted and default-deny NetworkPolicy.
- By default namespaces are deleted when the Tenant is deleted, and a namespace cannot be moved between
  tenants; set `spec.preventDeletion: true` on a Tenant to decline accidental deletion requests.

## Verify
- [ ] Tenant owner can create a namespace; it carries the tenant's quota, LimitRange and NetworkPolicy.
- [ ] Creating an Ingress with a non-allowed class or a pod from a non-allowed registry is denied.

## Checked

Checked on 2026-10-26 against `projectcapsule/capsule` main (chart README, Tenant and CapsuleConfiguration CRDs; pushed 2026-10-25) and the `projectcapsule/website` docs (installation, tenants/namespaces, proxy).
Confirmed: Tenant `capsule.clastix.io/v1beta2` (storage) and `v1beta1` served; spec fields `owners`, `namespaceOptions.quota`, `resourceQuotas.scope`/`items`, `limitRanges.items`, `networkPolicies.items`, `nodeSelector`, `storageClasses.allowed`, `ingressOptions.allowedClasses`, `containerRegistries.allowed`, `preventDeletion`; `CapsuleConfiguration` name `default` and `users` default group `projectcapsule.dev`; Helm repo URL and OCI install; the `capsule.clastix.io/tenant` label; Capsule Proxy exists to let tenants list cluster-scoped resources.
Wrong in the draft: namespaces are deleted with the Tenant, not kept. Removed as unconfirmed: the Kiosk archived claim and the quota overshoot claim.

Method: documentation only; no commands were run.
