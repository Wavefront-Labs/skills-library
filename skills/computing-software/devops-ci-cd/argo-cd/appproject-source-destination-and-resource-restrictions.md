---
id: computing-software.devops-ci-cd.argo-cd.appproject-source-destination-and-resource-restrictions
name: appproject-source-destination-and-resource-restrictions
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, source-repos, destination-restrictions, cluster-resource-whitelist, namespace-resource-blacklist, appproject-restrictions]
level: advanced
status: docs-checked
description: "Lock down Argo CD AppProjects: allowed sourceRepos, destination clusters and namespaces with negation, cluster and namespace resource allow/deny lists, and source namespaces."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/projects/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/project-specification/", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/project.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppProject restrictions

The `default` project allows any repo, any cluster, any resource. Tenants must get their own project.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata: { name: payments, namespace: argocd }
spec:
  description: Payments team
  sourceRepos:
    - https://github.com/acme/payments-*.git
    - '!https://github.com/acme/payments-sandbox.git'     # negation
  destinations:
    - { name: prod-eu, namespace: 'payments-*' }
    - { name: '*', namespace: '!kube-system' }             # deny pattern
  clusterResourceWhitelist: []                              # no cluster-scoped resources at all
  namespaceResourceBlacklist:
    - { group: '', kind: ResourceQuota }
    - { group: '', kind: LimitRange }
    - { group: networking.k8s.io, kind: NetworkPolicy }
  sourceNamespaces: [payments]                              # apps-in-any-namespace
  orphanedResources: { warn: true }
```

## Semantics
- `sourceRepos`, `destinations`: glob patterns; a `!`-prefixed (deny) entry rejects the source or destination even if another pattern allows it.
- Cluster-scoped resources are restricted by an allow list (`clusterResourceWhitelist`; empty means none allowed), namespaced ones by a deny list. A common cluster entry is `- { group: '', kind: Namespace }` with `CreateNamespace=true`.
- Namespaced kinds are allowed unless in `namespaceResourceBlacklist` (or not in a `namespaceResourceWhitelist` if you use one).

## CLI
```bash
argocd proj create payments -d https://kubernetes.default.svc,payments -s https://github.com/acme/payments.git
argocd proj add-destination payments prod-eu 'payments-*' --name   # --name: second argument is a cluster name
argocd proj allow-cluster-resource payments '' Namespace
argocd proj deny-namespace-resource payments '' ResourceQuota
```

## Gotchas
- A wildcard destination matches every cluster including in-cluster, so deny the Argo CD namespace (`'!argocd'`) explicitly.
- Keep AppProjects in Git, managed by the platform team's app, not editable by tenants.

## Verify
- [ ] An app in project `payments` trying to create a ClusterRole is refused as not permitted by the project.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: AppProject fields (`sourceRepos`, `destinations` with `name`/`namespace`, `clusterResourceWhitelist`, `namespaceResourceBlacklist`, `sourceNamespaces`, `orphanedResources.warn`) against the reference project.yaml, negation with `!`, cluster-scoped allow list versus namespaced deny list, `argocd proj add-destination --name`. Removed unconfirmed error-message text and two remarks no document states.

Method: documentation only; no commands were run.
