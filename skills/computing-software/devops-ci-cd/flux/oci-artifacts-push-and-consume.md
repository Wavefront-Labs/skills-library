---
id: computing-software.devops-ci-cd.flux.oci-artifacts-push-and-consume
name: oci-artifacts-push-and-consume
category: computing-software
field: devops-ci-cd
product: flux
tags: [oci, ocirepository, flux-push-artifact, flux-tag-artifact, registry]
level: sme
status: docs-checked
description: "Publish Kubernetes manifests as OCI artifacts with the Flux CLI and consume them with OCIRepository and Kustomization."
sources:
  - https://fluxcd.io/flux/cheatsheets/oci-artifacts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of Git, Flux can reconcile manifests stored in a container registry. This is useful when Git holds templates (cue, jsonnet) and CI generates the final YAML.

Author with the CLI commands `flux push artifact`, `flux pull artifact`, `flux tag artifact`, `flux diff artifact` and `flux list artifacts`. Content media type is `application/vnd.cncf.flux.content.v1.tar+gzip`.

```sh
flux push artifact oci://ghcr.io/org/manifests/podinfo:$(git rev-parse --short HEAD) \
  --path="./kustomize" \
  --source="$(git config --get remote.origin.url)" \
  --revision="$(git branch --show-current)@sha1:$(git rev-parse HEAD)"
flux tag artifact oci://ghcr.io/org/manifests/podinfo:$(git rev-parse --short HEAD) --tag latest
```

Consume with an OCIRepository used like a GitRepository:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: OCIRepository
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 10m
  url: oci://ghcr.io/org/manifests/podinfo
  ref:
    tag: latest
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 10m
  targetNamespace: default
  prune: true
  sourceRef:
    kind: OCIRepository
    name: podinfo
  path: ./
```

Typical flow: staging follows `latest`, production follows a semver (`ref.semver`). Alerts and Receivers work with OCIRepository just as with Git.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/cheatsheets/oci-artifacts/ (raw source in the fluxcd/website repository).

Removed or corrected: the OCIRepository url and default-tag claims, which are not on the page.

Method: documentation only; no commands were run.
