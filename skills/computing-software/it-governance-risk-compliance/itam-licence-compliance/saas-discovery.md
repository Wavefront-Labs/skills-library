---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.saas-discovery
name: saas-discovery
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [saas-discovery, saas-licence-management, saas discovery, shadow it, sso logs, casb, expense data, saas management platform, itam-licence-compliance]
level: practitioner
status: draft
description: "Discover SaaS applications through SSO logs, finance data, expense reports and browser or CASB signals."
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

# SaaS discovery and shadow IT

Goal: complete inventory of SaaS in use.

Sources, from most to least reliable:
- IdP/SSO app catalogue and OAuth grants (Entra enterprise apps, Okta, Google Workspace).
- Finance: card statements, AP vendor lists and expense claims.
- CASB and secure web gateway logs.
- Browser extensions or endpoint agents.
- Survey of department heads.

Method: merge into a register with app owner, users, spend, data classification, contract end and SSO status; triage unapproved apps (approve, replace, block).

Gotchas:
- OAuth grants to consumer apps leak data; review and revoke.
- Free tiers become paid silently.

Verify: top 20 apps by spend all have named owners.
