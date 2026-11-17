---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.outbound-contribution-policy
name: outbound-contribution-policy
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [outbound-contribution-policy, contribution-and-relicensing, dco, cla, contribution policy, signed-off-by, upstream, employee contributions, itam-licence-compliance]
level: practitioner
status: draft
description: "Let employees contribute to open source safely: approval flow, IP assignment checks, DCO sign-off and CLAs."
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

# Outbound contribution policy and DCO/CLA

Goal: contribute without leaking IP.

Method:
- Approval flow: manager, legal/OSPO check of content (no confidential code), licence compatibility with project.
- DCO: contributors add Signed-off-by to commits (git commit -s), asserting right to contribute.
- CLA: a project may require ICLA/CCLA (Apache-style) granting licence to the project; corporate CLA signed by the employer.
- Track contributions in a register with project, licence, patches and owner.
- Preferred upstream-first over private forks.

Gotchas:
- Contractors' IP assignment may not cover open contributions.
- Contributing patent-encumbered code triggers patent grants.

Verify: register shows approvals for every external pull request.
