---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.clear-purge-destroy-selection
name: clear-purge-destroy-selection
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [clear-purge-destroy-selection, media-sanitisation-nist-800-88, nist 800-88, clear, purge, destroy, sanitisation, data sensitivity, itam-licence-compliance]
level: practitioner
status: draft
description: "Select Clear, Purge or Destroy per NIST 800-88 using data sensitivity, media type and whether the device leaves control."
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

# Choosing clear, purge or destroy

Goal: pick the minimum method that makes data recovery infeasible for the risk.

NIST SP 800-88 Rev.1 categories:
- Clear: logical overwrite, protects against simple non-invasive recovery; typical for devices staying in the organisation.
- Purge: makes recovery infeasible even with laboratory attack (cryptographic erase, block erase, firmware secure erase, degauss for magnetic).
- Destroy: physical destruction (shred, disintegrate, incinerate) so media cannot be reused.

Method:
1. Classify data impact (low/moderate/high).
2. Decide if media leaves your control.
3. Moderate or high impact leaving control: Purge or Destroy.
4. Record the method and tool version per asset.

Gotchas:
- Overwriting SSDs does not reach remapped blocks; use crypto or block erase.
- Failed drives cannot be wiped; they go to destroy.

Verify: sanitisation record exists per serial and sampled media is validated.
