---
id: business-finance.product-management.roadmapping-and-prioritisation.outcome-roadmap-and-rice-prioritisation
name: outcome-roadmap-and-rice-prioritisation
category: business-finance
field: product-management
product: roadmapping-and-prioritisation
tags: [product-management, roadmapping-and-prioritisation, product-roadmap, now-next-later, outcome-based-roadmap, prioritization, prioritisation, rice, rice-score, weighted-scoring, ice, moscow, kano, cost-of-delay, wsjf, stakeholder-management, saying-no, scope-negotiation, backlog, jira-product-discovery, productboard, aha]
level: practitioner
status: draft
description: "Build an outcome-based Now/Next/Later roadmap, score candidates with RICE or weighted scoring without fooling yourself, run stakeholder trade-offs, and say no with reasons people accept."
sources: ["Intercom - RICE prioritisation framework (Sean McBride, 2016)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Outcome roadmap and RICE prioritisation

**Goal:** a roadmap that communicates *why* and *in what order*, with dates only where
they're real, and a prioritisation process stakeholders trust even when they lose.

## 1. Roadmap format: Now / Next / Later, by outcome
- **Now** (this quarter, committed): specific initiatives, owners, rough sizing.
- **Next** (next 1-2 quarters): problems/opportunities you intend to tackle; solutions
  still open.
- **Later**: themes. Explicitly uncertain.
Group items under the **outcome** they serve ("cut onboarding drop-off from 40% to
25%"), not under features. Each outcome links to a strategy bet
(see business-finance.product-management.product-strategy).
Avoid a Gantt with features on dates 12 months out: it becomes a promise you'll break,
and the date gets remembered while the caveats don't. Where a real external date
exists (regulation, contract, event), show it as a fixed milestone.

## 2. Prioritise with RICE (or a weighted score)
RICE = **Reach × Impact × Confidence ÷ Effort**
- **Reach**: users/accounts affected per period (e.g. per quarter), from data.
- **Impact**: per user, on the target outcome. Use a fixed scale: 3 massive, 2 high,
  1 medium, 0.5 low, 0.25 minimal.
- **Confidence**: 100% (data), 80% (some evidence), 50% (gut). Below 50% means
  "do discovery first" rather than score it.
- **Effort**: person-months across all functions (estimate from engineering + design).
Do it in a shared spreadsheet with the inputs visible and the source of each number.
Weighted scoring alternative: 3-5 criteria agreed with leadership (strategic fit,
revenue, retention, risk reduction, effort), weights summing to 100%, each scored 1-5.
Use **cost of delay / WSJF** when timing matters (regulatory deadlines, seasonal value).

## 3. Use scores as a conversation, not an oracle
- Sort, then sanity-check the top 10 with the team. If something obviously important
  scores low, a missing criterion (e.g. compliance, platform health) is the cause:
  add it explicitly rather than fiddling numbers.
- Reserve capacity outside the scoring: commonly ~15-30% for tech debt, bugs and
  platform work (rule of thumb, varies by team maturity).
- Revisit scores quarterly; Reach and Confidence change as you learn.

## 4. Stakeholder trade-offs
- Collect requests in one intake (form, Jira Product Discovery, Productboard, Aha!),
  each tagged with requester, customer evidence and the outcome it serves.
- Run a regular review (monthly) where stakeholders see the scored list. Transparency
  is what makes "no" acceptable.
- Frame trade-offs as swaps: "We can add X this quarter if we move Y to Next. Which
  matters more for the revenue target?" Let the accountable exec pick.

## 5. Saying no well
"Not now, because <outcome we're prioritising>; here's where it sits and what would
change that (more customers asking, a revenue figure, a deadline)." Log it, so the
requester can see it wasn't lost. Re-surface it if the evidence arrives.

## 6. Scope negotiation inside an initiative
Fix time and team, flex scope. Define the **smallest version that moves the outcome**
(appetite), list what's explicitly out, and keep a "fast follow" list.

## Gotchas
- Everyone inflates Impact for their pet item; calibrate against shipped work's actual impact.
- Effort estimated by PM alone is fiction; ask the people who'll build it.
- Roadmap tools don't prioritise for you; garbage scores in, polished garbage out.
- Publishing internal Later items externally creates commitments sales will sell.

## Verify
- [ ] Every Now item maps to a stated outcome.
- [ ] RICE inputs have sources and Confidence below 50% sends items to discovery.
- [ ] Capacity reserved for debt/bugs is explicit.
- [ ] Declined requests logged with the reason and revisit trigger.
- [ ] No feature has a date more than a quarter out unless externally fixed.
