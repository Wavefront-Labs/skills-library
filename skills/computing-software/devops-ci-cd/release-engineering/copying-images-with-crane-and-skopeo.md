---
id: computing-software.devops-ci-cd.release-engineering.copying-images-with-crane-and-skopeo
name: copying-images-with-crane-and-skopeo
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, crane, skopeo, artifact-promotion]
level: practitioner
status: docs-checked
description: "Promote container images between registries or repos without rebuilding using crane or skopeo: copy by digest, multi-arch preservation, retagging and keeping signatures."
sources: ["https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Re-tagging and copying images with crane / skopeo

Promotion must move the **same bytes**. `docker pull/tag/push` works but needs a daemon. Use registry-to-registry tools.

## crane
```bash
crane digest registry.example.com/staging/api:1.4.2           # sha256:...
crane copy registry.example.com/staging/api@sha256:abc... registry.example.com/prod/api:1.4.2
crane tag registry.example.com/prod/api:1.4.2 stable           # add tag, same registry, no data copy
crane manifest registry.example.com/prod/api:1.4.2 | jq .mediaType   # index vs single manifest
```
`crane copy` retains the digest value of the source image (per the crane reference).

## skopeo
```bash
skopeo copy --all --preserve-digests \
  docker://registry.example.com/staging/api@sha256:abc... \
  docker://123456789012.dkr.ecr.eu-west-1.amazonaws.com/api:1.4.2
```
`--all` copies every platform; without it only the current platform is copied (digest changes!).

## Signatures and attestations
Signatures and attestations (for example Cosign's) are stored as separate OCI objects. Copy them too and keep the image digest unchanged, or they will not verify (see your signing tool's docs).

## Auth in CI
`crane auth` / `skopeo login`, or rely on the Docker config and credential helpers.

## Verify
- [ ] `crane digest` returns the same digest at source and destination.

## Checked

2026-10-28. Confirmed against the crane reference (copy retains the digest value, tag, digest, manifest, auth) and the skopeo-copy manual (`--all` copies every image of a list instead of the current platform only, `--preserve-digests`, `skopeo login`). Removed: the multi-arch claim about docker tooling, `skopeo inspect --raw`, `cosign copy` and the signature tag naming, `crane auth login` spelling, the ECR credential helper and `cosign verify`.

Method: documentation only; no commands were run.
