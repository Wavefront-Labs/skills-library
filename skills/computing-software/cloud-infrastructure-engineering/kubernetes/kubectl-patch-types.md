---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-patch-types
name: kubectl-patch-types
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-patch, strategic-merge, merge-patch, json-patch, subresource-patch, cka]
level: practitioner
status: docs-checked
description: "Choose the right kubectl patch type: strategic merge (list merge keys), JSON merge (replaces lists), JSON patch (precise ops), plus patching status/scale subresources and CRDs."
sources: ["https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_patch/", "https://datatracker.ietf.org/doc/html/rfc6902", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd", "https://github.com/kubernetes/community/blob/master/contributors/devel/sig-api-machinery/strategic-merge-patch.md", "https://datatracker.ietf.org/doc/html/rfc6901"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl patch types

## Strategic merge patch (default `--type=strategic`)
Kubernetes-aware: lists with a **patchMergeKey** (containers by `name`, ports by
`containerPort`, env by `name`, volumes by `name`) are merged by key, not replaced.
```bash
kubectl patch deploy web -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"myapp:1.9"}]}}}}'
kubectl patch deploy web -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","env":[{"name":"LOG","value":"debug"}]}]}}}}'
# delete a list element with a directive
kubectl patch deploy web -p '{"spec":{"template":{"spec":{"containers":[{"name":"sidecar","$patch":"delete"}]}}}}'
```
**Not supported for custom resources** (`kubectl patch --help` says so). Use merge or json for custom resources.

## JSON merge patch (`--type=merge`, RFC 7386)
Maps merge; **lists are replaced entirely**; `null` deletes a key.
```bash
kubectl patch widget w1 --type=merge -p '{"spec":{"size":3,"debug":null}}'
kubectl patch pvc data --type=merge -p '{"metadata":{"finalizers":null}}'     # careful: removes all finalizers
```

## JSON patch (`--type=json`, RFC 6902)
Explicit ops with paths; the only way to touch a list element by index or remove one item.
```bash
kubectl patch deploy web --type=json -p='[
 {"op":"replace","path":"/spec/replicas","value":4},
 {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--verbose"},
 {"op":"remove","path":"/spec/template/spec/tolerations/1"},
 {"op":"test","path":"/metadata/labels/env","value":"prod"}]'
```
`~1` escapes `/` in keys (`/metadata/annotations/example.com~1owner`), `~0` escapes `~`. `test`
makes the patch conditional (fails if not matching).

## Subresources
```bash
kubectl patch deploy web --subresource=scale --type=merge -p '{"spec":{"replicas":5}}'
kubectl patch widget w1 --subresource=status --type=merge -p '{"status":{"phase":"Ready"}}'
```

## Tips
- `--dry-run=server -o yaml` to preview the result.
- Patch from a file: `kubectl patch deploy web --patch-file=patch.yaml`.
- For declarative ownership prefer `kubectl apply --server-side`; patches are for surgical fixes.

## Verify
- [ ] The resulting object (`kubectl get -o yaml`) has exactly the intended change; no list wiped by a merge patch.

## Checked
Checked 2026-10-24 against the Kubernetes documentation (website main, v1.37) and kubectl source (main): `--type` values strategic, merge and json; strategic merge not supported for custom resources; `--subresource` and `--patch-file` flags; patchMergeKey for containers (name), ports (containerPort), env (name) and volumes (name) in the core/v1 types; `$patch: delete` directive; RFC 6901 `~0`/`~1` escapes; RFC 6902 operations, `test` failure and `/-` append. Removed the unconfirmed error text and the `1.24+` version gate.
Method: documentation only; no commands were run.
