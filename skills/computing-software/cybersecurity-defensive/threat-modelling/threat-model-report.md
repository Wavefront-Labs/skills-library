---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-model-report
name: threat-model-report
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [stride, threat-model-report, four-question-framework, threat-register, mitigation-tracking, assumptions, security-documentation]
level: practitioner
status: draft
description: "Write a threat model document people use: scope and assumptions, diagram, threat register with status, mitigations linked to tickets, residual risk, and when to revise it."
sources: ["https://www.threatmodelingmanifesto.org/", "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html", "https://github.com/OWASP/threat-model-cookbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat model report

The output of threat modelling is decisions and work items, not a diagram. The document answers the
four questions: what are we working on, what can go wrong, what are we going to do about it, did we
do a good job?

## Structure
1. **Header**: system, version/commit or design doc reference, date, participants, owner, review date.
2. **Scope**: in scope components and flows; explicitly out of scope (e.g. "corporate SSO, covered
   by its own model").
3. **Assumptions and dependencies**: "TLS terminates at the load balancer", "the IdP enforces MFA",
   "S3 buckets are private by org policy". Assumptions are where threats hide; each one is checkable.
4. **System description**: DFD with trust boundaries; data classification of key data stores;
   entry points; external dependencies.
5. **Threat register** (table):
   | ID | Component/flow | Threat (STRIDE) | Scenario | Likelihood/impact | Mitigation | Status | Ticket |
   Status values: Mitigated (existing control, evidence), Planned (ticket), Accepted (owner + reason +
   review date), Transferred, Not applicable (why).
6. **Mitigation summary**: grouped by owner/team with ticket links.
7. **Residual risks** needing sign-off.
8. **Validation**: tests that prove mitigations (unit/integration tests, pentest scope items).

## Writing threats well
Specific and testable: "An authenticated user changes `account_id` in `PUT /api/invoices/{id}` to edit
another tenant's invoice (Tampering, BOLA)" beats "Tampering with data".
Avoid generic lists copied from a template; every threat should mention this system's components.

## Keep it alive
- Store as Markdown in the repo next to the code (`docs/threat-model.md`) or in the threat modelling
  tool, linked from the design doc.
- Revisit on triggers: new external interface, auth change, new data class, major architecture
  change; and at least yearly.
- Pull request template asks "does this change the threat model?".

## Gotchas
- 60-page reports nobody reads; prefer 3-8 pages plus the register.
- Accepted risks without an owner and expiry turn into permanent unknowns.
- Mitigations claimed without evidence ("we validate input") are assumptions, not mitigations.

## Verify
Every threat has a status; every Planned item has a ticket; a reviewer outside the team can trace three
threats from diagram to ticket to test.
