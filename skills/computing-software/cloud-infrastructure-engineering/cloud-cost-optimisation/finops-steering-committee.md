---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-steering-committee
name: finops-steering-committee
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-policy-governance, finops-governance, finops-steering-committee, governance-forum, decision-log]
level: practitioner
status: docs-checked
description: "Set up a FinOps governance body using the FinOps Framework: personas to include, accountability and escalation, decision log, and Crawl/Walk/Run governance maturity."
sources:
  - https://www.finops.org/framework/capabilities/policy-governance/
  - https://www.finops.org/framework/personas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps steering committee (governance body)

The FinOps Framework does not prescribe a "steering committee"; its Policy and Governance capability
talks about governance bodies, processes, accountabilities and controls. This skill applies that
capability to a cross-functional decision forum.

## What the Framework says governance is
- Governance is the set of mechanisms (bodies, processes, accountabilities and controls) for
  evaluating options, setting direction and monitoring compliance. Policy translates governance
  direction into actionable rules.
- Policies disconnected from governance bodies tend to create compliance theatre rather than real
  control.
- Governance procedures should establish accountability, escalation paths and decision-making
  processes for technology spend and usage. Risk thresholds are set with Finance, Leadership and
  other personas, and Leadership accepts accountability for risk decisions within its authority.
- Mechanisms are guidelines (advisory), guardrails (mandatory pathways) and automation.

## Who to include (Framework personas)
| Persona | Contribution to governance |
|---|---|
| FinOps Practitioner | defines policy and coordinates governance mechanisms |
| Engineering | implements controls and escalates risk signals |
| Finance | contributes KPIs and aligns policy to financial governance |
| Procurement | aligns vendor management to policy; routes purchases through governance review |
| Product | applies policy in planning ("shifting left") |
| Leadership | sets governing principles and enforces compliance |

Allied personas listed by the Framework include ITAM, ITFM, Sustainability, ITSM/ITIL and
Security; bring them in when their topic is on the agenda.

## Maturity (Policy and Governance capability)
- **Crawl:** governance is informal, with no regular cadence or structured communication; compliance
  is checked manually during design review.
- **Walk:** cross-functional collaboration with Finance, Engineering, Procurement, Security and
  Risk is established and a regular review cadence exists; enforcement is still manual.
- **Run:** the FinOps team is a recognised participant in enterprise governance, risk and
  compliance processes; policy is enforced automatically in build and deployment tooling, with
  exception records feeding back into design.

## Working practice (suggestions, not from the Framework)
- Write terms of reference: purpose, membership, decision method, cadence, and what the FinOps
  practitioner may decide alone versus what comes to the forum.
- Keep a decision log: date, decision, options considered, owner, due date, status. Publish it so
  engineers can see why a policy exists, and trace each policy in force to a logged approval.
- Decisions without owners and dates do not happen; review attendance and decisions periodically.

## Verify
- [ ] Each meeting produces logged decisions with owners.
- [ ] Policies in force trace back to a logged approval.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the FinOps Framework Policy and Governance capability page and the Personas page. Removed because neither page states them: membership of 6-10 people, the chair role, the monthly 60-minute agenda with timings, the 48-hour pre-read rule, the scorecard metrics, and the claim that status forums die within two quarters. The pages do not use the terms "steering committee" or "governance forum".
