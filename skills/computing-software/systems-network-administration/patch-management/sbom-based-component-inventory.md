---
id: computing-software.systems-network-administration.patch-management.sbom-based-component-inventory
name: sbom-based-component-inventory
category: computing-software
field: systems-network-administration
product: patch-management
tags: [sbom-inventory, sbom, syft, grype, cyclonedx, spdx, dependency-track, software-inventory]
level: advanced
status: docs-checked
description: "Build a component-level software inventory from SBOMs: generate with Syft (CycloneDX/SPDX), track in Dependency-Track, and find affected systems when a library CVE drops."
sources:
  - https://github.com/anchore/syft
  - https://github.com/anchore/grype
  - https://docs.dependencytrack.org/
  - https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM-based component inventory

**Goal:** answer "where do we run library X version Y?" in minutes, including inside containers and vendor apps that package managers do not see.

## Generate SBOMs
```bash
syft /opt/app -o cyclonedx-json=app.cdx.json
syft registry.example/app:1.4.2 -o spdx-json=app-1.4.2.spdx.json
```
Generate in CI for everything you build (attach to the image as an attestation), and request SBOMs from vendors (CycloneDX or SPDX; the NTIA minimum elements report defines the required data fields).

## Scan SBOMs for vulnerabilities
```bash
grype sbom:app.cdx.json --fail-on high
```
Rescanning stored SBOMs catches new CVEs without touching the systems.

## Central tracking
Upload to OWASP Dependency-Track: `POST /api/v1/bom` (multipart form with `projectName`, `projectVersion` and `autoCreate=true`, or a project UUID) or `PUT /api/v1/bom` with a Base64-encoded JSON payload. Check its documentation for the vulnerability sources it analyses against and for searching components across projects.

## Use it during an emergency
1. Search the component (purl, e.g. `pkg:maven/org.apache.logging.log4j/log4j-core`).
2. List affected projects and versions; map projects to hosts/images via your deployment records.
3. Use VEX statements to mark "not affected" where code paths are unreachable, so they drop off reports.

## Gotchas
- SBOMs go stale at the next deploy; tie them to the exact build digest.
- Static binaries and vendored code are often missed; check SBOM completeness against known dependencies.

## Verify
Pick a known library in production and confirm the inventory returns every location within one query.

## Checked
Date: 2026-10-27. Documentation checked: Syft README (image and directory scanning, `-o cyclonedx-json`, `-o spdx-json=<file>`), Grype README and source (`sbom:` input, `--fail-on`), Dependency-Track CI/CD page (`PUT` with Base64 JSON, `POST` multipart, `autoCreate`, `projectName`, `projectVersion`). Removed the `dir:` scheme, the host-scan exclusions, the NTIA element list and the Dependency-Track vulnerability-source claim, which were not confirmed.

Method: documentation only; no commands were run.
