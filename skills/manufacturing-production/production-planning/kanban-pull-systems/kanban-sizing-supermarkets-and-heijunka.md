---
id: manufacturing-production.production-planning.kanban-pull-systems.kanban-sizing-supermarkets-and-heijunka
name: kanban-sizing-supermarkets-and-heijunka
category: manufacturing-production
field: production-planning
product: kanban-pull-systems
tags: [kanban-pull-systems, kanban, production-kanban, withdrawal-kanban, signal-kanban, triangle-kanban, two-bin, e-kanban, kanban-sizing, kanban-formula, supermarket, pull-system, heijunka, heijunka-box, load-levelling, pitch, epei, every-part-every-interval, conwip, wip-cap, replenishment, lean, toyota-production-system, tps, water-spider, mizusumashi]
level: practitioner
status: draft
description: "Run production on pull: size kanban loops from demand, lead time and safety, design supermarkets, level the mix with a heijunka box, and decide when CONWIP fits better."
sources: ["Toyota Production System practice (general reference)", "Hopp & Spearman, Factory Physics (CONWIP, general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kanban and pull: sizing loops, supermarkets and heijunka

**Goal:** replenish only what was consumed, with a fixed and visible amount of
inventory in each loop, so overproduction stops and problems become visible. (For
kanban in knowledge work see
business-finance.project-and-program-management.agile-delivery.kanban-flow-and-forecasting —
a different use of the word.)

## 1. Where pull fits
Pull works for **repetitive parts with reasonably stable demand** (often the
high-volume "runners" and "repeaters"). Low-volume, erratic or one-off parts ("strangers")
are usually better made to order. Map volume per part and choose per part, not per plant.

## 2. Sizing a kanban loop
A common formula:
**Number of kanbans = (D × L × (1 + S)) / C**, rounded up
- **D** = average demand per time unit (e.g. parts/day)
- **L** = replenishment lead time in the same unit: waiting for the card to be
  collected + queue + changeover + processing + move back
- **S** = safety factor (e.g. 0.1–0.3), reflecting demand and supply variability
- **C** = container quantity
Example: D = 400/day, L = 1.5 days, S = 0.2, C = 50 → 400 × 1.5 × 1.2 / 50 = 14.4 →
**15 kanbans**.
- Lead time is the big lever: halving changeover and queue time halves the loop.
- Re-size when demand changes materially (e.g. monthly from the plan), not daily.
- For batch processes, add the **lot-size** effect: cards accumulate until a batch
  trigger (signal/triangle kanban at a reorder point).

## 3. Supermarkets
A supermarket is a controlled store at the point of use or between processes:
- **Fixed locations** per part, max/min marked, first-in-first-out (gravity racks,
  lanes).
- **Withdrawal kanbans** move parts from supermarket to user; **production kanbans**
  authorise the supplying process to make more.
- A **material handler** ("water spider") runs a fixed route at a fixed interval,
  collecting cards and delivering parts — making collection time predictable, which
  is part of L above.
Rule: **no card, no production; no card, no move.** Parts made without a card are
overproduction.

## 4. Heijunka: level the mix
If the pacemaker process builds in big batches (all A Monday, all B Tuesday), the
upstream loops see huge swings and need large inventories.
- **Pitch** = takt × pack-out quantity (e.g. takt 60 s × 20 per container = 20 min).
- A **heijunka box** has a slot per pitch interval; production kanbans are loaded into
  slots in a levelled sequence (e.g. A B A C A B…). The pacemaker takes the next card
  each pitch — volume and mix are levelled.
- The **EPEI** (every part every interval) shows how often each part can be made given
  available changeover time; shrinking changeovers lets you level more finely.

## 5. CONWIP as an alternative
**CONWIP** (constant work in process) caps total WIP across a whole line with one card
loop: a job enters only when one leaves. Simpler than part-specific kanbans and
handles a wide product mix; you still need a sequence (backlog list) for what enters
next. Good for high-mix lines where per-part supermarkets would be huge.

## 6. Running and improving
- Audit loops weekly: cards in circulation = planned number? Lost cards silently
  shrink the loop and cause shortages.
- Use the loop to improve: once stable, remove a card and see what breaks (changeover,
  breakdowns, quality) — fix it.
- Keep a planner's override for known spikes (promotions, shutdowns) by adding
  temporary cards with an end date.

## Gotchas
- Kanban on unstable demand without re-sizing → stockouts then excess.
- Using kanban while MRP still releases orders for the same parts: double replenishment.
- Supermarkets that become "general storage" with no max.

## Verify
- [ ] Pull chosen per part from volume/variability; strangers excluded.
- [ ] Loops sized with measured lead time and stated safety factor.
- [ ] Supermarkets have fixed locations, max/min and FIFO.
- [ ] Pacemaker levelled by heijunka/pitch; EPEI known.
- [ ] Card counts audited; MRP not double-ordering kanban parts.

*Draft note:* the formula is one common form; companies vary the safety term and
lead-time components.
