---
id: computing-software.devops-ci-cd.flux.image-digest-pinning
name: image-digest-pinning
category: computing-software
field: devops-ci-cd
product: flux
tags: [digestreflectionpolicy, latest-tag, imagepolicy, digest, pinning]
level: advanced
status: docs-checked
description: "Follow a mutable tag such as latest safely by pinning its digest in Git with ImagePolicy digestReflectionPolicy."
sources:
  - https://fluxcd.io/flux/guides/image-update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Using `latest` directly means pod restarts can silently pull new software. The GitOps approach pins the digest after the tag in Git, so the deployed version is controlled and the update is traceable in history:

```yaml
image: ghcr.io/stefanprodan/podinfo:latest@sha256:ec0119616bb8be9199575c05bfc23a6bf0fbdb0690ee15834e7b43bc3f4f6017
```

Flux can poll the digest of a fixed tag. Filter to just that tag and reflect the digest:

```yaml
apiVersion: image.toolkit.fluxcd.io/v1
kind: ImagePolicy
metadata:
  name: podinfo
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: podinfo
  filterTags:
    pattern: '^latest$'
  policy:
    alphabetical: {}
  digestReflectionPolicy: Always
  interval: 10m
```

`digestReflectionPolicy` values:
- `Never` (default): the digest is not reflected in the ImagePolicy status.
- `Always`: Flux fetches the digest for the filtered tag every `interval`; use it to follow `latest`.
- `IfNotPresent`: the digest is updated only when a new tag is elected as latest (tag and digest change together), preventing a re-pushed tag from changing; an `interval` is not allowed with it.

The manifest carries the setter marker `# {"$imagepolicy": "flux-system:podinfo"}` on the image line. For Helm values with separate fields, use `:name`, `:tag` and `:digest` setters, e.g. `{"$imagepolicy": "flux-system:podinfo:digest"}`.

## Checked

2026-11-08. partial read of https://fluxcd.io/flux/guides/image-update/: only the Digest pinning section and the digest setter notes; the rest of the guide was not read.

Removed or corrected: the .status.latestRef.digest field name and the closing claim about commits authored by Flux, neither of which is on the page.

Method: documentation only; no commands were run.
