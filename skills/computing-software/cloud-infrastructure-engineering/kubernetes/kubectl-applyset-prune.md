---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-applyset-prune
name: kubectl-applyset-prune
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-object-management, applyset, kubectl-prune, kubectl-apply, gitops]
level: practitioner
status: docs-checked
description: "Prune resources removed from manifests with kubectl apply --prune using ApplySets instead of risky label-based pruning, with dry runs first."
sources: ["https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/#alternative-kubectl-apply-f-directory-prune", "https://kubernetes.io/blog/2023/05/09/introducing-kubectl-applyset-pruning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl apply --prune with ApplySets

Plain `kubectl apply -f dir/` never deletes objects you removed from the directory. Pruning
fixes that. Both pruning modes are still alpha in current Kubernetes docs.

## ApplySet (alpha since kubectl v1.27, needs env var)
```bash
export KUBECTL_APPLYSET=true
kubectl apply -n shop --prune --applyset=shop-app -f manifests/ --dry-run=server
kubectl apply -n shop --prune --applyset=shop-app -f manifests/
```
The parent object is a Secret by default (kubectl creates it if missing), or a ConfigMap with
`--applyset=configmaps/<name>`, or a custom resource whose CRD carries the label
`applyset.kubernetes.io/is-parent-type: true` (you create that parent yourself; reference it as
`--applyset=<resource>.<group>/<name>`). kubectl labels each member
`applyset.kubernetes.io/part-of=<parentID>`, records the resource types and namespaces on the
parent, and at the end of the apply queries those for members no longer in the manifests.

Restrictions from the docs:
- Each object can belong to at most one set.
- `--namespace` is required for any namespaced parent, including the default Secret, so a set
  spanning several namespaces needs a cluster-scoped custom resource parent.
- Use a unique ApplySet name per directory.

## Allowlist (label-based) prune (avoid)
```bash
kubectl apply --prune -l app=shop -f manifests/ --prune-allowlist=core/v1/ConfigMap --prune-allowlist=apps/v1/Deployment
```
Available since kubectl v1.5, still alpha. What is pruned depends on `--prune-allowlist`,
`--selector` and `--namespace`, found by dynamic discovery; changing those flags between runs can
delete or keep objects unexpectedly. The default allowlist is a partial list of namespaced and
cluster-scoped types. A live object is deleted if it matches, has no manifest in the directory
and has a `kubectl.kubernetes.io/last-applied-configuration` annotation. Use `--all` instead of
`-l` to select all previously applied objects of the allowlisted types. The ApplySet mode was
introduced to replace it.

## Safety
- Run with `--dry-run=server` first and read what kubectl says it would prune.
- Run prune only against the root directory holding all manifests; applying a subdirectory can
  delete previously applied objects that are not in it.
- For larger setups, Argo CD or Flux pruning with sync status is easier to audit.

## Verify
Remove one manifest, run with `--dry-run=server`, see exactly that object reported as pruned,
then run for real.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Declarative management of Kubernetes
objects using configuration files" (current docs, v1.37 era; latest release v1.37.1).
Confirmed: ApplySet mode alpha since v1.27 with `KUBECTL_APPLYSET=true`; Secret default parent,
`configmaps/<name>` form, CRD label for custom parents; `part-of` label; the three restrictions;
allowlist mode alpha since v1.5 with its flags and warnings. Removed unconfirmed claims (the
"deprecated" wording, name-change orphaning).
Method: documentation only; no commands were run.
