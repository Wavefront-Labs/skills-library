---
id: sales-marketing.digital-marketing.marketing-analytics-attribution.tracking-plan-attribution-and-ltv-reporting
name: tracking-plan-attribution-and-ltv-reporting
category: sales-marketing
field: digital-marketing
product: marketing-analytics-attribution
tags: [marketing-analytics-attribution, marketing-analytics, attribution, multi-touch-attribution, last-click, data-driven-attribution, mmm, marketing-mix-modelling, incrementality, geo-lift, holdout-test, tracking-plan, utm-parameters, ga4, google-tag-manager, gtm, server-side-tagging, consent-mode, cohort-analysis, ltv, clv, cac, payback-period, roas, mer, blended-roas, looker-studio, dashboards]
level: advanced
status: draft
description: "Know what marketing worked: a tracking and UTM plan, GA4/GTM event setup, attribution that triangulates platform data with incrementality tests and MMM, cohort LTV:CAC, and budget-changing reports."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Marketing analytics and attribution

**Goal:** measurement good enough to move budget confidently — consistent tracking,
an honest view of each channel's contribution, and unit economics (CAC, LTV, payback).

## 1. Tracking plan (before tools)
A spreadsheet listing every **event** that matters: name, trigger, parameters, where it
fires, owner. E.g. `view_item`, `add_to_cart`, `begin_checkout`, `purchase` (with
`value`, `currency`, `transaction_id`), `generate_lead`. Use GA4 recommended event
names where they fit so built-in reports work.

**UTM convention** (write it down, enforce it):
- `utm_source` = the site/platform (`google`, `meta`, `newsletter`)
- `utm_medium` = channel type (`cpc`, `paid_social`, `email`, `affiliate`)
- `utm_campaign` = campaign name in a fixed pattern (`2026q4_blackfriday_prospecting`)
- lowercase only; a shared UTM builder sheet prevents `Facebook` vs `facebook` splits.

## 2. Implement and validate
- Deploy via **Google Tag Manager** (or the platform's equivalent); push ecommerce data
  to the dataLayer from the site.
- Platform conversion APIs (Meta CAPI, Google enhanced conversions) or **server-side
  tagging** improve match rates as browser tracking degrades.
- **Consent:** apply consent mode / CMP rules required in your markets (e.g. Google
  Consent Mode v2 for EEA traffic). Expect modelled, not exact, conversions.
- Validate: GTM preview, GA4 DebugView, then reconcile GA4 purchases with backend
  orders weekly. A gap beyond roughly 5–15% needs investigating (some gap is normal from
  consent and blockers).

## 3. Attribution: triangulate three views
1. **Platform-reported** (Google Ads, Meta): useful for in-platform optimisation; each
   platform claims credit, so totals exceed actual sales.
2. **Analytics attribution** (GA4 data-driven or last-click): one de-duplicated view,
   but only of trackable digital touchpoints.
3. **Incrementality:** what sales would have happened anyway?
   - **Holdout / conversion-lift tests** inside platforms.
   - **Geo-lift tests:** turn a channel off/on in matched regions, compare sales.
   - **Marketing mix modelling (MMM):** regression on 2+ years of weekly spend and sales
     including offline channels, seasonality and price (open-source options include
     Meta's Robyn and Google's Meridian).
Use tests to calibrate the other two: if a geo test shows a channel drives half the
sales its platform claims, discount that platform's ROAS by about half when allocating.

## 4. Unit economics
- **CAC** = acquisition spend ÷ new customers (blended and by channel).
- **Cohort LTV:** group customers by first-purchase month and channel; track cumulative
  gross margin per customer at 30/90/180/365 days.
- **LTV:CAC** and **payback period** (months until cumulative margin covers CAC).
  A frequently cited heuristic is LTV:CAC ≥ 3 — treat as a sanity check, not a rule.
- **MER / blended ROAS** = total revenue ÷ total marketing spend — the check that
  channel-level stories add up.

## 5. Reporting that changes decisions
Weekly dashboard (Looker Studio or BI tool): spend, revenue, MER, CAC, conversion rate by
channel, vs target and last period. Monthly: cohort LTV, test results, recommended budget
shifts. Every report ends with "so we will…".

## Gotchas
- Retargeting and brand search look superb in last-click and often have low incrementality.
- Changing UTM or event names mid-year breaks comparisons; version the tracking plan.
- MMM needs enough spend variation; flat budgets yield unreliable estimates.
- Attribution models and privacy rules change; revalidate after major platform updates.

## Verify
- [ ] Tracking plan and UTM convention documented and in use.
- [ ] GA4 purchases reconcile to backend orders within an agreed tolerance.
- [ ] At least one incrementality test run for the largest channel.
- [ ] Cohort LTV and CAC by channel calculated with payback period.
- [ ] Weekly report includes MER and a budget recommendation.
