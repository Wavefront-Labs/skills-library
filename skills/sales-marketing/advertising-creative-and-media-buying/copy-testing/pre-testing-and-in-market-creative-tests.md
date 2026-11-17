---
id: sales-marketing.advertising-creative-and-media-buying.copy-testing.pre-testing-and-in-market-creative-tests
name: pre-testing-and-in-market-creative-tests
category: sales-marketing
field: advertising-creative-and-media-buying
product: copy-testing
tags: [copy-testing, ad-testing, pre-testing, creative-testing, ab-testing, split-testing, brand-lift, ad-recall, persuasion, purchase-intent, attention, branding-cue, kill-or-scale, statistical-significance, sample-size, holdout, control-group, conversion-lift, meta-experiments, google-ads-experiments, system1, kantar-link, ipsos]
level: practitioner
status: draft
description: "Test ads before and during spend: choose pre-test metrics, design fair A/B creative tests, size samples, read lift and recall results, and make kill-or-scale calls without fooling yourself."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Copy testing — pre-flight tests and in-market creative experiments

**Goal:** stop weak ads before they eat the budget, and move money to the strongest
execution quickly, using tests whose results you can actually trust.

## 1. Decide what you are testing for
Pick 2–3 primary metrics tied to the brief's objective before seeing any results:
- **Branding / attribution:** do viewers correctly name the brand? (Weak branding is the
  most common fixable failure.)
- **Attention / recall:** do they notice and remember it?
- **Message take-out:** can they play back the single-minded proposition?
- **Persuasion / intent:** change in purchase intent or preference vs a control.
- **Response:** click-through, conversion, cost per acquisition (in-market only).
Write the decision rule in advance, e.g. "Kill any execution scoring in the bottom
third on branding; scale the winner if CPA is ≥15% better at 95% confidence."

## 2. Pre-flight (before media spend)
Options, cheapest first:
1. **Internal check** against the brief (free, biased — use as a filter, not proof).
2. **Online survey pre-test** via a panel or a commercial service (System1, Kantar
   LINK, Ipsos and similar; methods and norms differ — compare only within one
   provider's norms). Show the ad in a clutter reel, then ask recall, branding,
   take-out, intent. Typical cells: 150–300 respondents per execution (check the
   vendor's guidance).
3. **Animatic or rough-cut tests** to catch problems before full production.
Use open-ended "what was the ad trying to tell you?" answers — they diagnose *why*.

## 3. In-market A/B tests
- **Platform experiments:** Meta (A/B test in Ads Manager, Conversion Lift studies),
  Google Ads (Experiments; Brand Lift for YouTube), DSP split tests. These randomise
  audiences so cells don't overlap.
- **Rules for a fair test:**
  - Change one variable (headline, opening 3 seconds, offer, visual) per test.
  - Equal budgets and identical targeting, placements and schedule across cells.
  - Run at least one full weekly cycle; don't stop early on a promising day.
  - Pre-calculate sample size: to detect a relative 10% lift on a 2% conversion rate
    at 95% confidence / 80% power you need tens of thousands of visitors per cell
    (use an online sample-size calculator; small differences need large samples).
- **Geo or holdout tests** for channels without user-level randomisation (TV, OOH):
  run in matched test regions, hold out control regions, compare sales.

## 4. Read the result and decide
1. Check the test ran as designed (spend split, delivery, no mid-test edits).
2. Look at the confidence interval, not just the point estimate. Overlapping
   intervals = no proven winner.
3. Act per the pre-written rule: kill, iterate (fix the diagnosed weakness, re-test)
   or scale. Scaling: increase budget gradually (e.g. 20–30% steps) to see if results
   hold as reach widens.
4. Log the learning in a test library: hypothesis, variant, metric, result, decision.

## Gotchas
- Peeking and stopping when "significant" inflates false winners; fix duration first.
- Platform delivery algorithms can favour one creative within an ad set — that is
  optimisation, not a controlled test. Use the formal experiment tool.
- Pre-test norms are vendor-specific; a "good score" doesn't transfer across providers.
- Survey intent overstates real purchase; use it to rank ads, not forecast sales.
- Winners decay (creative fatigue); retest periodically.

## Verify
- [ ] Metrics and kill/scale rule written before results were seen.
- [ ] One variable changed; cells had equal budget and targeting.
- [ ] Sample size or duration fixed in advance and met.
- [ ] Decision based on confidence interval, not point estimate.
- [ ] Learning logged in the test library.
