---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-quality-scoring
name: sbom-quality-scoring
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-quality-scoring, sbom-minimum-elements, sbom quality, sbomqs, completeness, ntia conformance, accuracy, ground truth, ntia checker, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Measure SBOM quality by field completeness, identifier validity, depth and accuracy against ground truth."
sources:
  - https://github.com/interlynk-io/sbomqs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM quality and completeness scoring

Goal: sbom that consumers can trust.

Method:
- Run a quality tool such as sbomqs (sbomqs score FILE gives a 0-10 quality score and can validate against BSI, NTIA and other standards) to score fields such as supplier, licence, checksum, purl and dependencies.
- Compare against ground truth: build a reference app with known dependencies and diff.
- Test across tools; different generators give different results.
- Track metrics over time: percent components with purl, percent with licence, percent with hashes.
- Fix upstream by pinning, lock files and enrichment.

Gotchas:
- A high score does not show completeness; transitive coverage still needs testing.
- Using NOASSERTION everywhere may pass schema but fail value.

Verify: threshold gate in CI for quality score.

## Checked

2026-11-02. Checked against the sbomqs README (sbomqs score, 0-10 score, compliance standards, per-feature listing of components without suppliers). Removed: the NTIA conformance checker and SBOM Scorecard names (not confirmed).

Method: documentation only; no commands were run.
