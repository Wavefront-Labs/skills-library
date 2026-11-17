---
id: computing-software.cloud-infrastructure-engineering.docker.helm-charts-in-oci-registries
name: helm-charts-in-oci-registries
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oci-artifacts, helm-oci, helm-push, helm, registry]
level: practitioner
description: "Package and push Helm charts to OCI registries with helm push oci://, install or pull by version or digest, and sign them, replacing chart repo index.yaml."
sources: ["https://helm.sh/docs/topics/registries/", "https://helm.sh/docs/helm/helm_push/", "https://helm.sh/docs/topics/provenance/", "https://github.com/helm/helm/blob/main/pkg/registry/client.go", "https://github.com/fluxcd/source-controller/blob/main/docs/spec/v1/helmrepositories.md", "https://argo-cd.readthedocs.io/en/stable/user-guide/helm/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Helm charts in OCI registries

## Push
```sh
helm registry login registry.example.com -u ci --password-stdin <<<"$TOKEN"
helm package ./charts/api --version 1.4.0 --app-version 1.4.0
helm push api-1.4.0.tgz oci://registry.example.com/charts
# -> Pushed: registry.example.com/charts/api:1.4.0  Digest: sha256:...
```
The login host is the bare registry hostname (optionally with port): no scheme, no path.
- The chart **name** becomes the repository, the **version** the tag. You push to the
  namespace (`oci://.../charts`), not to `.../charts/api`.
- SemVer `+` build metadata is stored as `_` in the tag (`1.4.0+1` -> `1.4.0_1`); Helm converts it back when listing tags.
- The chart name comes from `Chart.yaml`, not the `.tgz` filename.
- Media types: config `application/vnd.cncf.helm.config.v1+json`, layer
  `application/vnd.cncf.helm.chart.content.v1.tar+gzip`.

## Consume
```sh
helm install api oci://registry.example.com/charts/api --version 1.4.0
helm pull oci://registry.example.com/charts/api --version 1.4.0
helm show values oci://registry.example.com/charts/api --version 1.4.0
helm install api oci://registry.example.com/charts/api@sha256:<digest>     # by digest (immutable)
```
Dependencies in Chart.yaml (the `repository` is the registry reference without the chart name):
```yaml
dependencies:
  - name: redis
    version: 20.x.x
    repository: oci://registry-1.docker.io/bitnamicharts
```
No `helm repo add` for OCI - `helm repo` commands do not apply.

## Argo CD / Flux
Argo CD: the `repoURL` has **no** `oci://` prefix (`registry.example.com/charts`), and a Helm
repository secret for an OCI registry sets `enableOCI: "true"`. Flux: prefer an `OCIRepository`
with `url: oci://registry.example.com/charts/api`; `HelmRepository` with `type: oci` still works
but is in maintenance mode in source-controller.

## Signing
Classic provenance (`helm package --sign`) writes a `.prov` file; if it sits next to the `.tgz`,
`helm push` uploads it as an extra layer of the chart manifest (media type
`application/vnd.cncf.helm.chart.provenance.v1.prov`). For transparency-log signing, Helm's docs
point to the `helm-sigstore` plugin (`helm sigstore upload`). Whether your cluster enforces any of
this is a separate admission-time decision; Helm's own commands do not do it for you.

## Gotchas
- Some registries need the repository and/or namespace created before the first `helm push`;
  otherwise the push errors. Create it first if your registry requires that.
- `helm push` takes only the `.tgz` made by `helm package`.
- The registry credentials file path is set with `$HELM_REGISTRY_CONFIG`.

## Verify
`helm show chart oci://registry.example.com/charts/api --version 1.4.0` prints the chart;
the registry manifest has config media type `application/vnd.cncf.helm.config.v1+json`.

## Checked

2026-10-25, against the Helm docs (helm-www, Helm 4 documentation: registries, helm push, provenance), Helm source `pkg/registry/client.go`, Argo CD user guide and declarative-setup docs, and Flux source-controller HelmRepository spec. Confirmed: login host format, push reference without chart name, `+` to `_` tag mapping, config and layer media types, digest install, dependency `repository` form, Argo CD URL without `oci://` plus `enableOCI`, Flux `type: oci` maintenance mode, `.prov` upload on push, `HELM_REGISTRY_CONFIG`. Removed: the claim that `.prov` files do not travel with OCI pushes (wrong), the Helm 3.13 digest gate, tag-range and ECR specifics, and the crane/jq verification.

Method: documentation only; no commands were run.
