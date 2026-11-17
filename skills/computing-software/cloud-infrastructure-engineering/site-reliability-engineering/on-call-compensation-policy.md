---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-compensation-policy
name: on-call-compensation-policy
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [on-call-compensation-policy, compensation-policy, on-call, time-off-in-lieu, labour-law, sre-management]
level: practitioner
status: docs-checked
description: "Design an on-call compensation policy: time off in lieu vs cash, caps that limit overload, and the local labour-law checks to run with HR."
sources: ["https://sre.google/sre-book/being-on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call compensation policy

SRE Book: adequate compensation needs to be considered for out-of-hours support, and organisations handle it
differently. Google offers time off in lieu or straight cash compensation, capped at some proportion of overall salary.
The cap in practice limits how much on-call work any individual takes on: it keeps the incentive to take on on-call duty,
promotes a balanced distribution and limits burnout and lost project time.

## Elements to decide
| Element | Question |
|---|---|
| Form | Time off in lieu, cash, or both; which is allowed where you employ people |
| Standby | What availability constraints does standby impose (response time, location, sobriety), and does the pay reflect them |
| Active incident time | How out-of-hours incident work is recorded and paid or taken as time off |
| Cap | The maximum on-call load per person (the book ties the cap to a proportion of salary) |
| Holidays | Whether public holidays are treated differently, per region |

Amounts, multipliers and cap sizes are your organisation's decision; the book gives none.

## Legal and HR checks (jurisdiction dependent; involve HR or legal)
- Whether standby counts as working time where you operate.
- Minimum rest periods between shifts.
- Overtime rules for non-exempt employees.
- Contractors: billing terms for standby versus active time.
Check the governing national or regional labour authority for the rules that apply to you.

## Gotchas
- Pay per page creates a reason to keep noisy alerts; consider pay per shift plus incident time.
- Unpaid "best-effort" on-call is still on-call; formalise it or remove it.
- A compensation cap that is hit regularly is a signal of overload, not a budget line to raise.

## Verify
- [ ] Policy reviewed by HR or legal per country.
- [ ] Incident hours exported from the paging tool and reconciled with payments or time off.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Being On-Call", section "Compensation" (time off in lieu or cash,
capped proportion of salary, cap as a limit on on-call work). Removed: rate multipliers, example cap and rest figures,
the policy template with response-time and TOIL deadlines, and the specific statutes and rulings cited (not on the page).
Method: documentation only; no commands were run.
