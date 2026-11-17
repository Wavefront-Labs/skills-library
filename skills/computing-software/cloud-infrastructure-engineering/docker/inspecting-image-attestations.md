---
id: computing-software.cloud-infrastructure-engineering.docker.inspecting-image-attestations
name: inspecting-image-attestations
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, attestations, imagetools-inspect-attestations, in-toto, provenance, sbom, slsa, crane]
level: advanced
description: "Read in-toto SBOM and provenance attestations attached by buildx using imagetools Go templates, crane and jq, including per-platform selection."
sources: ["https://docs.docker.com/build/metadata/attestations/attestation-storage/", "https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/", "https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting image attestations

## Quick reads with imagetools

```sh
IMG=registry.example.com/app:1.4.0
docker buildx imagetools inspect $IMG --format '{{ json .Provenance.SLSA }}'
docker buildx imagetools inspect $IMG --format '{{ json .SBOM.SPDX }}'
docker buildx imagetools inspect $IMG --format '{{ json (index .SBOM "linux/amd64").SPDX }}'   # multi-platform image
docker buildx imagetools inspect $IMG \
  --format '{{ range .SBOM.SPDX.packages }}{{ .name }}@{{ .versionInfo }}{{ println }}{{ end }}'
```

All SBOM data is under `.SBOM` and all provenance data under `.Provenance`. For a multi-platform image,
index the attribute by platform, as in the third command.

## What's underneath

BuildKit stores attestations as manifests in the image index, after the runnable manifests. Each attestation
manifest describes one platform manifest. Its descriptor in the index has platform `unknown/unknown` and
annotations:

```
vnd.docker.reference.type: attestation-manifest
vnd.docker.reference.digest: sha256:<manifest it describes>
```

With OCI artifact storage enabled the attestation manifest has `artifactType`
`application/vnd.docker.attestation.manifest.v1+json` and a `subject` pointing at the image manifest; with
`oci-artifact=false` the legacy layout is used. Each layer holds one attestation blob with media type
`application/vnd.in-toto+json` and the annotation `in-toto.io/predicate-type`, set to the statement's
`predicateType` (`https://spdx.dev/Document` for SBOMs, `https://slsa.dev/provenance/v0.2` for provenance by
default; SLSA provenance v1 can be selected with `--attest type=provenance,version=v1`).

An in-toto statement has `_type`, `subject[]` (name and digest), `predicateType` and `predicate`.
BuildKit limits each attestation file it reads from a build result to 80 MiB.

Because attestations are manifests in the registry, you can inspect them without pulling the image. To walk
the index by hand, filter its `manifests[]` on the `vnd.docker.reference.type` annotation, then read the
attestation manifest's layers and fetch the blob you need with `crane manifest` and `crane blob`.

## Uses

- Confirm which base image and sources an image was built from: provenance `materials` list entries such as
  `pkg:docker/golang@1.19.4-alpine?platform=linux%2Farm64` with digests (with `mode=max` provenance also
  records the Dockerfile source).
- Feed the SBOM to a scanner: `docker buildx imagetools inspect $IMG --format '{{ json .SBOM.SPDX }}' > sbom.spdx.json`.
- Policy checks with a tool that understands in-toto attestations.

## Gotchas

- The `local` and `tar` exporters cannot attach attestations to an image; they write JSON files to the root of
  the output instead.
- The classic image store cannot hold an image index, so the `docker` driver fails to build with attestations
  there; use a different driver or turn on the containerd image store.
- `docker pull` and `docker image inspect` do not show attestations; they are registry-side manifests.

## Verify

The provenance `materials` digest for a base image equals the digest of that base tag at build time, and the
statement's `subject` digest equals the digest of the platform manifest it describes.

## Checked

2026-10-26. Documentation release: docker/docs main (build attestations: SBOM, SLSA provenance and index pages) and moby/buildkit docs/attestations/attestation-storage.md at main, checked 2026-10-26. Confirmed: .SBOM and .Provenance attributes with Go template formats, platform indexing, SPDX package template, attestation manifests in the image index with platform unknown/unknown, vnd.docker.reference.type and vnd.docker.reference.digest annotations, in-toto media type and in-toto.io/predicate-type annotation, artifactType and oci-artifact=false, 80 MiB read limit, SLSA provenance v0.2 default with --attest version option, exporter limitation for local and tar, materials entries with uri and digest. Fixed: the old `.Provenance.SLSA.materials` jq pipeline and the claim that v1 predicates appear on newer BuildKit (v1 is opt-in). Removed unconfirmed claims: Docker Scout and Kyverno policy details, the cosign download attestation advice and the statement that buildx attestations are unsigned.

Method: documentation only; no commands were run.
