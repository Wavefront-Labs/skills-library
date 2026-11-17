---
id: engineering-technology.industrial-manufacturing-systems-engineering.lean-six-sigma.value-stream-mapping-and-flow-design
name: value-stream-mapping-and-flow-design
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: lean-six-sigma
tags: [value-stream-mapping, vsm, lean, lean-manufacturing, toyota-production-system, tps, takt-time, lead-time, process-cycle-efficiency, pce, future-state, current-state, continuous-flow, pull-system, kanban, supermarket, fifo-lane, pacemaker, heijunka, pitch, epei, cell-design, one-piece-flow, waste, muda, lean-six-sigma, kaizen]
level: practitioner
status: draft
description: "Map a current-state value stream, compute takt, lead time and PCE, then design a future state with flow cells, pacemaker, supermarkets and kanban sizing."
sources:
  - "Rother & Shook, Learning to See (Lean Enterprise Institute)"
  - "Rother & Harris, Creating Continuous Flow"
  - "Smalley, Creating Level Pull"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Value-stream mapping and flow design

**Goal:** see where a product family's lead time actually goes, then design a future
state that flows where it can, pulls where it must, and is scheduled at one point.

## 1. Pick one product family
Group products that share most downstream steps (a product-process matrix: products
as rows, steps as columns, cluster rows with ~80% common steps). One map per family.
Mapping "the whole plant" produces a wall poster and no decisions.

## 2. Walk and draw the current state (pencil, on the floor)
Start at shipping and walk upstream. For each process box record: cycle time (C/T),
changeover time (C/O), uptime, operators, shifts, scrap %, batch size. Between boxes
record **inventory counted on the floor** (not from the ERP) and how material moves
(push, FIFO, supermarket). Draw information flow: how each step learns what to make.

Convert each inventory triangle to days: **days of inventory = units ÷ daily demand**.

## 3. Calculate the headline numbers
- **Takt = net available time ÷ customer demand.** Example: 2 shifts × 7.5 h
  (breaks removed) = 54,000 s; demand 920/day → **takt ≈ 58.7 s**.
- **Lead time** = Σ inventory days (the ladder at the bottom of the map).
- **Value-added time** = Σ C/T of value-adding steps.
- **Process cycle efficiency (PCE)** = VA time ÷ lead time. A current state of
  250 s VA vs 18 days lead time is typical for batch-and-push plants: PCE well under 1%.

## 4. Design the future state — answer the classic questions in order
1. **Takt**: what is it? Do you need a finished-goods supermarket or build to ship?
2. **Continuous flow**: where can steps with C/T close to each other be joined into a
   cell? Operators needed = Σ work content ÷ takt. Example: 4 steps totalling 210 s at
   58.7 s takt → 3.6 → plan 4 operators, then kaizen to 3.5 or below.
3. **Supermarkets/pull**: where flow is impossible (shared equipment, long changeover,
   distant supplier), put a supermarket and kanban; where you can, use a **FIFO lane**
   with a max quantity instead.
4. **Pacemaker**: the *single* point that receives the schedule. Everything downstream
   of it must flow (FIFO); upstream is pulled by supermarkets.
5. **Level the mix (heijunka)** at the pacemaker and set a **pitch** = takt × pack-out
   quantity (58.7 s × 20 = ~20 min) as the management interval for releasing work.
6. **EPEI** (every-part-every-interval) at shared equipment, in days =
   (number of variants × C/O) ÷ (daily available time − daily run time). Example:
   6 variants × 45 min C/O = 270 min; 900 min available − 750 min run = 150 min/day
   spare → EPEI ≈ 1.8 days. If EPEI is weeks, SMED is the first kaizen.
7. **Kaizen bursts**: the process improvements the future state depends on.

## 5. Size the pull loops
Kanban count N = D × L × (1 + safety) ÷ container quantity.
Example: 920/day, replenishment lead time 0.5 day, 15% safety, 40 per tote →
920 × 0.5 × 1.15 ÷ 40 = 13.2 → **14 kanbans**. Recalculate when demand moves by more
than ~20%; stale kanban counts are the commonest pull failure.

## Gotchas
- C/T is not takt: a step whose C/T exceeds takt × uptime is a bottleneck in waiting.
  Compare C/T against takt adjusted for OEE (e.g. 58.7 s × 0.85 ≈ 50 s planned cycle).
- Inventory counted from the system is usually wrong; count it.
- Designing flow while changeovers take hours forces big batches; schedule SMED first.
- A future state without an implementation plan (loops, owners, dates) is decoration.
  Implement loop by loop, starting at the pacemaker loop.
- Six Sigma pairing: VSM finds *where*; use DMAIC on the step with the variation
  problem (scrap, unstable C/T) rather than mapping again.

## Verify
- [ ] One product family, mapped on the floor, inventory physically counted.
- [ ] Takt, lead time, VA time and PCE computed and shown on the map.
- [ ] Future state has exactly one pacemaker; downstream of it is FIFO flow.
- [ ] Every supermarket has a kanban count from the sizing formula.
- [ ] Cell staffing equals Σ work content ÷ takt (rounded, with the gap as a kaizen target).
- [ ] An action plan with owners and dates exists per loop.
