---
id: computing-software.devops-ci-cd.secrets-management.sbom-diff-and-merge
name: sbom-diff-and-merge
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, sbom, sbom-diff, sbom-merge, cyclonedx-cli, cyclonedx, spdx, sbomasm, dependency-drift, release-diff, multi-component-sbom, jq]
level: advanced
status: verified
description: "Compare SBOMs between releases to see added, removed and upgraded components, and merge per-service or per-layer SBOMs into one product SBOM with cyclonedx-cli or sbomasm."
sources: ["https://github.com/CycloneDX/cyclonedx-cli", "https://github.com/interlynk-io/sbomasm", "https://cyclonedx.org/specification/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM diff and merge

## Diff: what changed between two releases
```bash
cyclonedx diff old.cdx.json new.cdx.json --component-versions
# lists components added, removed, and with changed versions (run on cyclonedx-cli 0.33.1: a 4.17.20 -> 4.17.21 bump showed as -/+ pair)
cyclonedx diff old.cdx.json new.cdx.json --component-versions --output-format json > diff.json
```
SPDX inputs: convert first (`cyclonedx convert --input-file x.spdx.json --output-format json`
or regenerate with `syft convert x.syft.json -o cyclonedx-json`; both ran, `cyclonedx convert` accepts `--input-format spdxjson`). Keep `syft-json` from
the build to convert losslessly later.

Quick jq diff by purl (format-agnostic once you extract purls):
```bash
purls() { jq -r '.components[]?.purl // empty' "$1" | sort -u; }   # CycloneDX
# the root application component is in .components too, so a version bump of the app itself shows up as add + remove
comm -13 <(purls old.cdx.json) <(purls new.cdx.json)   # added
comm -23 <(purls old.cdx.json) <(purls new.cdx.json)   # removed
```
Uses in CI:
- PR comment: "this change adds 14 transitive packages" for the reviewer.
- Release notes: dependency changes section generated from the diff.
- Gate: fail when a new component has a disallowed licence or comes from an unapproved
  registry (purl namespace).

## Merge: one SBOM for a product
Products ship several images/binaries; customers want a single SBOM.
```bash
# cyclonedx-cli: flat merge or hierarchical (each input becomes a sub-component)
cyclonedx merge --input-files api.cdx.json web.cdx.json worker.cdx.json \
  --hierarchical --name acme-platform --version 2026.10 --output-file platform.cdx.json

# sbomasm (CycloneDX and SPDX)
sbomasm assemble -n acme-platform -v 2026.10 -t application \
  -o platform.spdx.json api.spdx.json web.spdx.json worker.spdx.json
```
- **Hierarchical** keeps which component came from which service (needed for
  "where is log4j?" answers; run: two sub-components holding 3 and 6 components); **flat** loses provenance and, in cyclonedx-cli 0.33.1, did NOT
  de-duplicate (two 3- and 6-component inputs gave 11 components, `pkg:npm/minimist@1.2.5` twice).
- sbomasm: hierarchical is the default, `-f` flat, `-a` assembly, `--augmentMerge --primary` enrich (checked in `sbomasm assemble --help` v2.1.1; run on two SPDX files).
- Don't merge SPDX and CycloneDX inputs: normalise to one format first.
- Set the top-level metadata (supplier, product name, version, timestamp) explicitly;
  merged documents otherwise inherit odd defaults.

## Validate the result
```bash
cyclonedx validate --input-file platform.cdx.json     # the version is auto-detected
# --input-version must match the document: syft 1.54 writes CycloneDX 1.7 and `--input-version v1_6` fails with "expected 1.6 actual 1.7"
# SPDX: pyspdxtools -i platform.spdx.json   (pip install spdx-tools; silent exit 0 on a valid merged file)
```
Then sign/attest the merged SBOM like any release artifact.

## Gotchas
- Different generators name the same package differently; compare by `purl`, not
  `name`.
- Diffs are noisy if SBOMs embed timestamps/serial numbers; exclude metadata.
- Merging duplicates of the same component with different `bom-ref`s creates
  duplicate entries (observed: syft's `bom-ref` embeds a per-run `package-id`); dedupe by purl yourself when flat-merging.

## Verify
Diff an SBOM against itself: no changes. Bump one dependency and rebuild: diff shows
exactly that version change. The merged SBOM validates and its component count equals the
de-duplicated union of the inputs.
