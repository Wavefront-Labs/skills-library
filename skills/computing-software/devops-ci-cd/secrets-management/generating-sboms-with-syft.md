---
id: computing-software.devops-ci-cd.secrets-management.generating-sboms-with-syft
name: generating-sboms-with-syft
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, sbom, syft, syft-generate, sbom-formats, spdx, cyclonedx, spdx-json, cyclonedx-json, anchore-sbom-action, container-sbom, sbom-attestation, grype, docker-buildx-sbom]
level: practitioner
status: gated
description: "Generate SBOMs with syft for images, directories and archives: choosing SPDX vs CycloneDX, scope and catalogers, CI actions, attaching as attestations, and checking completeness."
sources: ["https://github.com/anchore/syft", "https://github.com/anchore/sbom-action", "https://spdx.dev/use/specifications/", "https://cyclonedx.org/specification/overview/", "https://docs.docker.com/build/metadata/attestations/sbom/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating SBOMs with syft

## Commands
```bash
syft scan registry.example.com/api@sha256:... -o spdx-json=sbom.spdx.json -o cyclonedx-json=sbom.cdx.json
syft scan dir:. -o cyclonedx-json=src.cdx.json         # source tree (manifests/lockfiles)
syft scan docker-archive:image.tar -o syft-json
syft scan oci-dir:./layout
syft convert sbom.syft.json -o cyclonedx-json=sbom.cdx.json   # experimental; also reads SPDX
syft scan registry:ghcr.io/acme/api:1.4.0 --scope all-layers   # include files deleted in later layers
```
Run on syft 1.54.1: the `registry:`, `oci-dir:`, `docker-archive:` and `dir:` sources all scanned a local registry image/tarball/layout, and a
npm `package-lock.json` gave 3 components for a 2-dependency app (the app itself is listed too).
Formats: `spdx-json` (syft writes SPDX 2.3; CycloneDX output is 1.7 in this release, so a validator pinned to 1.6 rejects it; SPDX is an ISO standard, licence-centric, US EO 14028 / NTIA
accepted), `cyclonedx-json` (OWASP; security-centric, VEX support, good tooling for
vuln management), `syft-json` (lossless, convertible later with `syft convert`). Produce
the one your consumers ask for; when unsure, CycloneDX for internal security tooling,
SPDX for customers/regulators.

## What syft finds
Catalogers read package DBs (dpkg/apk/rpm), language manifests and lockfiles (npm,
pip/poetry, go modules incl. binaries' embedded build info, Maven JARs, Cargo.lock,
gems...). Image scans are the most accurate for "what ships"; source scans list what
*would* be installed and miss OS packages.
- Go binaries built with `-trimpath -ldflags "-s -w"` still report their modules (run: `golang.org/x/text@v0.14.0` and `stdlib` found); stripped C/C++ binaries
  don't show up: anything vendored/compiled-in without metadata is invisible.
- `--select-catalogers` / `--override-default-catalogers` to narrow or add (e.g.
  `+sbom-cataloger` to include SBOMs embedded in the image; `syft cataloger list` shows names and tags).

## In CI
```yaml
- uses: anchore/sbom-action@v0
  with:
    image: ghcr.io/acme/api@${{ steps.build.outputs.digest }}
    format: spdx-json
    output-file: sbom.spdx.json         # also uploads as workflow artifact / release asset
```
BuildKit alternative: `docker buildx build --sbom=true --push ...` attaches an SPDX
attestation to the image index (gated: unconfirmed, no Docker here; see docs.docker.com attestations page).

## Attach to the artifact
```bash
cosign attest --yes --predicate sbom.spdx.json --type spdxjson registry.example.com/api@sha256:...
# or GitHub: actions/attest with subject-digest + sbom-path (actions/attest-sbom is deprecated in its favour; gated: unconfirmed, not run in Actions)
cosign verify-attestation --type spdxjson --certificate-identity ... --certificate-oidc-issuer ... <image@digest>
```
Run with a key pair against a local registry: `cosign attest --type spdxjson` then `cosign verify-attestation --key cosign.pub --type spdxjson` verified.
Signed attestations bind the SBOM to the exact digest; loose files in a bucket don't.

## Use it
- Scan the SBOM instead of re-scanning the image: `grype sbom:sbom.cdx.json` (run on grype 0.120.1: lodash 4.17.20 and minimist 1.2.5 reported).
- Store per release; answer "are we affected by CVE-X?" by querying SBOMs (Dependency-Track,
  GUAC).

## Verify
`jq '.packages | length' sbom.spdx.json` (SPDX) or `jq '.components | length'` (CycloneDX)
is plausible (hundreds for a typical image), and spot-check that a known dependency with
its exact version is present.
