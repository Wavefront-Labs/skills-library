---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.risk-tolerance-factors-and-revenue-impact
name: risk-tolerance-factors-and-revenue-impact
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, embracing-risk, risk-tolerance-factors, revenue-impact-analysis, availability-target, slo]
level: advanced
status: docs-checked
description: "Set a service's availability target from risk tolerance factors: user expectations, revenue impact per minute, paid vs free tiers, competitors and cost of the next nine."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/workbook/implementing-slos/", "https://sre.google/sre-book/service-level-objectives/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Risk tolerance factors and revenue impact

**Goal:** pick an availability target with a business argument, not "as high as possible".

## Factors (SRE Book, consumer services)
1. **Level of availability users expect**, shaped by the function the service provides and its place in the market.
2. **Different failure types**: a constant low error rate vs an occasional full outage can cost the business very differently, and a partial failure that exposes private data is worse than one that drops profile pictures.
3. **Cost of an extra nine**: what incremental revenue would one more nine bring, and does it offset the cost of reaching it?
4. **Revenue impact**: does the service tie directly to revenue, yours or your customers'?
5. **Paid vs free**, and consumer vs enterprise; contracts can carry penalties.
6. **Competitive landscape**: what level of service do competitors provide?

Also check that critical dependencies can support the target (a design judgement, not from the Book's list).

## Revenue impact worksheet
```
revenue per minute at peak       = R  (for example 1,000 USD/min)
fraction of revenue lost per minute of outage (retry/abandon)  = f (for example 0.6)
minutes of downtime allowed per 30 days at target T = 43,200 x (1 - T)
expected outage cost per month   = R x f x 43,200 x (1 - T)
```
| Target | Downtime / 30 d | Cost (R=1000, f=0.6) |
|---|---|---|
| 99% | 432 min | 259,200 |
| 99.9% | 43.2 min | 25,920 |
| 99.95% | 21.6 min | 12,960 |
| 99.99% | 4.3 min | 2,592 |
Moving from 99.9% to 99.99% saves about 23k/month here; if it costs more than that in engineering and infrastructure, it is not worth it for revenue alone.

## Process
1. Gather the factor answers with product, finance and support.
2. Measure current reliability (last 90 days) as a reality check.
3. Propose target + window; document rationale and what is out of scope (planned maintenance? dependencies?).
4. Revisit yearly or when business model changes.

## Verify
- [ ] SLO document includes the factor analysis and cost table, signed off by product.

## Checked
2026-11-01. Confirmed in SRE Book Embracing Risk: the target-availability questions (user expectation, revenue link, paid vs free, competitors, consumer vs enterprise), types of failures, and the incremental-nine cost test. The worksheet arithmetic was recomputed and is illustrative (the revenue and loss-fraction inputs are examples). Removed the claim that users tolerate slow pages better than lost orders, and the SRE Book attribution for the dependency factor.
Method: documentation only; no commands were run.
