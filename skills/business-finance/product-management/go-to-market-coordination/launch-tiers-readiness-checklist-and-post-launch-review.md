---
id: business-finance.product-management.go-to-market-coordination.launch-tiers-readiness-checklist-and-post-launch-review
name: launch-tiers-readiness-checklist-and-post-launch-review
category: business-finance
field: product-management
product: go-to-market-coordination
tags: [product-management, go-to-market-coordination, go-to-market, gtm, product-launch, launch-plan, launch-tiers, launch-readiness, readiness-checklist, go-no-go, sales-enablement, internal-enablement, product-marketing, release-notes, feature-flags, phased-rollout, beta-program, post-launch-review, retrospective, raci, cross-functional]
level: practitioner
status: draft
description: "Coordinate a launch from the product seat: tier it, build a cross-functional plan with owners, run a readiness checklist and go/no-go, enable sales and support, and hold a post-launch review."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Launch tiers, readiness checklist and post-launch review

**Goal:** every function that touches customers is ready on day one, the launch effort
matches the size of the change, and you learn whether it worked.

## 1. Tier the launch first
| Tier | What | Effort |
|---|---|---|
| 1 | New product, new pricing, major repositioning | Full plan, PR/analyst, events, sales training, exec sponsor |
| 2 | Significant feature for an existing segment | Blog, email to relevant users, enablement session, in-app announcement |
| 3 | Small improvement, fix | Release notes, changelog, help-centre update |
Agree the tier with product marketing early. Over-launching small things trains
customers to ignore announcements; under-launching big ones wastes the build.

## 2. Roles (who owns what)
PM owns: the *what* and *when*, readiness tracking, go/no-go call, success metrics.
Product marketing (PMM) usually owns: positioning, messaging, launch content, sales
collateral. Engineering: release, flags, monitoring. Support/CS: macros, help docs,
escalation path. Sales: pitch, pricing/quoting, deal desk. Legal/compliance: terms,
privacy review, claims in marketing copy. Write it as a RACI in the launch doc.
Smaller companies: the PM often does PMM's part; budget time for it.

## 3. Launch plan (one doc, one channel)
Timeline working back from launch date (T): e.g. T-6 weeks messaging draft; T-4 beta
feedback in; T-3 enablement content; T-2 sales/support training; T-1 go/no-go;
T launch; T+2 weeks first metrics read; T+4–6 weeks post-launch review.
One Slack/Teams channel and one tracker (spreadsheet or project board) with owner and
status per item.

## 4. Readiness checklist (adapt per tier)
**Product**: feature complete to acceptance criteria; feature flag and rollback plan;
monitoring/alerts; analytics events firing; performance tested at expected load;
phased rollout plan (internal → beta → %-based → all).
**Customer-facing**: help-centre articles; in-app copy reviewed; release notes;
pricing/packaging live in billing and CPQ; localisation if needed.
**Support/CS**: trained; macros and FAQs; known issues list; escalation path and
on-call named for launch week.
**Sales**: talk track, demo environment, objection handling, who it's for and **not**
for, competitive notes.
**Legal/compliance**: terms updates, privacy/DPIA where personal data is new, marketing
claims substantiated.
**Comms**: customer email, blog, social, press (tier 1), internal announcement.

## 5. Go/no-go meeting (T-1 week and launch-day morning)
Walk the checklist; each owner says ready / not ready. Pre-define **blocking criteria**
(e.g. P1 bugs open, billing not live, support untrained) so the call is mechanical.
Slipping a date is cheaper than a broken launch with customers watching; for tier 1,
have a fallback date pre-agreed with marketing (press embargoes and events make slips
expensive).

## 6. Launch day and week
Staged rollout with someone watching dashboards; support channel monitored; a
launch-day standup; quick fixes prioritised over new work for the week.

## 7. Post-launch review (4-6 weeks after)
Compare against success metrics set before launch (adoption, activation, revenue,
support tickets). Blameless retro: what went well, what didn't, what we change in the
launch template. Share results with everyone who contributed; it's the payoff for
cross-functional goodwill. Decide: iterate, invest more, or sunset.

## Gotchas
- Sales hears about features from customers first: the most common enablement failure.
- Docs written by engineers after launch day lag reality; schedule them in the plan.
- "Launched" isn't "adopted": many features see low uptake without in-product prompts.
- Pricing changes need billing-system lead time often longer than the feature build.

## Verify
- [ ] Tier agreed with PMM and documented.
- [ ] RACI and dated plan in one doc; every checklist item has an owner.
- [ ] Blocking criteria defined before go/no-go.
- [ ] Sales and support trained before customers are told.
- [ ] Post-launch review booked at launch time, with pre-set success metrics.
