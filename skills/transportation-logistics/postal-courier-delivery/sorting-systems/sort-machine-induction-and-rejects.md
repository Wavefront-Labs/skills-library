---
id: transportation-logistics.postal-courier-delivery.sorting-systems.sort-machine-induction-and-rejects
name: sort-machine-induction-and-rejects
category: transportation-logistics
field: postal-courier-delivery
product: sorting-systems
tags: [sorting-systems, mail-sorting, parcel-sorting, induction, inducting, sort-plan, sort-scheme, reject-handling, no-read, no-reads, rework, cross-belt-sorter, tilt-tray, shoe-sorter, letter-sorting-machine, ocr, video-coding, barcode, scan-tunnel, chute-full, recirculation, sorter-throughput, manual-sort, postal-hub]
level: practitioner
status: draft
description: "Run a mail/parcel sorter shift: pre-start checks, clean induction, sort-plan sanity checks, and a reject/no-read rework loop that keeps read rates up and missorts down."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sort-machine induction and reject handling

**Goal:** keep an automated sorter (cross-belt, tilt-tray, shoe/sliding-shoe, bomb-bay,
or a letter/flats sorting machine) running at rated throughput with a high read rate,
few recirculations and near-zero missorts, and clear the reject stream before the
outbound cut-off.

Vendor HMIs differ (and site sort-plan tools differ more), so the screens named here
are generic; the principles hold across equipment. *Draft: thresholds below are
typical operating targets, not vendor specs — use your site's KPIs.*

## 1. Before the run (10 minutes)
- **Sort plan:** confirm the plan loaded on the controller matches today's run
  (weekday/weekend and peak plans differ). Spot-check 3–5 destinations: chute number on
  the HMI vs the physical chute label vs the outbound trailer/cage it feeds.
- **Chutes:** every active chute has an empty container/cage and a "full" sensor that
  clears. Disabled chutes are marked on the plan so items go to an alternate, not reject.
- **Scan tunnel / OCR:** cameras and scanners clean (dust on a lens is a classic cause of
  a creeping no-read rate). Run the vendor test item or a known-good batch.
- **Safety:** e-stops tested per site schedule, guards closed, lock-out/tag-out for
  anyone clearing jams inside the guarding. Never reach into a moving induct belt.

## 2. Clean induction — where most rejects are made
- **One item per carrier/tray, label up (or label-facing the scanner)**, centred,
  longest side along the direction of travel unless your sorter says otherwise.
- **Gap discipline:** on manual inducts, place on the induct belt's cue (light, beep or
  marked window); don't double-load to "catch up" — doubles go to reject or missort.
- **Non-conveyables out at induction:** rolling items (tubes, tyres), soft bags that
  drape, overweight/oversize, leaking or damaged parcels, loose straps. Route them to the
  manual/irregular stream immediately.
- **Letters/flats:** jog and face the stack (stamps/indicia in the same corner, same
  orientation), remove stiff, bulky or window-damaged items before the feeder.

## 3. Watch the right numbers during the run
Keep the HMI dashboard on these, and act on trends, not single events:
| Signal | Typical action if it rises |
|---|---|
| No-read / no-code rate | Clean scanners; check label quality from one customer/source; check induction orientation |
| Recirculation | Destination chute full or disabled — empty it or reassign |
| Reject (no destination) | Sort plan gap — postcode/route not mapped; escalate to plan owner |
| Jams per hour | Look for one bad item type at induction, not "the machine" |

## 4. The reject and rework loop
1. Rejects land in a reject chute/bin with a reason code if your system provides one
   (no-read, no-rule, over-weight, double, chute-full). **Sort the reject bin by reason**
   — each reason has a different fix.
2. **No-read:** re-label or hand-key the barcode at a rework station, then re-induct.
   Damaged labels get a replacement label, never a guess.
3. **No-rule/unmapped:** manual-sort to the right outbound by lookup; log the code so
   the plan gets fixed for tomorrow.
4. **Video coding (letters):** keyers type the postcode/address image the OCR couldn't
   read; prioritise accuracy over speed — a wrong key is a missort.
5. Clear the reject stream **before** outbound cut-off; schedule a final rework push
   ~30 minutes before trailers close.

## 5. Manual sort schemes (fallback and irregulars)
Sort by "breaking down" in stages — e.g. first by outward code/region into a frame,
then each pigeonhole by delivery route. Learn the scheme in chunks (one area at a time)
and test with a flash-card drill before you work live mail.

## Gotchas
- A read rate that drops suddenly at one time each day is usually one shipper's bad
  labels or a lighting change — not a scanner fault.
- Running with a full chute "for a minute" causes recirculation, which steals capacity
  from new induction: throughput falls faster than you expect.
- Plan changes made mid-shift without updating chute labels cause silent missorts that
  surface only at the delivery office.

## Verify
- [ ] Today's sort plan matches physical chute labels for your spot-checks.
- [ ] Reject bin is sorted by reason and each reason has an owner.
- [ ] No-read rate is stable across the shift (trend checked at least hourly).
- [ ] Every unmapped code from today is logged for the plan owner.
- [ ] Reject stream cleared before outbound cut-off.
