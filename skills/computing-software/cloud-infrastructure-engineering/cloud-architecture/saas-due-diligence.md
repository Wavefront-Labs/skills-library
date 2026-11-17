---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.saas-due-diligence
name: saas-due-diligence
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, saas-due-diligence, saas, vendor-assessment, sso, scim, data-export, sig-questionnaire, caiq]
level: practitioner
status: draft
description: "Run due diligence before adopting a SaaS product: security evidence, SSO/SCIM, data residency and export, API limits, SLA, sub-processors and an exit plan."
sources: ["https://cloudsecurityalliance.org/research/topics/caiq", "https://sharedassessments.org/sig/", "https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final", "https://datatracker.ietf.org/doc/html/rfc7644"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SaaS adoption due diligence and integration

## Evidence to request
- **Assurance**: SOC 2 Type II report (check period, scope, exceptions, complementary user entity
  controls), ISO 27001 certificate + Statement of Applicability, CSA STAR / CAIQ answers, pen-test
  summary. A Type I report or "in progress" is not equivalent.
- **Questionnaire**: SIG Lite or CAIQ only for gaps the reports do not answer; long custom
  questionnaires waste both sides' time.
- **Sub-processors** list and change-notification terms.
- **Data**: hosting regions, residency options, encryption at rest (customer-managed keys?),
  retention and deletion on termination (timeline and certificate).

## Integration requirements
| Need | Check |
|---|---|
| SSO | SAML 2.0 or OIDC on your plan tier (often gated to "enterprise") |
| Provisioning | SCIM 2.0 (RFC 7644) for joiner/mover/leaver; without it accounts linger |
| Audit | Admin and access audit log export / API / SIEM integration |
| API | Rate limits, bulk export, webhooks, API key scopes |
| Data export | Full export in an open format, how long it takes for your data size |
| Availability | SLA %, measurement, credits, status page, incident history |

## Procedure
1. Classify the data the SaaS will hold (drives depth of review).
2. Collect evidence; read the SOC 2 exceptions and CUECs and assign each CUEC to an owner.
3. Test SSO + SCIM + export in a trial tenant.
4. Contract: DPA, breach notification time, liability caps, termination assistance.
5. Register the app (owner, data class, renewal date) in the SaaS inventory; set an annual review.

## Gotchas
- SSO tax: the security features you require may double the per-seat price; include in TCO.
- Shadow SaaS: discover via SSO logs, expense reports, CASB/DNS logs before rolling out policy.
- Export that exists only as a support ticket is not an exit plan.

## Verify
- [ ] Evidence filed and reviewed; exceptions risk-accepted by an owner.
- [ ] SSO enforced, local passwords disabled, SCIM deprovisioning tested.
- [ ] Export tested end to end.
