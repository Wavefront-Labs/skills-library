---
id: sales-marketing.technical-b2b-sales.proof-of-concept-demos.tailored-demos-and-poc-success-criteria
name: tailored-demos-and-poc-success-criteria
category: sales-marketing
field: technical-b2b-sales
product: proof-of-concept-demos
tags: [proof-of-concept-demos, poc, proof-of-concept, pilot, trial, evaluation, demo, product-demo, tailored-demo, sales-engineer, solutions-engineer, presales, demo-script, tell-show-tell, success-criteria, success-plan, mutual-action-plan, pilot-to-contract, demo-environment, sandbox, technical-win, b2b-sales, saas-sales]
level: practitioner
status: draft
description: "Sell with the product: a tailored demo built from discovery, tell-show-tell flow, and a time-boxed POC with written success criteria that converts to a contract instead of an endless free trial."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tailored demos and POC success criteria

**Goal:** show the buyer their own problem being solved, then — only if needed — run a
short, scoped proof of concept whose agreed pass criteria lead straight to a purchase.

## 1. Tailored demo (never the generic tour)
**Inputs from discovery:** top 2–3 pains in the buyer's words, their metrics, who attends
and what each cares about. No discovery → reschedule or run a discovery call first
(sales-marketing.technical-b2b-sales.discovery-calls.running-a-qualifying-discovery-call).

**Prepare the environment**
- Demo tenant with *their* terminology, logo, and realistic sample data (anonymised or
  synthetic — never another customer's data).
- Reset script or snapshot so the demo starts clean every time.
- Backup: recorded video of each segment, in case of network or environment failure.
- Close notifications, use a clean browser profile, zoom to ~125–150% for screen-share legibility.

**Structure (30–45 min)**
1. Recap the pains and agree the agenda: "You said A, B, C. I'll show those three; stop me anytime."
2. For each pain — **Tell-Show-Tell**:
   - Tell: "You said month-end takes 5 days because of manual matching."
   - Show: the shortest path to the outcome (the "wow" first, configuration later).
   - Tell: "So that's matching done in minutes — what would that mean for your close?"
3. Check in after each segment ("How does that compare with today?").
4. End with next step, not features: "What would you need to see to be confident?"
Rule of thumb: show less. Every extra feature is a chance to confuse or raise objections.

## 2. Decide whether a POC is needed
POCs cost both sides weeks. Run one only when: the technical risk is real (integration,
scale, data quality), the buyer's process requires it, and the deal size justifies it.
Otherwise offer references, a technical deep-dive or a sandbox walkthrough.

## 3. Scope the POC in writing (success plan)
One page, signed or emailed back by the buyer's decision-maker:
- **Objective**: the business question the POC answers.
- **Success criteria** — specific, measurable, binary: "Ingest the 3 named data sources;
  reconcile last month's 40k transactions with ≥ 98% auto-match; run under 10 min."
- **Scope out**: what is explicitly not being tested.
- **Duration**: time-boxed (often 2–4 weeks), start and end dates.
- **Resources**: named people on both sides, access, data, environments.
- **Decision**: "If the criteria are met, we will proceed to <commercial step> by <date>."
- Paid vs free: a paid pilot (credited against the contract) filters out tyre-kickers.

## 4. Run it
- Kick-off with both teams; weekly check-ins against criteria; shared tracker
  (criterion · status · evidence · owner).
- Surface blockers early (data access, security approval) — they're the usual reason POCs slip.
- Keep the commercial conversation running in parallel: pricing, legal and procurement
  shouldn't start only after the POC ends.

## 5. Close-out meeting
Present results against each criterion with evidence; get the buyer to confirm "met / not met".
Then ask for the decision agreed in §3. If a criterion missed, agree whether it blocks.

## Gotchas
- "Let's just try it" without criteria → endless free trial that never closes.
- Scope creep mid-POC; new asks go into a "phase 2" list, not this POC.
- Demoing the roadmap as if it ships today — say clearly what's GA vs planned.
- The real users not involved in the POC, then rejecting the tool later.

## Verify
- [ ] Demo built from documented discovery pains, with a tested reset and video backup.
- [ ] Each demo segment tied to a stated pain and checked in on.
- [ ] POC has written, measurable success criteria and a decision clause agreed by the buyer.
- [ ] POC time-boxed with named resources and a weekly tracker.
- [ ] Commercial steps progressed in parallel; close-out meeting booked before kick-off.
