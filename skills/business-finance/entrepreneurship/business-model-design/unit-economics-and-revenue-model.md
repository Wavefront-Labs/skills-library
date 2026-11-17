---
id: business-finance.entrepreneurship.business-model-design.unit-economics-and-revenue-model
name: unit-economics-and-revenue-model
category: business-finance
field: entrepreneurship
product: business-model-design
tags: [business-model-design, entrepreneurship, unit-economics, revenue-model, business-model-canvas, cac, customer-acquisition-cost, ltv, clv, lifetime-value, ltv-cac-ratio, payback-period, contribution-margin, gross-margin, churn, retention, cohort-analysis, pricing, subscription, saas, marketplace, take-rate, value-proposition]
level: practitioner
status: draft
description: "Choose a revenue model and prove it works per customer: contribution margin, CAC, LTV, payback and churn by cohort, with the common ways founders flatter their own numbers."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unit economics and revenue model — does each customer make you money?

**Goal:** decide how the venture captures value, then show — with honest numbers — that
one more customer adds profit rather than loss. Scale multiplies unit economics; it
does not fix them.

## 1. Sketch the model on one page
Use a business model canvas or a plain list, but answer these explicitly:
- **Customer segment** — one specific buyer, not "SMEs".
- **Value proposition** — the job they hire you for and what they use today instead.
- **Channel** — how they find and buy (self-serve, sales team, partner, marketplace).
- **Revenue model** — who pays, for what, how often (below).
- **Cost structure** — what scales with each sale versus what is fixed.

## 2. Pick the revenue model that fits the value
| Model | Fits when | Watch |
|---|---|---|
| One-off sale | Durable product, clear moment of purchase | Constant re-acquisition cost |
| Subscription | Ongoing value, used repeatedly | Churn is the whole game |
| Usage / metered | Value scales with consumption | Unpredictable revenue, bill shock |
| Transaction / take rate | Marketplace or payments | Disintermediation; take rate is limited by value added |
| Freemium | Low marginal cost, viral or self-serve | Free-to-paid conversion is often only a few percent |
| Licensing / services | Enterprise, IP-heavy | Services revenue scales with headcount |

Price on the customer's value and alternatives, not on your cost plus a margin.

## 3. Compute the unit economics
Define "unit" first (a customer, an order, a seat). Then:
- **Contribution margin per unit** = revenue − variable costs (COGS, payment fees,
  hosting per user, delivery, support that scales with customers). Gross margin alone
  can hide fulfilment and support costs.
- **CAC** (customer acquisition cost) = total sales + marketing spend in a period ÷ new
  customers acquired in that period. Include salaries, tools and agency fees — not just ad spend.
- **Churn** = share of customers (or revenue) lost per period. Monthly churn of 3% is
  roughly 31% lost per year (1 − 0.97¹²), not 36%.
- **LTV** (simple) = monthly contribution margin per customer ÷ monthly churn rate.
- **CAC payback** (months) = CAC ÷ monthly contribution margin per customer.

Worked example: €50/month plan, €10 variable cost → €40 contribution; 2.5% monthly churn
→ LTV ≈ €40 ÷ 0.025 = €1,600; CAC €600 → LTV:CAC ≈ 2.7, payback 15 months.

Rules of thumb often quoted for SaaS: LTV:CAC ≥ 3 and payback under ~12–18 months.
These are heuristics from venture-backed software, not laws — capital-light or
high-retention businesses can live with different numbers.

## 4. Look at cohorts, not blended averages
Group customers by the month they joined and track retention and revenue for each
cohort. A blended churn rate improves just because you added lots of new customers;
cohort curves show whether retention actually flattens (good) or keeps falling to zero.
For subscriptions, also track **net revenue retention** — expansion revenue can offset churn.

## Gotchas (how founders flatter themselves)
- **Blended CAC** that counts organic/word-of-mouth customers hides the true cost of
  paid channels. Report paid CAC by channel separately.
- **LTV from too little data** — a 6-month-old company extrapolating a 5-year lifetime.
  Cap the assumed lifetime (e.g. 3 years) until you have the data.
- **Revenue-based LTV** instead of contribution-based: overstates value by the variable cost.
- **Discounts and free months** left out of revenue per customer.
- **Founder-led sales** — early CAC looks tiny because the founder's time is free. It
  won't be when you hire a sales team.
- CAC rises as you exhaust the cheapest channel; model it rising, not flat.

## Verify
- [ ] One named customer segment and one stated revenue model.
- [ ] Contribution margin per unit includes every cost that scales with sales.
- [ ] CAC includes salaries and tools, split by channel.
- [ ] LTV uses contribution margin and a capped lifetime; payback stated in months.
- [ ] A cohort retention table exists and its curve shape is described.
- [ ] You can name the one number that most needs to improve, and the experiment to move it.

Related: business-finance.entrepreneurship.lean-validation (testing the assumptions behind these numbers).
