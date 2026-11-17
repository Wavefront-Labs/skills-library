---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.consumer-service-risk-tolerance
name: consumer-service-risk-tolerance
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [consumer-risk-tolerance, product-risk-assessment, embracing-risk, availability-target, product-management, sre]
level: practitioner
status: docs-checked
description: "Work with product owners to set a consumer service's risk tolerance: target availability, failure types, cost, and other service metrics, as a structured interview."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifying consumer-service risk tolerance

Risk tolerance for a consumer product is a product decision, not an engineering one. SRE's job is to make
the trade-off explicit. The SRE Book lists the factors; run them as an interview with the product owner.

## Interview script
1. **Target availability**
   - What level of service do users expect? (Compare with competitors and the user's own network.)
   - Is the service directly tied to revenue (ads, checkout) or indirect?
   - Paid or free? Is there an SLA with credits?
   - If there are competitors, what level of service do they provide?
   - Consumer or enterprise audience? (The book notes an enterprise outage is an outage for every customer that depends on you.)
2. **Types of failure**
   - Which is worse: constant low error rate or occasional full outage?
   - Which failures are catastrophic (data exposure, wrong balances) vs annoying (stale avatar)?
   - Are there quiet periods where planned downtime is acceptable?
3. **Cost**
   - Revenue per minute at risk at peak and off-peak.
   - What would one more nine cost, and would the extra revenue offset it? (See `cost-of-each-extra-nine`.)
4. **Other service metrics**
   - Latency expectations per surface (the book contrasts AdWords, where ads must not slow search, with AdSense).
   - Other metrics that give degrees of freedom for thoughtful risk-taking.

## Output: a risk statement
```
Service: photo-sharing web frontend
Target: 99.9% request success over the agreed window; page-load latency target
Worst failure: serving another user's private photo (correctness: zero tolerance, separate control)
Acceptable: a stated amount of degraded thumbnails
Not acceptable: checkout failures; separate, stricter SLO on /checkout
Owner sign-off: <product owner>, <date>
```

## Checked

2026-11-01. Confirmed against the SRE Book chapter Embracing Risk, section Identifying the Risk Tolerance of
Consumer Services (the four factor groups and their questions, the full-versus-partial outage examples, planned
downtime for Ads Frontend, the AdWords and AdSense latency contrast). Removed: the 28d, 800 ms, 4 h/quarter and
99.95% figures in the example (illustrative, not from the book).
Method: documentation only; no commands were run.

## Gotchas
- Product owners often ask for "100%"; answer with the downtime table and cost, not a refusal.
- Different user journeys deserve different targets; one service-wide number hides this.
- Failure *type* matters more than rate for correctness/privacy; do not express those as an error budget.
- Revisit when the business model changes (free to paid, new enterprise tier).

## Verify
- [ ] Written risk statement per critical user journey, signed by the product owner.
- [ ] Targets traceable to SLOs and error budget policy.
