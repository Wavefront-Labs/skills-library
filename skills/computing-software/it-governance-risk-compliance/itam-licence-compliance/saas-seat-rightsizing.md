---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.saas-seat-rightsizing
name: saas-seat-rightsizing
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [saas-seat-rightsizing, saas-licence-management, seat reclamation, inactive users, scim, tiering, saas rightsizing, last login, itam-licence-compliance]
level: practitioner
status: draft
description: "Reclaim inactive SaaS seats using last-login and feature usage, tier users and automate offboarding via SCIM."
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

# SaaS seat reclamation and rightsizing

Goal: pay only for active seats at the right tier.

Method:
- Pull last activity per user via vendor admin API or SSO.
- Define inactivity thresholds (e.g. 60-90 days) and notify before reclaiming.
- Move light users to cheaper tiers (viewer, light, collaborator).
- Use SCIM provisioning so removal from the IdP group deprovisions the seat.
- Review contract rules on seat reductions and true-down windows before the renewal date.

Gotchas:
- Annual contracts often forbid mid-term reductions; time the clean-up before renewal notice.
- Service accounts and integration users count seats.

Verify: seat utilisation target above 85% per app.
