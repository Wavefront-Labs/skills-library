---
id: computing-software.cloud-infrastructure-engineering.kubernetes.system-namespaces-and-resource-scoping
name: system-namespaces-and-resource-scoping
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespaces, system-namespaces, kube-node-lease, kube-public, api-resources, namespaced-resources, cluster-scoped, cka]
level: practitioner
status: docs-checked
description: "Know the built-in namespaces (default, kube-system, kube-public, kube-node-lease) and which resources are namespaced vs cluster-scoped, using kubectl api-resources."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_api-resources/", "https://kubernetes.io/docs/concepts/architecture/leases/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System namespaces and resource scoping

## Built-in namespaces
| Namespace | Purpose | Rules of thumb |
|---|---|---|
| `default` | namespace for objects created without one | don't run workloads here; easy to deploy into by accident |
| `kube-system` | objects created by the Kubernetes system | no app workloads; keep RBAC tight |
| `kube-public` | readable by all clients including unauthenticated ones (a convention, not a requirement); kubeadm creates the `cluster-info` ConfigMap here | don't put anything sensitive |
| `kube-node-lease` | one `Lease` per node, used for kubelet heartbeats | one Lease per node, so its size follows the node count |
Others you'll see: `kube-flannel`, `calico-system`, `gatekeeper-system`, etc. from add-ons.
Names starting with `kube-` are reserved by convention for the system; don't create your own.
All namespaces get the label `kubernetes.io/metadata.name=<name>` automatically.

## Namespaced vs cluster-scoped
```bash
kubectl api-resources --namespaced=true -o name | head -40
kubectl api-resources --namespaced=false -o name
kubectl api-resources --api-group=rbac.authorization.k8s.io -o wide   # verbs, shortnames, kind
kubectl api-resources --verbs=list --namespaced -o name | xargs -n1 kubectl get -n team-a --ignore-not-found --show-kind   # everything in a namespace
```
Cluster-scoped examples: Namespace, Node, PersistentVolume, StorageClass, ClusterRole,
ClusterRoleBinding. Namespaced examples: Pods, Deployments, Services, Roles, RoleBindings,
ResourceQuota, Leases. Run `kubectl api-resources --namespaced=false` for the full list of
cluster-scoped kinds on your cluster.
Implications: namespace-based scoping does not apply to cluster-wide objects, so a namespaced
Role cannot grant access to cluster-scoped resources (that needs a ClusterRole).

## Gotchas
- Use the api-resources loop above rather than guessing which kinds exist in a namespace.

## Verify
- [ ] `kubectl get pods -n default` empty in production clusters; no non-system workloads in kube-system.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Initial namespaces `default`, `kube-system`, `kube-public` (readable by all clients, convention), `kube-node-lease`
  (one Lease per node for heartbeats), reserved `kube-` prefix and the automatic `kubernetes.io/metadata.name` label:
  namespaces page.
- `kubectl api-resources` flags `--namespaced`, `--api-group`, `--verbs`, `-o wide`: kubectl api-resources reference.
- `cluster-info` ConfigMap created in `kube-public` by kubeadm: kubeadm implementation details page.
- Cluster-scoped versus namespaced examples: namespaces page and RBAC page.
- Removed: the `kubernetes` Service remark, the "cluster takeover" claim, the "never delete leases" advice, the long kind
  lists, `kubectl get all` coverage and CRD scope immutability, none of which the checked pages state.

Method: documentation only; no commands were run.
