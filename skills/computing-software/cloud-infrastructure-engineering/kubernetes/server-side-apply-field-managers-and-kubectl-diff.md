---
id: computing-software.cloud-infrastructure-engineering.kubernetes.server-side-apply-field-managers-and-kubectl-diff
name: server-side-apply-field-managers-and-kubectl-diff
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, server-side-apply, field-manager, managedfields, ssa-conflict, kubectl-diff, dry-run-server, kubectl-apply]
level: advanced
status: docs-checked
description: "Use server-side apply and field managers to share objects between tools, resolve apply conflicts, migrate from client-side apply, and preview with kubectl diff."
sources: ["https://kubernetes.io/docs/reference/using-api/server-side-apply/", "https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/diff/diff.go", "https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side apply, field managers and kubectl diff

## Server-side apply (SSA)
```bash
kubectl apply --server-side --field-manager=platform-ci -f manifests/
```
The apiserver tracks, per field, which **manager** set it (`metadata.managedFields`). An apply
sends a partial object containing only the fields you have an opinion about; fields you
leave out are not claimed by you, and fields owned by others are left alone. Changing a field
moves its ownership to the manager making the change. `kubectl` omits managed fields by
default:
```bash
kubectl get deploy web --show-managed-fields -o yaml
```
Do not edit `metadata.managedFields` by hand; the API server manages it.

## Conflicts
A conflict is a status error returned when an apply changes a field whose value differs
and that another manager owns. The Kubernetes docs give three ways out:
- **Drop the field** from your manifest: the value is left unchanged and the field is removed from
  your entry in `managedFields` (right answer for `replicas` when an HPA owns it).
- **Overwrite and become sole manager** with `--force-conflicts` (right answer when your tool is the
  source of truth); the field is removed from all other managers' entries.
- Keep the field with the same value as the current one to share ownership (see the docs on
  shared field management).
Appliers must send a field manager name (`--field-manager`); controllers should use SSA with their
own name so ownership is visible.

## Migrating from client-side apply
Client-side apply stored state in the `kubectl.kubernetes.io/last-applied-configuration`
annotation. Switch an object with `kubectl apply --server-side`: by default field management
transfers from client-side apply to the kubectl server-side apply manager (default field
manager name `kubectl`) without conflicts. Keep the annotation up to date first: fields not
managed by client-side apply raise conflicts (for example a replicas value changed with
`kubectl scale`). Passing a different, non-default `--field-manager` opts out of this transfer.
Going back is possible with plain `kubectl apply`, because kubectl SSA keeps the annotation
up to date (again for the default `kubectl` manager). The total size of all annotations on an
object is limited to 256 KiB, which the last-applied annotation counts toward.

## Preview: kubectl diff and dry-run=server
```bash
kubectl diff -f manifests/                       # exit 0 no differences, 1 differences found, >1 kubectl or diff failed
kubectl diff --server-side --field-manager=platform-ci -f manifests/
KUBECTL_EXTERNAL_DIFF="<your diff command>" kubectl diff -f manifests/   # custom differ; must follow the same exit codes
kubectl apply --server-side --dry-run=server -f manifests/   # server processes the request without persisting
```
`kubectl diff` compares against the result of a server-side dry run, so server defaulting and
mutating webhooks show up in the diff. Webhooks with side effects must declare
`sideEffects: NoneOnDryRun` (or `None` if they have none); otherwise the dry-run request is not
sent to the webhook and the API request fails.

## Gotchas
- How lists merge is set by the schema: `x-kubernetes-list-type` (`atomic`, `set`, `map`, with
  `x-kubernetes-list-map-keys` for `map`); declare them correctly in CRDs.
- Other tools that apply server-side use their own field manager names; give each tool a distinct,
  stable `--field-manager` so ownership shows who set what.

## Verify
- [ ] `kubectl diff` in CI is empty after deploy (no drift); no unexpected managers on critical fields.

## Checked
Checked 2026-10-24 against the kubernetes/website Server-Side Apply page (field management, conflict
options and `--force-conflicts`, `--show-managed-fields`, CSA to SSA migration and default `kubectl`
manager, list and map type markers), the Annotations page (256 KiB total), the admission-controller
reference (`sideEffects` and dry-run) and kubectl's `diff` source (exit status, `KUBECTL_EXTERNAL_DIFF`,
`--server-side`). Removed: the quoted conflict error text, the `yq`/`dyff` examples and the Argo CD/Flux notes,
which no checked documentation covers.
Method: documentation only; no commands were run.
