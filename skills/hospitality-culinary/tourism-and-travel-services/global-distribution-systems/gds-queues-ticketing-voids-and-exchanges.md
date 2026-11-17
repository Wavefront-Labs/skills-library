---
id: hospitality-culinary.tourism-and-travel-services.global-distribution-systems.gds-queues-ticketing-voids-and-exchanges
name: gds-queues-ticketing-voids-and-exchanges
category: hospitality-culinary
field: tourism-and-travel-services
product: global-distribution-systems
tags: [global-distribution-systems, gds, amadeus, sabre, travelport, galileo, worldspan, cryptic-entries, pnr, queues, queue-handling, schedule-change-queue, ticketing, ticketing-time-limit, ttl, e-ticket, emd, void, exchange, reissue, refund, bsp, arc, fare-quote, stored-fare, adm, travel-agency, tourism]
level: advanced
status: draft
description: "Working GDS queues and ticketing: daily queue sweep, pricing and issuing, ticket-time limits, voids within the window, and exchanges/reissues in Amadeus and Sabre."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GDS queues, ticketing, voids and exchanges

**Goal:** keep every booking ticketed on time and correct after airline changes, using the
GDS's queues as your work list and the ticketing, void and exchange functions without
generating debit memos. (Building the PNR itself is covered in
sales-marketing.travel-agency-sales.gds-and-booking-systems.building-a-pnr-in-amadeus-sabre-travelport.)

**Status note:** entries below are the commonly taught cryptic formats. Office setups,
host versions and graphical front-ends differ — *treat formats as indicative and confirm
in your GDS help pages (Amadeus `HE <topic>`, Sabre Format Finder) before use.*

## 1. Queues = your inbox
Airlines and your own office place PNRs on numbered queues: schedule changes, waitlist
clearances, ticketing deadlines, ticket-time-limit warnings, special-service-request replies.
- **Count queues first thing and through the day.** Amadeus `QT` (queue totals);
  Sabre `QC/`.
- **Start working a queue:** Amadeus `QS<queue>` (e.g. `QS1C0`); Sabre `Q/<queue>`.
- For each PNR: read the history/remarks, act, then **remove and move to next**
  (Amadeus `QN`; Sabre `QR` to remove, or `I` to ignore and leave it). **Delay** a PNR
  you can't finish yet so it comes back (Amadeus `QD`). Exit queue mode (Amadeus `QI`,
  Sabre `QXI`).
- **Never empty a queue without acting** — an ignored schedule change is a stranded client.
- Typical priorities: schedule changes (UN/TK/HX segment statuses), ticketing time limits,
  waitlist clears (KL), SSR replies.

## 2. Reading segment status codes
`HK` holding confirmed; `TK` confirmed with schedule change — accept by changing to HK;
`UN`/`UC`/`NO` unable / no action — must be removed and rebooked; `HX` cancelled by
airline — remove; `KL` waitlist cleared — confirm. Leftover HX/UN segments cause
airline auto-cancellations and ADMs (agency debit memos) — clean them up.

## 3. Pricing and issuing
1. **Price and store:** Amadeus `FXP` (price and store a TST); `FXB` for best-buy rebook;
   Sabre `WP` to price, `WPRQ` to price and store a PQ.
2. Check passenger type (ADT/CHD/INF), fare basis, baggage and the last-ticketing date
   the fare demands.
3. Add form of payment and commission per office policy.
4. **Issue:** Amadeus `TTP`; Sabre `W‡PQ1` style entries (with your office's FOP qualifiers).
5. Verify: display the ticket (Amadeus `TWD`; Sabre `WETR`) — coupon status `OPEN`/`O` for
   unflown sectors — and send the itinerary receipt.

Ticketing time limits (TTL) set by the airline are hard: miss one and the airline
cancels the space. Put your own internal deadline 24 h earlier.

## 4. Voids
- A ticket can usually be **voided only within the void window** — often until end of
  the same business day in the BSP/ARC reporting period. *Uncertain: windows differ by
  market and carrier.*
- Amadeus: from `TWD`, use the void entry (commonly `TWX`); Sabre: display via `WETR` then void (e.g. `WV`).
- After voiding, **cancel or rebook the segments** — an unticketed PNR left holding space
  attracts ADMs for "churning" or passive segments.

## 5. Exchanges and reissues
- Used after voluntary changes or involuntary schedule changes.
- Use the GDS's automated exchange tool (Amadeus ATC; Sabre automated exchanges) where
  the fare is filed for it — it calculates fare difference, change fee, tax carry-forward and residual value per the fare rules.
- Manual reissues are where ADMs come from: wrong penalty, missing fare difference,
  taxes not collected. Use automation, or follow the carrier's documented waiver codes
  and endorsements exactly for involuntary changes.
- Refunds: automated refund function; non-refundable taxes vs refundable taxes differ.

## Gotchas
- **Duplicate bookings** for the same passenger (in your or another PNR) are policed by
  airlines and cost ADMs.
- Fictitious names and test bookings in live mode also cost money.
- End and retrieve (Amadeus `ER`; Sabre `ER`) after changes to confirm what was saved.

## Verify
- [ ] Queue counts checked at start, midday and end of day; all queues worked to zero or delayed with reason.
- [ ] No HX/UN/UC/NO segments left; TK accepted as HK.
- [ ] Tickets issued before TTL; ticket display shows correct coupons and fare.
- [ ] Voids within window, followed by segment cancellation.
- [ ] Exchanges done with the automated tool or per waiver; receipts sent.
