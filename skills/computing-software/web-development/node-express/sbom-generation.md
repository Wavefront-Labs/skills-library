---
id: computing-software.web-development.node-express.sbom-generation
name: sbom-generation
category: computing-software
field: web-development
product: node-express
tags: [sbom, cyclonedx, spdx, syft, npm-sbom, supply-chain]
level: practitioner
status: docs-checked
description: "Generating and using SBOMs: npm sbom, CycloneDX and syft for source and container images, attaching and attesting them to releases, and scanning SBOMs for vulnerabilities."
sources:
  - https://docs.npmjs.com/cli/v11/commands/npm-sbom
  - https://github.com/anchore/syft
  - https://github.com/anchore/grype
  - https://github.com/sigstore/cosign/blob/main/doc/cosign_attest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM generation

A Software Bill of Materials lists every component (name, version, purl, licence, hashes) in what you ship. Customers, regulators and your own incident response ("are we affected by CVE-X?") need it.

## 1. Generate
```bash
npm sbom --sbom-format cyclonedx --omit dev > sbom.cdx.json          # from the lockfile
npx @cyclonedx/cyclonedx-npm --omit dev --output-file sbom.cdx.json
syft . -o cyclonedx-json=sbom.cdx.json                                # any ecosystem in the repo
syft ghcr.io/acme/web:1.4.2 -o spdx-json=sbom.spdx.json               # what is really in the image (OS packages too)
```
- Formats: **CycloneDX** and **SPDX**. Pick what consumers ask for; tools convert.
- Container SBOMs include OS packages and binaries that a source SBOM misses; ship both or the image one.
- Exclude dev dependencies for distribution SBOMs; keep a full one internally.

## 2. Publish and attest
```bash
cosign attest --yes --predicate sbom.cdx.json --type cyclonedx ghcr.io/acme/web@sha256:...
```
Attach to GitHub releases, or use `docker buildx build --sbom=true --provenance=true` (BuildKit attestations). GitHub's dependency graph can export SPDX for a repo.

## 3. Use it
```bash
grype sbom:sbom.cdx.json
```
Ingest into Dependency-Track for continuous monitoring across all services; when a new CVE lands, query which releases include the component. Publish VEX statements for vulnerabilities that are present but not exploitable.

## Gotchas
- An SBOM generated before `npm ci` or from `package.json` alone has ranges, not versions; generate from the lockfile or built artifact.
- Bundled/vendored code and CDN scripts are invisible to lockfile-based tools; list them manually.

## Verify
- [ ] CI produces an SBOM per release artifact, scanned with a failing threshold, and stored with the release.

## Checked

2026-10-25 against the npm CLI source (npm/cli main), Syft and Grype READMEs, the cosign attest reference and Docker docs. Confirmed: npm sbom has a sbom-format config accepting cyclonedx or spdx; syft takes an image or directory and -o cyclonedx-json / spdx-json with =file output; grype scans an SBOM with grype sbom:<file>; cosign attest takes --predicate, --type (including cyclonedx) and -y/--yes; docker buildx --sbom=true and --provenance=mode=max generate attestations.

Method: documentation only; no commands were run.
