---
id: sales-marketing.advertising-creative-and-media-buying.programmatic-platforms.dsp-campaign-setup-and-controls
name: dsp-campaign-setup-and-controls
category: sales-marketing
field: advertising-creative-and-media-buying
product: programmatic-platforms
tags: [programmatic-platforms, programmatic, dsp, demand-side-platform, the-trade-desk, ttd, dv360, display-and-video-360, amazon-dsp, open-exchange, pmp, private-marketplace, deal-id, programmatic-guaranteed, ctv, connected-tv, display, online-video, bid-strategy, frequency-cap, audience-targeting, first-party-data, brand-safety, ias, doubleverify, ivt, ad-fraud, supply-path-optimisation, ads-txt]
level: practitioner
status: draft
description: "Set up a programmatic campaign in a DSP (The Trade Desk, DV360, Amazon DSP): deals vs open exchange, audiences, bids, frequency caps, brand-safety and fraud controls, and first-week QA."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Programmatic DSP campaign setup and controls

**Goal:** launch a display/video/CTV campaign in a demand-side platform that buys the
right audience on quality inventory at a controlled price, and catch problems in week one.

UI labels differ across The Trade Desk, DV360 and Amazon DSP and change often; the
structure below is common to all three, but check current menu names in each platform.

## 1. Structure
- **Campaign / advertiser level:** total budget, flight dates, pixels/conversion tags,
  attribution windows.
- **Ad group / line item / insertion order:** one per meaningful split (channel:
  display vs OLV vs CTV; tactic: prospecting vs retargeting; deal vs open market).
  Keep splits few enough that each line spends meaningfully — dozens of tiny lines
  starve the bidding algorithm of data.

## 2. Choose the supply
| Route | What it is | Use for |
|---|---|---|
| Open exchange | Real-time auction on all available inventory | Scale, low CPM, needs strong filters |
| Private marketplace (PMP) | Invite-only auction via a **deal ID** | Premium publishers, CTV apps |
| Preferred deal | Fixed price, first look, no guarantee | Priority access |
| Programmatic guaranteed | Fixed price & volume, booked like direct | Guaranteed premium/CTV |
Add deal IDs from the seller into the line; test each deal is actually bidding (a deal
with zero bids usually means a targeting or creative-spec mismatch).

## 3. Targeting
- **Audiences:** first-party lists (CRM uploads, site visitors), retailer/partner data
  (e.g. Amazon shopping signals in Amazon DSP), third-party segments (cost extra per CPM),
  contextual categories. Avoid stacking so many layers that reach collapses.
- **Geo, device, daypart, language.**
- **Frequency cap:** e.g. 3–5 per user per week for prospecting display; household-level
  for CTV. Starting points only — tune to the plan's frequency goals.

## 4. Bidding
- Start with the platform's goal-based bidding (CPA, ROAS, viewable CPM, completion
  rate) where you have conversion volume; use fixed/max CPM bids where you don't.
- Set a max bid ceiling so the algorithm can't chase expensive impressions.
- Expect a learning period (days) after launch or major edits; avoid daily tinkering.

## 5. Brand safety and fraud
- Apply **verification** (IAS, DoubleVerify or the platform's built-in) pre-bid
  filters: brand-safety categories, invalid traffic (IVT), viewability thresholds.
- Use **inclusion lists** for sensitive brands; exclusion lists (sites/apps) at minimum.
- Prefer supply paths that are authorised in the publisher's **ads.txt / app-ads.txt**;
  supply-path optimisation cuts reseller hops and fraud risk.
- Wrap or tag creatives for post-bid measurement of viewability and IVT.

## 6. First-week QA
Day 1: confirm each line is spending, pixels fire, creatives approved. Days 2–7: check
site/app placement reports for junk inventory (made-for-advertising sites, app
bundles with tiny CTR spikes = suspect), win rate, CPM, viewability, IVT %, frequency.
Add exclusions and adjust bids, then leave it to learn.

## Gotchas
- High CTR on display is often accidental clicks or bots, not interest.
- CTV "reach" can include mobile/desktop if device targeting isn't explicit.
- Third-party cookie-dependent segments may be thin or unavailable on some browsers;
  check reach estimates before relying on them.
- Fees stack: platform fee, data, verification — model the real CPM before promising results.

## Verify
- [ ] Each line has a clear role, budget and enough expected volume to learn.
- [ ] Every deal ID shows bids and wins within 48 hours.
- [ ] Frequency caps, geo and device targeting set and confirmed in reports.
- [ ] Pre-bid brand-safety, IVT and viewability filters active; placement report reviewed.
- [ ] All-in CPM (media + fees + data) calculated and within plan.
