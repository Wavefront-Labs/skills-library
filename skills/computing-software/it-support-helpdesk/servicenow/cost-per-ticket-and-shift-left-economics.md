---
id: computing-software.it-support-helpdesk.servicenow.cost-per-ticket-and-shift-left-economics
name: cost-per-ticket-and-shift-left-economics
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, metrics, kpi, cost-per-ticket, shift-left, cost-per-contact, service-desk-benchmarking]
level: practitioner
status: draft
description: "Calculate cost per ticket by support level and channel, and use it to justify shift-left: loaded labour cost, volume, level cost ratios, and building a savings case."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.metricnet.com/"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cost-per-ticket-and-shift-left-economics
Goal: know what a ticket costs at each level and channel, so decisions
about knowledge, automation and self-service rest on numbers.

## Cost per ticket (simple, defensible)
cost per ticket = total desk operating cost ÷ tickets handled, per period.
Operating cost includes: salaries + benefits + overhead (loaded labour,
typically 1.3-1.5× salary), tools/licences, telephony, facilities share,
management, training. Do the same per level (L1, L2 desk-side, L3
engineering) and per channel (phone, chat, email, walk-up, portal).

## Typical ratios (industry benchmarks, use your own data)
- Self-service resolution: a fraction of L1 cost.
- L1 contact: baseline (often quoted in the US$15-25 range).
- Desk-side/L2: roughly 3-5× L1.
- L3/engineering or vendor: higher again.
The exact numbers vary; the ratio is what makes shift-left pay.

## Shift-left business case
1. Pick a ticket type resolved at L2 that L1 could do with knowledge or
   permissions (e.g. BitLocker recovery key retrieval, Outlook profile
   rebuild).
2. Volume per month × (L2 cost − L1 cost) = monthly saving.
3. Subtract one-off cost (KB writing, training, RBAC change) and risk.
4. After the change, measure actual L1 FCR for that type and recompute.

## Pitfalls
- Driving cost per ticket down by cutting staff while volume rises hurts
  MTTR and CSAT. Always show cost alongside quality metrics.
- Cost per ticket rises when self-service removes the easy tickets — the
  remaining ones are harder. Track total cost and cost per employee too.
- Include the end user's lost time for a balanced view (minutes waiting ×
  employee cost) when arguing for faster channels.

## Verify
You can show a cost per ticket for each level and channel with sources
for each cost line, and each shift-left initiative has a before/after
saving.
