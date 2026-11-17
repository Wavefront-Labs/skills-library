---
id: sales-marketing.sales-management.sales-process-design.stage-exit-criteria-and-handoffs
name: stage-exit-criteria-and-handoffs
category: sales-marketing
field: sales-management
product: sales-process-design
tags: [sales-process-design, sales-process, sales-stages, deal-stages, exit-criteria, qualification, bant, meddic, meddpicc, spiced, playbook, sales-playbook, sdr, bdr, ae, account-executive, customer-success, handoff, lead-handoff, service-level-agreement, sla, crm-stages, revops, sales-management]
level: practitioner
status: draft
description: "Define how the team sells: 5-7 buyer-verified stages with exit criteria, one qualification standard, a playbook per stage, and clean SDR-to-AE and AE-to-CS handoffs with SLAs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stage exit criteria and handoffs

**Goal:** everyone means the same thing by "stage 3", deals move only on evidence from the
buyer, and nothing drops between teams.

## 1. Map how your buyers buy, then name the stages
Interview reps on 5–10 recent wins and losses: what did the buyer do at each step? Build
5–7 stages from that. A typical B2B example:
1. **Qualify** — first meeting held.
2. **Discover** — problem, impact and decision process understood.
3. **Solution/Demo** — tailored demo or trial done.
4. **Proposal** — pricing and scope sent.
5. **Negotiate/Commit** — verbal yes, contract in legal/procurement.
6. **Closed won / Closed lost.**

## 2. Exit criteria = buyer-verifiable evidence
Each stage gets 2–4 criteria that must be true to move forward, phrased as things you can
check, not rep feelings:
| Stage | Exit criteria (example) |
|---|---|
| Qualify | Fits ideal customer profile; a pain is named; next meeting booked |
| Discover | Pain quantified; decision-maker identified; buying process and timeline written down |
| Solution | Buyer confirmed demo meets requirements; champion identified |
| Proposal | Pricing reviewed live with decision-maker; mutual close plan agreed |
| Commit | Verbal approval; paperwork path and signer confirmed |
Put these into the CRM as **required fields** at stage change where your CRM supports it
(Salesforce validation rules or path guidance; HubSpot required properties per stage —
check your edition).

## 3. Pick one qualification standard
Choose one framework and use its words everywhere:
- **BANT** (Budget, Authority, Need, Timeline) — simple, suits transactional sales.
- **MEDDIC/MEDDPICC** (Metrics, Economic buyer, Decision criteria, Decision process,
  [Paper process], Identify pain, Champion, [Competition]) — suits complex enterprise.
- **SPICED** (Situation, Pain, Impact, Critical event, Decision) — common in SaaS.
Map its elements to stage exit criteria so qualification isn't a separate form.

## 4. Handoffs with SLAs
**SDR/BDR → AE:**
- Definition of a qualified meeting written down (e.g. ICP fit + named pain + attended).
- Handoff note in CRM: who, role, pain in their words, why now.
- AE accepts or rejects within an agreed time (e.g. 48 h) with a reason; SDR is credited on
  acceptance, not booking.
**AE → Customer Success/Onboarding:**
- Handoff doc at closed won: goals the customer bought for, success metrics, stakeholders,
  promises made, contract terms. Kickoff meeting with the AE present.

## 5. The playbook
One page per stage: goal, exit criteria, key questions, assets (deck, calculator, case
studies), common objections, and what "bad" looks like. Short and maintained beats
complete and stale.

## 6. Roll out and enforce
Train with real deals; the forecast call inspects by exit criteria; review stage
conversion monthly. Expect a temporary dip in pipeline as inflated deals move back.

## Gotchas
- Stages named after seller activity ("sent proposal") inflate pipeline; tie to buyer actions.
- Too many required fields → reps type junk. Keep 2–4 per stage.
- Changing stages mid-quarter breaks historical win-rate math; snapshot first.
- Framework names are trademarks/brand-associated in some cases; that's fine for internal use.

## Verify
- [ ] Each stage has 2–4 buyer-verifiable exit criteria, written and in the CRM.
- [ ] One qualification framework is used in stages, calls and forecast.
- [ ] SDR→AE acceptance SLA tracked with reject reasons.
- [ ] Every closed-won deal has a completed CS handoff doc.
- [ ] Stage-to-stage conversion reviewed monthly.
