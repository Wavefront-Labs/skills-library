---
id: sales-marketing.digital-marketing.meta-ads.campaign-setup-creative-testing-and-capi
name: campaign-setup-creative-testing-and-capi
category: sales-marketing
field: digital-marketing
product: meta-ads
tags: [meta-ads, facebook-ads, instagram-ads, ads-manager, paid-social, campaign-objectives, sales-objective, leads-objective, advantage-plus, advantage-plus-shopping, advantage-plus-audience, broad-targeting, lookalike-audiences, custom-audiences, retargeting, creative-testing, dynamic-creative, ugc-ads, meta-pixel, conversions-api, capi, event-match-quality, aggregated-event-measurement, cbo, learning-phase, creative-fatigue, frequency, scaling]
level: practitioner
status: draft
description: "Run Meta (Facebook/Instagram) ads: pixel plus Conversions API, objective and Advantage+ setup, broad vs custom audiences, structured creative testing, learning phase, scaling and fatigue."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Meta ads — tracking, setup, creative testing, scaling

**Goal:** profitable paid social on Facebook and Instagram, where creative does most
of the targeting and the algorithm gets clean conversion signals.

Meta renames and restructures campaign options frequently (Advantage+ features,
objective names). The principles hold; check Ads Manager and Meta's Business Help
Center for current labels.

## 1. Tracking: pixel + Conversions API
- Install the **Meta Pixel** and set up the **Conversions API (CAPI)** — via your
  e-commerce platform's integration (Shopify, WooCommerce etc.), a partner, or server-side
  GTM. Send the same events from both with a shared `event_id` for **deduplication**.
- Pass hashed customer info (email, phone) where consented to raise **Event Match Quality**
  (shown in Events Manager).
- Verify the domain in Business Manager and configure event priorities as required.
- Test in Events Manager's Test Events tool; check purchase values match orders.

## 2. Campaign setup
- Pick the objective matching the outcome you want (Sales, Leads, etc.) and optimise
  for the deepest event you get enough of — purchases ideally; Meta's guidance has been
  roughly 50 optimisation events per ad set per week to exit the learning phase.
- **Advantage+ shopping / sales campaigns** automate audience and placement for
  e-commerce; good default for prospecting at scale. Set an existing-customer budget cap
  if you want mostly new buyers.
- **Campaign budget optimisation (CBO / Advantage campaign budget)** distributes spend
  across ad sets; use ad-set budgets when you need forced spend on a test.
- Placements: Advantage+ placements by default; exclude only with evidence.

## 3. Audiences
- **Broad** (age/country only) with strong creative often beats detailed interests now.
- **Custom audiences:** site visitors, customer lists, video viewers, engagers — for
  retargeting and exclusions (exclude recent purchasers from prospecting).
- **Lookalikes** from high-value customer lists as an alternative prospecting test.
Keep audiences large enough that ad sets don't overlap heavily or exhaust quickly.

## 4. Creative testing (the main lever)
- Formats: short vertical video (9:16) for Reels/Stories, 1:1 or 4:5 for feed, carousels
  for catalogues. Hook in the first 1–3 seconds, captions on (most watch muted).
- Test **concepts** (angles: problem/solution, testimonial/UGC, demo, offer, comparison)
  before small tweaks (colour, button).
- A clean test: a dedicated campaign/ad set with equal conditions, 3–5 new ads, budget
  enough for each to get meaningful conversions or at least a strong leading metric
  (hook rate, CTR, cost per add-to-cart). Meta's A/B test tool gives a controlled split.
- Graduate winners into the main scaling campaign.

## 5. Learning phase and scaling
- Avoid significant edits (budget jumps, targeting, new creative in the same ad set)
  during learning; each resets it.
- **Scale vertically** with budget increases of ~20–30% every few days, or **horizontally**
  by duplicating winners into new campaigns/audiences.
- Judge on blended results (MER) as well as Ads Manager ROAS, which uses Meta's own
  attribution window (default 7-day click, 1-day view — check your setting).

## 6. Fatigue
Watch frequency rising alongside falling CTR and rising CPA on an ad — refresh creative
(new hooks on proven concepts) on a regular cadence; big accounts need new creative weekly.

## Gotchas
- iOS privacy changes reduced tracked conversions; CAPI recovers some, not all.
- Many tiny ad sets = none exit learning.
- Special Ad Categories (credit, employment, housing, social issues/politics) restrict
  targeting — declare them or ads get rejected.
- Policy rejections for "personal attributes" wording ("Are you overweight?") are common.

## Verify
- [ ] Pixel and CAPI both firing with deduplication; Event Match Quality checked.
- [ ] Objective optimises for purchases/leads with enough weekly volume.
- [ ] Recent purchasers excluded from prospecting.
- [ ] Creative test run on concepts with a controlled split; winners graduated.
- [ ] Budget changes ≤ ~30% at a time; frequency and CTR monitored for fatigue.
