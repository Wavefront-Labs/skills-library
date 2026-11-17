---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.organic-and-inorganic-demand-planning
name: organic-and-inorganic-demand-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [organic-growth, inorganic-growth, launch-demand, capacity-planning, demand-forecasting, launch-planning]
level: practitioner
status: docs-checked
description: "Separate organic growth (steady adoption) from inorganic demand (launches, marketing, migrations, events) and build both into a capacity plan with dated line items."
sources: ["https://sre.google/sre-book/introduction/", "https://sre.google/sre-book/reliable-product-launches/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organic and inorganic demand planning

The SRE Book's capacity planning steps: an accurate organic demand forecast extending beyond the lead time
for acquiring capacity; an accurate incorporation of inorganic demand sources; regular load testing to
correlate raw capacity to service capacity. This skill covers the first two.

## Organic growth
Natural adoption with no specific event. Model from history:
- Model from history of demand at the *driver* level (requests, storage bytes, users), not CPU.
- Fit a trend (see `demand-forecasting-models`) and project past your procurement lead time. The SRE Book's
  Reliable Product Launches chapter notes datacenter and network resources often have a long lead time and must be
  requested far enough in advance.

## Inorganic demand
Step changes caused by decisions: feature launches, marketing, customer onboarding, migrations, seasonal events.
Collect them from product, marketing and partner teams regularly and ask for dates, expected users, load per user
and regions.

## Building the plan
```
demand(t) = organic_forecast(t) + sum(inorganic_item_i(t))
capacity_needed(t) = demand(t) / per_instance_capacity / target_utilisation + redundancy
```
Track each inorganic item as a row with owner, date, confidence and expected load. The launch chapter's capacity
example: if three replicated deployments serve 100% of peak traffic, keep four or five so maintenance and
unexpected malfunctions do not hurt users.

## Gotchas
- Organic fits trained on data containing past launches over-forecast; subtract known steps first.
- Inorganic demand also *removes* load (decommissions); capture those to free capacity.

## Verify
- [ ] Forecast horizon exceeds procurement lead time.
- [ ] Inorganic register reviewed regularly with product/marketing.
- [ ] Post-launch: actual vs forecast recorded to calibrate the next estimate.

## Checked
2026-11-01. Confirmed against the SRE Book "Introduction" (organic demand forecast extending beyond acquisition lead time; incorporation of inorganic demand) and "Reliable Product Launches at Scale" (long lead time for datacenter and network resources; three deployments needing four or five).
Removed: 12-month history, cloud quota and hardware lead-time figures, the inorganic shape table, confidence tiers, and launch-estimate bias claims; the managing-load source.
Method: documentation only; no commands were run.
