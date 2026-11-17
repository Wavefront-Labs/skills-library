---
id: computing-software.cloud-infrastructure-engineering.kubernetes.namespacelifecycle-admission
name: namespacelifecycle-admission
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespaces, namespacelifecycle, admission-control, terminating-namespace, kube-system]
level: practitioner
status: docs-checked
description: "Understand the NamespaceLifecycle admission plugin, which blocks objects in missing or terminating namespaces and protects default, kube-system and kube-public."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#namespacelifecycle", "https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NamespaceLifecycle admission

Enabled by default (it is in the API server's default plugin list). It enforces:
1. No new objects in a namespace that does not exist:
   `Error from server (NotFound): namespaces "foo" not found`.
2. No new objects in a namespace being deleted:
   `unable to create new content in namespace foo because it is being terminated`.
3. The namespaces `default`, `kube-system` and `kube-public` cannot be deleted.

## Consequences
- Deploy tools must create the namespace first (`kubectl create ns`, Helm `--create-namespace`,
  Argo CD `CreateNamespace=true`); a manifest that contains both a Namespace and objects in it
  needs the Namespace to be created before those objects, so order them or use a tool that does.
- While a namespace is `Terminating`, controllers that keep recreating objects (for example an
  operator in another namespace) get errors in their logs until deletion finishes.
- Recreating a namespace with the same name must wait for termination to complete.

## Stuck Terminating namespaces
NamespaceLifecycle is not the cause; the namespace controller is waiting on finalizers or an
unavailable API group:
```bash
kubectl get ns foo -o jsonpath='{.status.conditions}' | jq
```
Conditions like `NamespaceDeletionDiscoveryFailure` (resource discovery errors during namespace
deletion) and `NamespaceContentRemaining` (resources still in the namespace) show what the
namespace controller is waiting for; a discovery failure usually points at a broken APIService.

## Do not
Disable the plugin; the Kubernetes docs strongly recommend running it, because namespace
deletion removes all objects in the namespace and this plugin enforces the integrity of that process.

## Verify
```bash
kubectl delete ns kube-public --dry-run=server
```
must fail with `this namespace may not be deleted` (a Forbidden error from the plugin).

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: plugin behaviour (rejects new objects in a terminating or missing namespace; protects `default`, `kube-system` and
`kube-public`); the "unable to create new content in namespace ... because it is being terminated" and "this namespace may not be
deleted" messages (lifecycle admission.go); default-enabled plugin list; NamespaceCondition types (core/v1 types.go); Helm
`--create-namespace` flag and Argo CD `CreateNamespace=true`. Wrong in the original: "kubectl applies Namespaces first" (removed, unconfirmed).
Method: documentation only; no commands were run.
