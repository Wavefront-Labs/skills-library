---
id: computing-software.devops-ci-cd.secrets-management.buildkit-sbom-and-provenance-attestations
name: buildkit-sbom-and-provenance-attestations
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, buildkit-sbom, sbom-attestation, provenance-attestations]
level: practitioner
status: docs-checked
description: "Generate SBOM and SLSA provenance attestations at image build time with BuildKit (docker buildx --sbom --provenance), inspect them and widen scan scope."
sources: ["https://docs.docker.com/build/metadata/attestations/sbom/", "https://docs.docker.com/build/metadata/attestations/slsa-provenance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuildKit SBOM attestations

```bash
docker buildx build --sbom=true --provenance=mode=max \
  -t registry.example.com/team/app:1.4.2 --push .
```
`--sbom=true` is shorthand for `--attest type=sbom` and `--provenance` for `--attest type=provenance`.
BuildKit generates the SBOM with a scanner plugin (by default the BuildKit Syft scanner, built on
Anchore's Syft); it follows the SPDX standard and attaches to the image as a JSON-encoded SPDX
document. Provenance follows the SLSA provenance schema, version 0.2 by default; add `version=v1`
(for example `--provenance=mode=max,version=v1`) for SLSA Provenance v1.

Provenance `mode=min` is the default and is safe for all builds. `mode=max` adds the LLB definition,
the full Dockerfile and source maps, but it exposes the values of build arguments. If build args are
carrying credentials or tokens, move them to secret mounts, which are never included in provenance.

## Inspect
```bash
docker buildx imagetools inspect registry.example.com/team/app:1.4.2 --format '{{ json .SBOM.SPDX }}'
docker buildx imagetools inspect registry.example.com/team/app:1.4.2 --format '{{ json .Provenance.SLSA }}'
```
For a multi-platform image, select a platform with `(index .SBOM "linux/amd64").SPDX`.

## Validate before pushing
Build with the local exporter and read the files in the output directory (the SBOM is
`sbom.spdx.json`):
```bash
docker buildx build --sbom=true --output type=local,dest=out .
```

## Scan stages and build context
By default BuildKit scans the final stage only, so build-time dependencies from earlier stages (for
example a `FROM scratch` final image) are missed. To widen the scope, declare these with an explicit
`ARG` in the Dockerfile; they cannot be set by variable substitution or environment variables:
```dockerfile
ARG BUILDKIT_SBOM_SCAN_STAGE=true     # in the stage(s) to scan; also accepts stage names such as base,bin
ARG BUILDKIT_SBOM_SCAN_CONTEXT=true   # scan the build context too
```
`--build-arg` can then override the value, but passing it without the `ARG` declaration has no effect.
Only stages that are actually built are scanned.

## Other generators
Select a different scanner with `--attest type=sbom,generator=<image>`; the image must implement the
BuildKit SBOM scanner protocol.

## Verify
- [ ] `imagetools inspect` shows the SBOM and provenance for the pushed image.

## Checked

Confirmed against both Docker pages (raw markdown of docker/docs): create flags and shorthands, SPDX and Syft scanner, provenance default mode and version, what `max` adds and the build-arg warning, `imagetools inspect` templates, local exporter validation, `BUILDKIT_SBOM_SCAN_STAGE` and `BUILDKIT_SBOM_SCAN_CONTEXT` behaviour, `generator` option. Removed: the GitHub Actions input names, the scanner image name, claims about the image index, `unknown/unknown` platform entries, attestations being unsigned and `--load` dropping them (none stated on these pages).

Method: docs-checked 2026-11-09 against the raw markdown of the Docker SBOM attestations and provenance attestations pages (docker/docs main), read in full.
