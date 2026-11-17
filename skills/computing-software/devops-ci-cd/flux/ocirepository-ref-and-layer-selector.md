---
id: computing-software.devops-ci-cd.flux.ocirepository-ref-and-layer-selector
name: ocirepository-ref-and-layer-selector
category: computing-software
field: devops-ci-cd
product: flux
tags: [ocirepository, semver, layerselector, helm-oci, mediatype]
level: sme
status: docs-checked
description: "Select OCI tags with tag, semver, semverFilter or digest, and extract the right layer with layerSelector extract or copy."
sources:
  - https://fluxcd.io/flux/components/source/ocirepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.url` is `oci://<host>:<port>/<org>/<repo>` with no tag or digest. `.spec.ref` has `tag`, `semver`, `digest`; later fields win, and with nothing set the `latest` tag is used.

```yaml
spec:
  url: oci://ghcr.io/org/manifests/podinfo
  ref:
    semver: ">=6.9.0"
    semverFilter: ".*-rc.*"
```

`ref.semverFilter` is a regular expression applied to fetched tags first; only matching tags are considered for the semver range, useful for separating release-candidate or per-environment tags.

`.spec.layerSelector` chooses which layer is extracted. Unset, the first layer is used. Otherwise:

```yaml
spec:
  layerSelector:
    mediaType: "application/vnd.cncf.helm.chart.content.v1.tar+gzip"
    operation: copy
```

- `operation: extract` (default) unpacks the layer.
- `operation: copy` stores the tarball as-is. Helm charts consumed by a HelmRelease use `copy`.
- The first layer matching the media type is used, and it must be compressed `tar+gzip`.

`.spec.insecure: true` allows plain HTTP registries (default `false`). Other fields: `interval`, `timeout`, `suspend`, `ignore`, `secretRef`, `serviceAccountName`, mutual TLS `certSecretRef` and a proxy secret.

Check which revision was pulled with `flux get sources oci`; the artifact revision is the tag plus digest.

## Checked

2026-11-03. Read the OCIRepository reference (fluxcd.io/flux/components/source/ocirepositories/): `.spec.url` format, `ref` fields and `latest` default, `semverFilter`, `layerSelector` operations and first-match rule, `insecure`, `certSecretRef`, `proxySecretRef`, `serviceAccountName`; `flux get sources oci` checked on its CLI page. Nothing removed.

Method: documentation only; no commands were run.
