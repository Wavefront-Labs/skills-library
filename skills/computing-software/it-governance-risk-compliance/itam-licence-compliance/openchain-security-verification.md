---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.openchain-security-verification
name: openchain-security-verification
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [openchain-security-verification, openchain-iso-18974, vulnerability disclosure, security.txt, cve numbering authority, residual risk, security advisory, coordinated disclosure, itam-licence-compliance]
level: advanced
status: draft
description: "Verify open-source security processes, disclose vulnerabilities responsibly and demonstrate residual-risk decisions."
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

# OpenChain security verification and disclosure

Goal: close the loop on identified vulnerabilities.

Method:
- Verification: periodic testing of the process (tabletop or mock advisory).
- Disclosure: publish a vulnerability disclosure policy and security.txt (RFC 9116) with contact and PGP key; consider becoming a CNA or using a coordinating CNA.
- Advisories: communicate affected versions, fixes, workarounds and VEX data.
- Residual risk: document accepted risks with owner and review date.
- Maintain evidence for audits.

Gotchas:
- Do not expose reporter identities without consent.
- Late advisories erode trust more than imperfect ones.

Verify: policy page and security.txt are live and monitored.
