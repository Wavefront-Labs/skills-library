---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.business-value-decisions
name: business-value-decisions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-principles, business-value-decisions, value-based-decisions, cost-vs-value, iron-triangle, trade-off-analysis]
level: practitioner
status: docs-checked
description: "Make cloud decisions on business value, not lowest cost: trade off cost, quality and speed, use unit economics, and read rising spend against value."
sources: ["https://www.finops.org/framework/principles/", "https://www.finops.org/framework/domains/quantify-business-value/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Business-value decisions over cost cutting

FinOps Principle: "Business value drives technology decisions." The Framework says unit economic
and value-based metrics show business impact better than aggregate or categorised spend, and
that teams should make conscious trade-off decisions among cost, quality and speed.

## Steps
1. **State the value metric** for the workload and pair it with cost as a unit metric (see
   `unit-metric-selection`). The Quantify Business Value domain asks for metrics based on
   objective measurements that reveal business value.
2. **Say which of cost, quality and speed the business is prioritising** for this workload now,
   and record the trade-off you accepted.
3. **Consider cost and value in monetary terms, in sustainability terms, and in traditional
   performance terms** such as availability, reliability or customer satisfaction, as the domain
   page recommends.
4. **Put the options side by side** in a short decision record: option, cost, value effect, risk,
   and "do nothing". The record format is a suggestion, not from the Framework.
5. **Revisit** the decision later to check that the expected value appeared.

## Questions the domain answers
- What value do we expect to achieve from our technology use?
- How will we measure that value?
- Does what we use and spend allow us to meet our strategic and organisational objectives?
- Is what we use and spend commensurate with other comparable examples?

## Verify
- [ ] Significant spend changes have a decision record with cost and value together.
- [ ] Reports show a unit metric next to total cost so growth is not misread as waste.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Principles page and the Quantify Business Value domain page (both read in full). The AWS Well-Architected cost pillar source was not readable and was dropped. Removed unconfirmed: the "iron triangle" name, the worked dollar examples, the 90-day revisit date and the claim that engineer time must be costed.
