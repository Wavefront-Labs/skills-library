---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-generation-from-source-and-build
name: sbom-generation-from-source-and-build
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-generation-from-source-and-build, sbom-generation, syft, cdxgen, cyclonedx maven plugin, cyclonedx-npm, lock file, build time sbom, spdx-sbom-generator, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Generate SBOMs at build time from lock files and package managers using CycloneDX plugins, cdxgen or Syft."
sources:
  - https://github.com/CycloneDX/cdxgen
  - https://github.com/CycloneDX/cyclonedx-rust-cargo
  - https://github.com/anchore/syft
  - https://github.com/aquasecurity/trivy/blob/main/docs/guide/supply-chain/sbom.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating SBOMs from source and build

Goal: accurate, repeatable SBOMs in CI.

Method:
- Prefer build-integrated generators that read the resolved dependency tree: cargo-cyclonedx (cargo cyclonedx) for Rust, or cdxgen, which detects maven, gradle or sbt for Java projects and supports other ecosystems.
- Syft: syft <source> -o cyclonedx-json=sbom.cdx.json -o spdx-json=sbom.spdx.json (several outputs in one run; sources include images, filesystems and archives). Trivy: trivy fs --format cyclonedx --output result.json <path>.
- Use lock files (package-lock.json, poetry.lock, Cargo.lock, go.sum) so versions are exact.
- Run on every release build; archive the SBOM with build artefacts and tag with commit and build ID.
- Generate both source (pre-build) and built (post-build) views if needed; record generation context.

Gotchas:
- Unpinned ranges produce non-reproducible lists.
- Vendored copies and statically linked C libraries are missed by package-manager scanning; add binary or file scanning.

Verify: regenerate twice and diff should be identical apart from timestamp and serial.

## Checked

2026-11-02. Checked against the cdxgen README (maven / gradle / sbt detection), the cargo-cyclonedx README (cargo cyclonedx), the Syft README (-o format=file, scan targets) and the Trivy SBOM guide (trivy fs --format cyclonedx --output). Removed: the list of per-language CycloneDX plugins and the 'syft dir:.' form, which these pages do not show.

Method: documentation only; no commands were run.
