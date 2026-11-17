---
id: hospitality-culinary.food-and-drink-service.pos-systems.order-entry-coursing-and-split-checks
name: order-entry-coursing-and-split-checks
category: hospitality-culinary
field: food-and-drink-service
product: pos-systems
tags: [pos-systems, food-and-drink-service, pos, point-of-sale, epos, toast, square, square-for-restaurants, lightspeed, clover, micros, oracle-micros, aloha, ncr-aloha, revel, tevalis, order-entry, modifiers, forced-modifiers, seat-numbers, coursing, hold-and-fire, fire-course, kds, kitchen-display, kitchen-printer, split-check, split-bill, voids, comps, menu-programming, end-of-day, z-report, x-report, cash-up, tips]
level: practitioner
status: draft
description: "Restaurant POS craft across Toast, Square, Lightspeed, Micros and similar: entering orders with seats and modifiers, holding and firing courses, splitting checks, voids, menu setup and end-of-day."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Order entry, coursing and split checks on a restaurant POS

**Goal:** what the guest said becomes a kitchen ticket the chef can't
misread, timed the way the table wants it, and a bill that splits and closes
without a manager override.

Button names differ between systems (Toast, Square for Restaurants, Lightspeed,
Oracle Micros Simphony, NCR Aloha, Clover, TouchBistro…). The concepts below
are common to almost all of them; **exact menu paths are not given because they
vary by product and version** — learn your system's equivalents in a training mode.

## 1. Entering an order
1. Open the table (by table number on the floor plan), set **guest count** — it
   drives covers reporting and sometimes auto-gratuity rules.
2. Assign items **by seat number** (see table-service). Seats print on the ticket,
   the runner delivers by them, and the split later is one tap.
3. Use **modifiers**, not free text, wherever they exist: temperature (forced
   modifier on steaks), sides, "no onion", allergen modifiers. Free-text notes are
   easily missed on a KDS and don't flow into reporting.
4. Allergens: use the allergen modifier **and** tell the chef (see
   allergen-and-dietary-service). A note alone is not a protocol.
5. Read the order back to the guest from the screen before sending.

## 2. Coursing: hold and fire
- Assign items to **courses** (1 = starters, 2 = mains, 3 = dessert) as you enter them.
- Send with mains **held**: the kitchen sees them as "on hold"/"away" (or not at all
  until fired, depending on setup), so they can plan but won't cook.
- **Fire** the next course when you clear the previous one. Most kitchens want the
  fire 10–15 minutes before the guest should eat it.
- "Rush" or "fire now" items (a kid's meal) skip the hold — use sparingly.
- If your KDS bumps tickets to expo, check the fire went through (ticket colour /
  timer) rather than assuming.

## 3. Changes, voids and comps
- **Void** = it never should have gone (entry mistake, not cooked). Done before the
  kitchen starts, usually with a reason; after, it needs a manager.
- **Comp / discount** = it was made and served but given free. Always choose the
  correct reason code — this is how waste and service failures are tracked.
- Never delete-and-re-ring to dodge a manager approval — it shows in audit logs.

## 4. Split checks
- **By seat** — fastest if seats were entered properly.
- **Evenly** — split N ways; watch for rounding cents landing on one check.
- **By item** — move items between checks; shared items can often be divided
  (e.g. a bottle ½ and ½).
- Split **before** applying discounts or tips where possible; some systems
  recalculate tax and service charges per check, others don't.
- Confirm totals with the table before running cards.

## 5. Menu programming (manager tasks)
- New item: name (kitchen-readable short name), price, tax category, **kitchen
  routing** (which printer/KDS station), course default, modifier groups, allergen tags.
- 86 an item in the POS the moment it runs out, so servers can't sell it.
- Test every new item through to the KDS/printer before service.

## 6. End of day
- Close or transfer all open checks; settle tips per policy.
- Run the **X report** (mid-shift, doesn't reset) vs the **Z report** (end of
  day, closes the business date) — terminology is common but systems vary.
- Reconcile cash drawer to expected cash; card batch to the processor report.
- Review voids and comps by server.

## Gotchas
- Free-text modifiers that don't print on a particular station.
- Items routed to the wrong printer (desserts going to the grill).
- Firing mains when sending starters, because "hold" wasn't set.
- Splitting after the discount — the discount lands on one check only.
- Offline mode: some cloud POSs queue card payments offline; know the risk and
  limit your house sets.

## Verify
- [ ] Every item has a seat number; forced modifiers used for temperature/sides.
- [ ] Mains held and fired on clearing starters; fire confirmed on KDS.
- [ ] Voids vs comps used correctly with reason codes.
- [ ] Split totals confirmed with the guests before payment.
- [ ] New menu items tested to the right station; 86s entered immediately.
- [ ] End-of-day report reconciled to cash and card batch.
