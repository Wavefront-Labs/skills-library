---
id: computing-software.cloud-infrastructure-engineering.external-dns.watching-multiple-namespaces
name: watching-multiple-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, namespace-flag, rolebinding, multi-namespace-watch, namespaced-rbac]
level: practitioner
status: docs-checked
description: "Limit ExternalDNS to several namespaces with repeated --namespace, supported sources, per-namespace RoleBindings, cluster-scoped exceptions and watch cost."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/multiple-namespaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Watching multiple namespaces

Default is every namespace. Limit with `--namespace`, repeated or comma separated:

```sh
--namespace=team-a --namespace=team-b
--namespace=team-a,team-b
```

Only sources marked `multiple` in the Namespace column of the supported-sources table accept several values; with any other source ExternalDNS refuses to start given more than one.

**RBAC.** It opens one watch per namespace, so a ClusterRole is not required for namespaced resources. Keep the ClusterRole for rules and bind it per namespace:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: external-dns
  namespace: team-a # repeat for team-b
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-dns
subjects:
  - kind: ServiceAccount
    name: external-dns
    namespace: external-dns
```

Cluster-scoped resources still need a `ClusterRoleBinding`, for example nodes for the `pod` source and for `NodePort` Services.

**Referenced objects** across namespaces are found only if their namespace is watched. With Istio sources, also watch the gateway namespace (often `istio-system`).

**Cost:** one watch per namespace per resource type uses more API server connections and memory than one cluster-wide watch. To read the whole cluster, omit `--namespace` and narrow with `--label-filter` or `--annotation-filter`.

## Checked

2026-11-04. Confirmed against the ExternalDNS Watching Multiple Namespaces page: flag forms, multiple-namespace sources, RBAC example, cluster-scoped exceptions, referenced objects and cost. Reworded one RBAC sentence to match the page.
Method: documentation only; no commands were run.
