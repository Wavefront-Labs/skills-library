---
id: computing-software.cloud-infrastructure-engineering.kubernetes.offline-helm-charts-and-oci-vendoring
name: offline-helm-charts-and-oci-vendoring
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, offline-helm, chart-vendoring, air-gapped, oci-registry, skopeo, hauler, image-relocation]
level: practitioner
status: docs-checked
description: "Move Helm charts and every image they reference into an air gap: helm pull/push to OCI, extracting image lists, skopeo/hauler sync, registry overrides."
sources: ["https://helm.sh/docs/topics/registries/", "https://github.com/containers/skopeo/blob/main/docs/skopeo-sync.1.md", "https://github.com/hauler-dev/hauler/blob/main/cmd/hauler/cli/store.go", "https://github.com/containerd/containerd/blob/main/docs/hosts.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://helm.sh/docs/helm/helm_dependency_build/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline Helm charts and OCI artifact vendoring

## 1. Pin and fetch charts (connected side)
```bash
helm pull oci://registry.example.com/charts/<chart> --version <x.y.z>
helm repo add <repo> <https-repo-url>
helm pull <repo>/<chart> --version <x.y.z>      # -> <chart>-<x.y.z>.tgz
helm dependency build ./my-umbrella                          # vendors subcharts into charts/
```
Commit `Chart.lock`; never rely on `latest` or repo index lookups offline.

## 2. Enumerate images the chart will actually use
Render with **your** values (images depend on values):
```bash
helm template x <chart>-<x.y.z>.tgz -f prod-values.yaml > rendered.yaml
# list every image: reference (containers, initContainers, hook Jobs) in rendered.yaml
```
Also check hook Jobs (for example admission webhook patch jobs) and operators that start
images at runtime: templates will not show those, so read the operator docs. Images referenced
by digest (`@sha256:`) must be copied with the digest preserved (`skopeo copy --preserve-digests`).

## 3. Copy into the disconnected registry
```bash
# connected: images + charts to a directory/tarball
skopeo sync --src yaml --dest dir sync.yaml ./bundle      # sync.yaml lists images per registry
# disconnected:
skopeo sync --src dir --dest docker ./bundle harbor.internal/mirror
helm push <chart>-<x.y.z>.tgz oci://harbor.internal/charts
```
`skopeo copy --all` copies a manifest list and all the images in it (without it, only the
image matching the current OS and architecture). Alternative all-in-one: **Hauler**, whose
`store` subcommands include `add chart`, `add image`, `save`, `load` and `serve registry`.
If admission verifies signatures or attestations, check that those artifacts also exist in
the mirror.

## 4. Point charts at the mirror
Use the chart's own image registry/repository values where it has them. For charts without
them, containerd registry configuration (`config_path` pointing to a directory of
`<host>/hosts.toml` files, for example `certs.d`) can redirect pulls to a mirror so manifests
keep upstream names.
```bash
helm install <release> oci://harbor.internal/charts/<chart> --version <x.y.z> -f prod-values.yaml
```

## Gotchas
- `helm dependency build` rebuilds `charts/` from `Chart.lock`; `helm dependency update` resolves
  versions again and needs the repositories reachable.

## Verify
- [ ] Install succeeds with egress blocked; `kubectl get pods -A -o jsonpath='{..image}'` shows only mirror hosts.

## Checked

2026-10-25, against skopeo `skopeo-sync` and `skopeo-copy` man pages, Hauler `cmd/hauler/cli/store.go` (main), containerd `docs/hosts.md`, and Helm `dependency build` and registries docs. Confirmed: `skopeo sync` yaml/dir/docker transports, `skopeo copy --all` and `--preserve-digests`, Hauler store subcommands (`add chart`, `add image`, `save`, `load`, `serve registry`), containerd `config_path` with per-host `hosts.toml`, `helm dependency build` from `Chart.lock`. Removed: the yq image-extraction pipeline, the Hauler `--add-images` flag, the `global.imageRegistry` convention, the claim about skopeo and referrers, and specific chart names and versions.

Method: documentation only; no commands were run.
