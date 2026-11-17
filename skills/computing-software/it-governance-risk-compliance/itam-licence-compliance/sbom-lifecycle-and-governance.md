---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-lifecycle-and-governance
name: sbom-lifecycle-and-governance
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-lifecycle-and-governance, sbom-distribution-and-integrity, sbom programme, retention, regeneration triggers, coverage metric, sbom governance, cisa maturity, itam-licence-compliance]
level: practitioner
status: draft
description: "Establish an SBOM programme with owners, triggers for regeneration, retention and metrics for coverage."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SBOM programme governance and lifecycle

Goal: sustainable SBOM operations.

Method:
- Scope: all products shipped and key internal services.
- Triggers: every build, dependency update, base image refresh, and vulnerability response.
- Retention: for the supported life of each version plus a legal tail (confirm with counsel).
- Metrics: percent of releases with SBOM, quality score, time from advisory to impacted list.
- Roles: product security owns programme, engineering teams own generation, legal owns licence review.
- Review CISA SBOM community guides for sharing and maturity.

Gotchas:
- One-off SBOM projects decay; embed in release gates.
- Hand-edited SBOMs lose trust.

Verify: release pipeline fails if SBOM missing.
