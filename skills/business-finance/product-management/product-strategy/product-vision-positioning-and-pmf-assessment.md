---
id: business-finance.product-management.product-strategy.product-vision-positioning-and-pmf-assessment
name: product-vision-positioning-and-pmf-assessment
category: business-finance
field: product-management
product: product-strategy
tags: [product-management, product-strategy, product-vision, positioning, product-market-fit, pmf, sean-ellis-test, retention-curve, target-customer, ideal-customer-profile, icp, value-proposition, strategic-bets, build-vs-buy, pricing-input, competitive-alternatives, april-dunford, strategy-doc, product-manager]
level: practitioner
status: draft
description: "Write a one-page product strategy: vision, target customer, positioning against real alternatives, a product-market-fit read from retention and the Sean Ellis survey, and 2-4 explicit bets."
sources: ["April Dunford, Obviously Awesome (2019) - positioning method", "Sean Ellis 40% 'very disappointed' survey benchmark"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Product vision, positioning and product-market-fit assessment

**Goal:** a short strategy that lets the team say no to most ideas without asking you,
because the target customer, the problem and the bets are explicit.

## 1. The one-page strategy (fill every line)
1. **Vision** (3-5 years): the change in the customer's world, not a feature list.
2. **Target customer**: a specific segment you can find and count ("finance teams of
   50-500-person SaaS companies running month-end in spreadsheets"), not "SMBs".
3. **Problem** they pay to solve, in their words (from discovery interviews).
4. **Positioning** (below).
5. **Where we are on PMF** (below), with data.
6. **Strategic bets** for the next 2-4 quarters: 2-4 of them, each with the
   hypothesis, the metric that would prove it, and what you are *not* doing.
7. **Business constraints**: revenue target, pricing model, build-vs-buy decisions.

## 2. Positioning, in a fixed order
Adapted from April Dunford's method:
1. **Competitive alternatives**: what customers would do if you didn't exist. Often
   a spreadsheet, an intern, or doing nothing, not a named competitor.
2. **Unique attributes** you have that those alternatives don't.
3. **Value** those attributes deliver (provable, ideally quantified).
4. **Best-fit customers** who care most about that value.
5. **Market category** that makes the value obvious (existing category, subcategory
   or, rarely and expensively, a new one).
Test: can sales and marketing repeat it in one sentence, and do best-fit customers nod?

## 3. Assessing product-market fit (use several signals)
- **Retention curve**: plot % of each signup cohort still active by week/month. PMF
  shows as the curve **flattening** to a non-zero plateau; a curve heading to zero means
  no fit, regardless of signups.
- **Sean Ellis survey**: ask active users "How would you feel if you could no longer use
  this product?" If roughly 40%+ answer "very disappointed", that's the commonly cited
  PMF threshold. Survey only users who've experienced the core value (e.g. used it
  2+ times in the last two weeks); small samples (<40-50 responses) are noisy.
- **Pull signals**: organic referrals, sales cycles shortening, customers complaining
  loudly when it breaks, expansion revenue.
- **Segment it**: PMF is usually strong in one segment and absent in others. That
  segment becomes the target customer.

## 4. Pricing input from the product seat
PM rarely sets price alone, but owns: which value metric scales with customer value
(seats, usage, transactions), what goes in which tier, and willingness-to-pay
evidence from interviews (e.g. Van Westendorp questions). Hand finance and sales data,
not opinions.

## 5. Build vs buy vs partner (product level)
Build only what is part of your differentiation (the unique attributes in §2). Buy or
integrate commodity capability (auth, billing, notifications). Count total cost: the
maintenance tail of a built feature typically outlasts the build.

## Gotchas
- A vision that is a list of features is a roadmap in disguise.
- "Everyone" as target customer means no positioning.
- Survey-only PMF claims with flat-to-zero retention are wishful thinking.
- Bets without kill criteria never get killed.

## Verify
- [ ] Strategy fits one page; every section has content.
- [ ] Target segment is specific enough to build a list of 50 real prospects.
- [ ] Positioning starts from competitive alternatives, including "do nothing".
- [ ] Cohort retention chart attached; PMF claim cites at least two signals.
- [ ] Each bet has a metric, a check-in date and what you're explicitly not doing.
