---
id: sales-marketing.digital-marketing.google-ads.search-pmax-shopping-structure-and-bidding
name: search-pmax-shopping-structure-and-bidding
category: sales-marketing
field: digital-marketing
product: google-ads
tags: [google-ads, adwords, ppc, paid-search, sem, search-campaigns, keywords, match-types, broad-match, phrase-match, exact-match, negative-keywords, search-terms-report, responsive-search-ads, rsa, performance-max, pmax, shopping-campaigns, merchant-center, product-feed, smart-bidding, target-cpa, target-roas, maximize-conversions, quality-score, ad-strength, conversion-tracking, enhanced-conversions, experiments]
level: practitioner
status: draft
description: "Run Google Ads: conversion tracking first, campaign structure, match types and negatives, responsive search ads, Performance Max and Shopping feeds, Smart Bidding, Quality Score."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Google Ads — structure, keywords, PMax/Shopping, bidding

**Goal:** paid search and Google's other surfaces bringing profitable conversions,
with the algorithm fed accurate data and enough control to stop waste.

Google changes features, names and defaults often (e.g. match-type behaviour,
PMax controls). Check the current Google Ads Help Center for anything below that
looks different in your account.

## 1. Conversion tracking first
- Define primary conversions (purchase with value, qualified lead); set secondary ones
  (add to cart, page views) to **secondary** so bidding doesn't optimise to them.
- Implement via the Google tag/GTM or GA4 import; turn on **enhanced conversions**.
- Lead gen: import offline conversions (qualified/closed deals) from the CRM so bidding
  optimises to real sales, not form spam.
- Verify with Tag Assistant and a test conversion.

## 2. Structure
- Campaigns split by **budget and goal** (brand vs non-brand search, Shopping/PMax,
  geography if budgets differ). Ad groups by tight theme (one product/service intent).
- Fewer, larger campaigns give Smart Bidding more data; over-segmenting starves it.
- Brand campaigns separate so they don't flatter non-brand performance.

## 3. Keywords and match types
- **Exact** `[blue running shoes]`: closest control. **Phrase** `"blue running shoes"`:
  query must include the meaning. **Broad**: widest; works best with Smart Bidding and
  good conversion data.
- **Search terms report** weekly: add converting queries as keywords; add irrelevant
  ones as **negative keywords** (shared negative lists for jobs, free, DIY, competitors
  if desired).
- Start new accounts with exact/phrase on proven high-intent terms; expand to broad
  once conversions flow.

## 4. Ads
**Responsive search ads**: up to 15 headlines and 4 descriptions. Include the keyword
theme, benefits, proof (reviews, numbers), offer and a call to action; pin only when
legally required (pinning reduces combinations). Add assets: sitelinks, callouts,
structured snippets, images, call, location. "Ad strength" is a guide to variety, not
a performance metric.

## 5. Shopping and Performance Max
- **Merchant Center** product feed quality decides Shopping results: accurate titles
  (brand + product type + key attributes), GTINs, high-quality images, correct
  price/availability, product categories. Fix disapprovals in the Diagnostics tab.
- **Performance Max** runs across Search, Shopping, YouTube, Display, Gmail, Maps from
  one campaign using asset groups (text, images, video) and audience signals.
  Give it accurate conversion values, brand exclusions if you want brand traffic kept in
  brand Search, and listing-group segmentation (e.g. by margin tier).
- Watch PMax search-term and placement insights available in the account; controls have
  been expanding over time.

## 6. Bidding
- Start with **Maximize conversions** (or conversion value) to gather data; move to
  **Target CPA / Target ROAS** once a campaign has steady conversions (Google's own
  guidance changes; dozens per month is a reasonable floor).
- Set targets near current actuals, then tighten in ~10–20% steps; each change restarts
  a learning period of roughly a week or two.
- Use **Experiments** to test bid strategies and landing pages with a split.

## 7. Quality Score
1–10 keyword diagnostic from expected CTR, ad relevance and landing-page experience.
Improve via tighter ad groups, keyword-aligned headlines, fast relevant landing pages.
Higher quality lowers cost per click for the same position.

## Gotchas
- Default settings on new campaigns may include Display Network expansion or broad
  location options ("presence or interest") — review every setting.
- Auto-applied recommendations can change budgets/keywords; review or switch off.
- Judging new campaigns in the learning period leads to thrashing.
- Last-click credit flatters brand search; see the attribution skill
  `sales-marketing.digital-marketing.marketing-analytics-attribution.tracking-plan-attribution-and-ltv-reporting`.

## Verify
- [ ] Primary conversions are real business outcomes, with values; test conversion recorded.
- [ ] Brand and non-brand separated; campaigns not over-segmented.
- [ ] Search terms reviewed weekly; negative lists applied.
- [ ] Merchant Center feed free of disapprovals; PMax has brand exclusions decision made.
- [ ] Bid targets changed in small steps with learning periods respected.
