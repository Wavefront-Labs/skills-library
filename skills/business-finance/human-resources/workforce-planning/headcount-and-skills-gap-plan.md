---
id: business-finance.human-resources.workforce-planning.headcount-and-skills-gap-plan
name: headcount-and-skills-gap-plan
category: business-finance
field: human-resources
product: workforce-planning
tags: [workforce-planning, strategic-workforce-planning, swp, headcount-planning, headcount-forecast, skills-gap-analysis, supply-and-demand, attrition, turnover, internal-mobility, build-buy-borrow, succession-planning, critical-roles, span-of-control, org-design, workforce-analytics, fte, time-to-fill, people-analytics, hr-planning]
level: practitioner
status: draft
description: "Build a 1-3 year workforce plan: demand from business drivers, supply after attrition and moves, the gap by role and skill, build/buy/borrow actions, succession for critical roles."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Headcount and skills-gap plan

**Goal:** know how many people, with which skills, the organisation will need in each
of the next 1–3 years; how many it will still have; and the specific actions that
close the gap — tied to the budget so finance and HR are working from one number.

## 1. Baseline (current supply)
From the HRIS, as of one date: headcount and **FTE** by function, location, job
family, level, employment type (permanent, fixed-term, contractor); age/tenure profile;
open requisitions; known leavers and retirements; skills/certifications where
recorded. **Reconcile headcount with payroll and the FP&A plan** — three different
numbers is the most common starting position.

## 2. Demand: drive it from the business plan
- Link roles to **workload drivers**: customers per account manager, tickets per
  agent, revenue per salesperson, beds per nurse, projects per engineer.
  `required FTE = forecast driver volume ÷ productivity ratio`.
- Add **strategic changes:** new products, markets, sites, automation that removes
  work, regulation that adds it.
- Use scenarios (base / growth / downturn) rather than one forecast.
- For skills, list the **critical capabilities** the strategy needs (e.g. data
  engineering, a new regulatory specialism), not just job titles.

## 3. Supply projection
```
projected supply(t+1) = current headcount
  − expected leavers (attrition rate by group × headcount)
  − retirements / contract ends
  ± internal moves and promotions
```
Use **attrition by segment** (role, level, tenure band) — first-year attrition is
usually much higher than average, so a company-wide rate misleads.

## 4. Gap analysis
Gap = demand − projected supply, by role family, level, location and year, plus a
**skills gap** (capability needed vs held). Flag:
- **Critical roles** (hard to fill, high business impact) and their bench strength.
- **Concentration risk** — one person holding a key skill.
- Surpluses (roles automation or restructuring will reduce).

## 5. Actions: build, buy, borrow, bot, move
- **Build:** train and develop existing staff (lead time 6–24 months).
- **Buy:** hire — check market availability and **time-to-fill** history.
- **Borrow:** contractors, agencies, partners for peaks or niche skills.
- **Bot/automate:** remove demand.
- **Move:** redeploy from surplus areas; often cheaper and better for retention.
Each action gets an owner, cost, timing, and entries in the recruiting plan and budget.

## 6. Succession for critical roles
For each critical role: ready-now, ready in 1–2 years, ready in 3+ candidates, with
development actions. No ready-now cover → external pipeline or interim plan.

## 7. Run it as a cycle
Refresh quarterly against actual hires, leavers and business changes; full rebuild
annually with the budget.

## Gotchas
- **Headcount vs FTE vs cost** confusion — always label which.
- Planning only for permanent staff while contractors do a large share of work.
- **Span of control** creeping down (too many managers) is a cost and agility issue
  the plan should surface.
- Skills data in HRIS is often sparse or self-reported; treat it as indicative.
- Personal data in analytics needs privacy controls; aggregate small groups.

## Verify
- [ ] Baseline headcount reconciled to payroll and the finance plan.
- [ ] Demand linked to business drivers with scenarios.
- [ ] Supply uses segmented attrition.
- [ ] Gaps by role, level, location and skill, with critical roles flagged.
- [ ] Every gap has a costed build/buy/borrow/automate/move action and owner.
