---
id: sales-marketing.sales-management.territory-and-quota-design.carving-territories-and-setting-quotas
name: carving-territories-and-setting-quotas
category: sales-marketing
field: sales-management
product: territory-and-quota-design
tags: [territory-and-quota-design, territory-planning, territory-design, quota-setting, quota, capacity-planning, account-assignment, tam, total-addressable-market, whitespace, ramp, quota-relief, rebalancing, attainment, sales-capacity, sales-management, revops, sales-ops, sales-compensation, named-accounts, geographic-territories]
level: practitioner
status: draft
description: "Carve fair sales territories by account potential and workload, set quotas from top-down target and bottom-up capacity, handle ramp and relief, and rebalance mid-year cleanly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Carving territories and setting quotas

**Goal:** every rep has a patch with roughly equal opportunity and a quota most good reps
can hit — so attainment reflects skill, not luck of the draw.

## 1. Build the account universe
In a spreadsheet or your CRM export, one row per target account with:
- Segment (size by employees/revenue), industry, region, current customer or prospect.
- **Potential**: estimated annual spend on your category (or a proxy score), current
  revenue if a customer.
- **Workload**: expected touches per year (customers need more than cold prospects).

## 2. Size capacity first
```
productive_reps   = ramped reps + Σ(ramping rep × ramp %)
rep_capacity      = realistic accounts or opportunities one rep can work
                    (e.g. 40–80 named enterprise accounts, hundreds in SMB — calibrate)
```
If the account universe needs more capacity than you have, either add headcount or
deliberately leave low-potential accounts to a pooled/inside team.

## 3. Carve
Choose the cut that matches how you sell: geography (field sales), named accounts
(enterprise), industry vertical, or segment. Then balance:
- **Potential** per territory within ~±10–15% of the average (a common target; pick yours).
- **Workload** within a similar band.
- Keep existing rep-account relationships where you can — breaking them costs deals.
- Use a simple greedy method: sort accounts by potential descending, assign each to the
  territory with the lowest running total (respecting geography), then hand-adjust.

## 4. Set quotas
- **Top-down:** company target → allocate by territory potential share.
- **Bottom-up:** each territory's pipeline + historical run rate + growth in the base.
- Reconcile the two. Where top-down exceeds bottom-up by a lot, the target needs more
  capacity, not a bigger number on the same reps.
- Sum of quotas is usually set **above** the company target (over-assignment, often
  10–20%) because not every rep hits — check your finance team's convention.
- **Ramp quotas** for new hires: e.g. 0–25–50–75–100% across early months/quarters; set from
  your actual time-to-productivity.
- Sanity check: historically, what % of reps hit quota? Healthy plans often see a majority
  attaining; if only a small minority hit, quotas are probably wrong, not the reps.

## 5. Relief and rebalancing
- Define rules up front: quota relief when a big account is moved, a rep leaves and
  accounts are redistributed, or a territory loses a major customer for reasons outside
  the rep's control.
- Rebalance at most once mid-year, at a period boundary, with written notice.
- Credit rules for deals in flight when accounts move (often: the original rep keeps credit
  for deals past a defined stage).

## 6. Communicate
Give each rep a territory pack: account list, potential, quota with math, ramp, relief
rules. Explaining the method is what makes reps accept the number.

## Gotchas
- Territories carved on last year's revenue reward incumbency, not opportunity.
- Over-assigned quotas compound with top-heavy accelerators into payout surprises —
  model compensation cost alongside quota.
- Pipeline-based quotas punish reps for building pipeline; blend with potential.
- The ranges above are typical rules of thumb, not benchmarks; calibrate on your history.

## Verify
- [ ] Every target account assigned to exactly one owner.
- [ ] Potential and workload per territory within your tolerance band.
- [ ] Quotas reconcile top-down and bottom-up; over-assignment explicit.
- [ ] Ramp, relief and credit rules written before the year starts.
- [ ] After the first quarter: attainment spread reviewed against territory potential.
