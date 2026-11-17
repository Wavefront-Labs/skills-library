---
id: computing-software.devops-ci-cd.secrets-management.sbom-quality-and-ntia-minimum-elements
name: sbom-quality-and-ntia-minimum-elements
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, ntia-minimum-elements, sbom-quality, sbom]
level: practitioner
status: verified
description: "Check SBOMs meet NTIA minimum elements and are actually useful: supplier, versions, unique identifiers (purl/CPE), dependency relationships, scoring with sbomqs."
sources: ["https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom", "https://github.com/interlynk-io/sbomqs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM quality and NTIA minimum elements

An SBOM that lists package names without versions or identifiers cannot be matched to
vulnerabilities and fails procurement checks (US EO 14028, EU CRA expectations).

## NTIA minimum elements
From the NTIA 2021 report (PDF, fetched): data fields per component: **supplier name, component name, version, other unique identifiers
(purl, CPE, SWID), dependency relationship, author of SBOM data, timestamp**.
Plus automation support (SPDX/CycloneDX machine-readable) and practices (generate per build, cover
transitive deps, state known unknowns).

## Score it
```bash
sbomqs score app.cdx.json                 # 0-10 overall, per profile and per category (run on sbomqs 2.1.3)
sbomqs score app.cdx.json --profile ntia-2021
sbomqs score app.cdx.json --category identification,provenance,integrity
sbomqs compliance --ntia-2021 app.cdx.json   # the 2021 field list above, scored per element
sbomqs compliance --ntia app.cdx.json        # in v2 this is the newer "NTIA Minimum Elements (2026)" profile
```
sbomqs v2 categories are identification, provenance, integrity, completeness, licensing, vulnerability, structural...; `--category ntia-minimum-elements` is rejected
(`invalid category ... for v2 mode`; it exists only with `--legacy` and the capitalised `NTIA-minimum-elements`).
Sample syft CycloneDX output scored 4.4/10 overall: no supplier, no author, no relationships.
Alternatives: `ntia-checker` from `pip install ntia-conformance-checker` (SPDX only; run: `Conformant: False`, versions and suppliers missing); `cyclonedx validate` for schema validity.

## Common gaps and fixes
| Gap | Fix |
|---|---|
| Missing purl | generate from lockfiles/package managers (syft, cdxgen), not from binary heuristics only |
| No supplier | set `--source-name`/metadata; for OSS supplier is often unknown, mark it explicitly |
| Flat list, no relationships | CycloneDX `dependencies`, SPDX `DEPENDS_ON`; cdxgen captures the tree |
| OS packages only for container images | combine image scan with app lockfile SBOM |
| No timestamp/author tool info | ensure tool metadata is populated |

## In CI
Fail the release if score drops below a threshold or NTIA compliance fails; store SBOMs with the release and attest them.

## Verify
- [ ] `sbomqs compliance --ntia-2021` (and `--ntia` if you target the newer profile) reports no zero-scored required element for each released artifact's SBOM.
