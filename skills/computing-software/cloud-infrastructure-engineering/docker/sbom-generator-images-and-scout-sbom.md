---
id: computing-software.cloud-infrastructure-engineering.docker.sbom-generator-images-and-scout-sbom
name: sbom-generator-images-and-scout-sbom
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, sbom, sbom-generator, scanner-image, scout-sbom, docker-scout, buildkit-syft-scanner, spdx]
level: advanced
description: "Plug a custom SBOM generator image into BuildKit via the scanner protocol, and export or compare SBOMs with docker scout sbom formats and filters."
sources: ["https://docs.docker.com/build/metadata/attestations/sbom/#sbom-generator", "https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md", "https://docs.docker.com/reference/cli/docker/scout/sbom/", "https://docs.docker.com/scout/how-tos/view-create-sboms/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom SBOM generator images and docker scout sbom

## BuildKit SBOM generator protocol
`--attest type=sbom,generator=<image>` runs that image after the build with:
- `BUILDKIT_SCAN_SOURCE` (required) - the root filesystem of the build stage, passed as a
  read-only mount,
- `BUILDKIT_SCAN_SOURCE_EXTRAS` (optional) - a directory containing extra filesystems to scan
  (if it does not exist, nothing extra is scanned),
- `BUILDKIT_SCAN_DESTINATION` (required) - the directory where the scanner writes its SBOM data,
  as `$BUILDKIT_SCAN_DESTINATION/<scan>.spdx.json`.

Default generator: the BuildKit Syft scanner (`docker/buildkit-syft-scanner`, built on Anchore's
Syft). Per the protocol document, only SBOMs in the **SPDX JSON** format are currently supported;
BuildKit attaches them to the final image as an in-toto attestation with the
`https://spdx.dev/Document` predicate type. A custom generator image must follow that protocol, so
other formats such as CycloneDX cannot be attached this way. The Docker Scout SBOM indexer
(`docker/scout-sbom-indexer`) is also available as a generator.
```sh
docker buildx build --attest type=sbom,generator=<generator-image> \
  -t registry.example.com/app:1.4.0 --push .
```

## docker scout sbom
```sh
docker scout sbom registry.example.com/app:1.4.0                       # default format: Scout JSON
docker scout sbom --format spdx -o app.spdx.json registry.example.com/app:1.4.0
docker scout sbom --format cyclonedx -o app.cdx.json image://app:dev   # local image
docker scout sbom --format list --only-package-type golang,npm app:dev
docker scout compare --to app:1.3.0 app:1.4.0                          # package/CVE diff
```
`--format` is one of `list`, `json` (default, not SPDX-JSON), `spdx`, `cyclonedx`;
`--only-package-type` works only with `--format list`. Image prefixes: `image://` (default),
`local://`, `registry://`, `oci-dir://`, `archive://`, `fs://`. Scout uses an attached SBOM
attestation if present, otherwise it creates one by indexing the image contents. Building with
the BuildKit default generator differs from the Scout indexer; the docs say the Scout SBOM indexer
gives richer results and better compatibility with Scout analysis:
`--attest type=sbom,generator=docker/scout-sbom-indexer:latest`.

## Gotchas
- To build images with SBOM attestations use the containerd image store, or a `docker-container`
  builder with `--push`; the classic image store does not support manifest lists or image indices,
  which attestations require.
- SBOM coverage depends on the package metadata the generator can read.

## Verify
`docker buildx imagetools inspect app:1.4.0 --format '{{json .SBOM}}'` shows the attached SBOM;
`docker scout sbom --format list app:1.4.0` lists the packages.

## Checked

Date: 2026-10-24. Documentation release: BuildKit SBOM protocol document, Docker build SBOM attestation page, `docker scout sbom` reference and Scout SBOM how-to (moby/buildkit, docker/docs main).
Confirmed: the three `BUILDKIT_SCAN_*` variables and their semantics, the destination file naming
`<scan>.spdx.json`, SPDX-JSON being the only supported generator output with the `https://spdx.dev/Document`
predicate type, the default Syft-based scanner, `docker scout sbom` formats and defaults, `--only-package-type`
restriction, image reference prefixes, the Scout SBOM indexer generator, and the image store requirement for attestations.
Corrected: generators write SPDX JSON files (not in-toto statements) and CycloneDX cannot be attached through this
protocol. Removed: the scanner version pin, third-party scanner names, the no-network claim, the air-gap advice and the
`dpkg` comparison, none of which the pages state.

Method: documentation only; no commands were run.
