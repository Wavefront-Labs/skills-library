---
id: computing-software.cloud-infrastructure-engineering.kubernetes.client-go-and-kubectl-version-compatibility
name: client-go-and-kubectl-version-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, client-library-skew, client-go-compatibility, kubectl-skew, version-skew, client-go, kubectl]
level: practitioner
status: docs-checked
description: "Keep kubectl within +/-1 minor of the apiserver and pin client-go/controller-runtime to the cluster range your controllers actually talk to; detect and fix skew breakage."
sources: ["https://kubernetes.io/releases/version-skew-policy/#kubectl", "https://github.com/kubernetes/client-go#compatibility-matrix", "https://github.com/kubernetes-sigs/controller-runtime#compatibility"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client-go and kubectl version compatibility

## The rules
- **kubectl**: supported within one minor (older or newer) of kube-apiserver. Against a 1.31
  apiserver, kubectl 1.30, 1.31 and 1.32 are supported. If apiserver instances in an HA
  cluster differ by a minor, the supported kubectl range narrows to the overlap. `kubectl
  version` prints a version-skew warning on stderr when client and server are outside the
  window (`--warnings-as-errors` turns it into an error).
- **client-go**: `k8s.io/client-go` `v0.N.x` corresponds to Kubernetes `1.N`. The client-go
  README says older clients work with many cluster versions because Kubernetes is backwards
  compatible with clients: everything both sides share works, but only the matching minor has
  exactly the same features and API objects. Alpha APIs may vanish or change in one release,
  and APIs the server removed (for example the `policy/v1beta1` PodDisruptionBudget, no longer
  served since v1.25) stop working on newer servers.
- **controller-runtime** is tested against one client-go minor per release (CR v0.19 with
  k8s.io/* v0.31, v0.20 with v0.32, v0.21 with v0.33 ... see its README table), and the
  maintainers say other combinations work only by chance. Upgrade them together.

## Check what you have
```bash
kubectl version -o yaml              # clientVersion + serverVersion; gitVersion minor matters
go list -m k8s.io/client-go k8s.io/api k8s.io/apimachinery sigs.k8s.io/controller-runtime
```
Keep `k8s.io/client-go`, `k8s.io/api` and `k8s.io/apimachinery` on the same `v0.N.x`; the
controller-runtime README says its compatible versions are listed in its `go.mod`.

## Upgrading a controller's client
```bash
go get k8s.io/client-go@v0.N.x k8s.io/api@v0.N.x k8s.io/apimachinery@v0.N.x
go get sigs.k8s.io/controller-runtime@<release built on that client-go>
go mod tidy && go build ./... && go test ./...
```
Then test against the oldest and newest cluster minor you support. Check the client-go
README for which client-go branches are still maintained.

## Managing many kubectl versions
- Keep one kubectl binary per cluster minor and select by context; pin kubectl in CI images
  to the cluster minor, not `latest`.

## Gotchas
- kubectl caches API discovery under `$HOME/.kube/cache` (override with the `KUBECACHEDIR`
  environment variable or `--cache-dir`); stale discovery after an upgrade can be cleared by
  deleting that cache directory.

## Verify
- [ ] `kubectl version` shows client/server minors within 1.
- [ ] `go list -m` shows one consistent `v0.N` across client-go/api/apimachinery.
- [ ] Tests pass against the oldest and newest supported apiserver minors.

## Checked
Date: 2026-10-27. Documentation: Kubernetes Version Skew Policy page, client-go README and
compatibility matrix, controller-runtime README and VERSIONING.md, API deprecation guide, kubectl
`version` and cli-runtime source (latest release v1.37.1). Confirmed: kubectl plus or minus one
minor; skew warning and `--warnings-as-errors`; client-go matrix semantics; CR v0.19/v0.31
mapping; `policy/v1beta1` PodDisruptionBudget no longer served from v1.25; discovery cache
location and `KUBECACHEDIR`. Removed the unconfirmed exact warning text, pinned patch
versions, `ENVTEST_K8S_VERSION` and the `rm -rf` command, and the typed-client field-dropping and
`kubectl apply --server-side` remarks.
Method: documentation only; no commands were run.
