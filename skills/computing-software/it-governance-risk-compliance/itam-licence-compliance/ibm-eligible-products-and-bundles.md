---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ibm-eligible-products-and-bundles
name: ibm-eligible-products-and-bundles
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ibm-eligible-products-and-bundles, ibm-licensing, cloud pak, vpc, virtual processor core, passport advantage, ibm entitlement, bundled software, itam-licence-compliance]
level: sme
status: draft
description: "Track IBM entitlements through Passport Advantage, bundled products and Cloud Pak virtual processor core terms."
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

# IBM bundles, entitlements and Cloud Pak licensing

Goal: use bundled rights and avoid double licensing.

Method:
- Use Passport Advantage site entitlements and Proofs of Entitlement.
- Cloud Paks are licensed by Virtual Processor Core (VPC) or by other metrics per pak (confirm per pak); bundled components may be restricted to use within the pak.
- Map installed components to the bundle and check restricted-use clauses.
- Use IBM License Service (for Cloud Paks) to collect usage metrics in clusters.
- Document container-based usage and sub-capacity eligibility.

Gotchas:
- Using a bundled component outside the pak triggers standalone licensing.
- Software subscription and support (S&S) lapse stops upgrades.

Verify: bundle map and License Service report agree.
