---
id: computing-software.cybersecurity-defensive.security-operations.cyber-insurance-claim-notification
name: cyber-insurance-claim-notification
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [cyber-insurance-notification, incident-reporting, cyber-insurance, incident-response, claims, legal-privilege]
level: practitioner
status: draft
description: "Notify your cyber insurer of an incident: policy notice requirements, timelines, panel vendors, pre-approval of costs, documentation and pitfalls that jeopardise cover."
sources: ["https://www.ncsc.gov.uk/guidance/cyber-insurance-guidance", "https://www.cisa.gov/topics/cybersecurity-best-practices", "https://www.naic.org/cipr_topics/topic_cyber_risk.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cyber insurance claim notification

## Before an incident
- Know the policy: notice clause (e.g. "as soon as practicable", sometimes specific hours), breach
  hotline number, panel vendors (DFIR, legal, PR, negotiation) and whether non-panel vendors are
  covered, retention/deductible, sublimits (ransom, business interruption, regulatory fines where
  insurable), exclusions (war/state-backed, unpatched known vulnerabilities, failure to maintain
  stated controls).
- Put the hotline number and policy number in the IR plan and offline copies.

## At notification
1. Call the insurer's breach hotline early, even before scope is known; follow with written notice.
2. Provide: policy number, discovery date/time, brief description, systems affected, actions taken,
   contacts.
3. Get panel counsel engaged (often via insurer) and route DFIR engagement through counsel.
4. Obtain **pre-approval** for significant costs (DFIR, ransom negotiation/payment, PR, overtime)
   before committing where the policy requires consent.

## During the claim
- Keep a cost log with invoices tied to the incident; separate business interruption calculations
  (lost revenue, extra expense) with finance from day one.
- Be accurate: statements in the application about controls (MFA, backups, EDR) are checked against
  forensic findings; misrepresentation risks denial.
- Ransom payments: insurer and counsel coordinate sanctions checks (OFAC etc.).

## Gotchas
- Late notice can void cover; notify on suspicion.
- Engaging non-panel firms without consent may not be reimbursed.
- Admissions of liability to third parties without insurer consent can breach policy terms.

## Verify
Claim file contains notification timestamps, insurer acknowledgements, cost approvals, and invoices
reconciled to the incident.
