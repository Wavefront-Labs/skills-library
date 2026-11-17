---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.licence-risk-tiering-policy
name: licence-risk-tiering-policy
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [licence-risk-tiering-policy, licence-compatibility-analysis, licence policy, allow list, deny list, risk tiers, approval workflow, policy as code, itam-licence-compliance]
level: practitioner
status: draft
description: "Create allow, review and deny licence tiers by use case, such as distributed, SaaS, internal, and automate gating."
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

# Licence risk tiering and approval policy

Goal: fast decisions for common cases.

Method:
- Tier 1 allowed: MIT, BSD, ISC, Apache-2.0, Zlib, Unlicense/CC0 (check patents).
- Tier 2 review: LGPL, MPL, EPL, CDDL, CC-BY, Artistic.
- Tier 3 restricted: GPL/AGPL/SSPL/BSL in distributed or hosted contexts.
- Tier 4 denied: unknown, non-commercial, proprietary or no licence.
- Vary by use: internal tools, SaaS back-end, distributed product, mobile app store (GPL conflicts with app store terms in some views).
- Implement as policy code in the SCA scanner and CI.

Gotchas:
- "No licence" means all rights reserved, not public domain.
- Policy exceptions need expiry.

Verify: CI blocks a test dependency with a denied licence.
