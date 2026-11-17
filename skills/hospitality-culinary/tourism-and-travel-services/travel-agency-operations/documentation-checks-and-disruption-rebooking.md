---
id: hospitality-culinary.tourism-and-travel-services.travel-agency-operations.documentation-checks-and-disruption-rebooking
name: documentation-checks-and-disruption-rebooking
category: hospitality-culinary
field: tourism-and-travel-services
product: travel-agency-operations
tags: [travel-agency-operations, travel-agent, travel-consultant, booking-management, needs-analysis, fare-rules, fare-selection, travel-documents, passport-validity, visa, eta, esta, etias, timatic, schedule-change, involuntary-change, irrops, disruption-rebooking, misconnect, eu261, uk261, refunds, travel-insurance, duty-of-care, tourism]
level: practitioner
status: draft
description: "Agent-side servicing: client needs analysis, fare-rule reading, passport/visa/ETA checks, schedule-change handling and rebooking clients through cancellations and misconnects."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Documentation checks and disruption rebooking

**Goal:** book the right trip for the client, make sure they can legally board it, and
get them moving again quickly when airlines change or cancel. (PNR entry mechanics are in
sales-marketing.travel-agency-sales.gds-and-booking-systems.building-a-pnr-in-amadeus-sabre-travelport;
selling and upselling are in the travel-agency-sales skills.)

## 1. Needs analysis before searching
Ask and record: purpose of trip, fixed vs flexible dates, **total budget vs value of
flexibility**, travellers (ages, names exactly as on passport), nationality and residence
of each, loyalty numbers, seating/meal/mobility needs, appetite for connections and
overnight flights, baggage needs. Nationality drives the document check; flexibility
drives fare choice.

## 2. Fare selection = reading the rules
For each option show the client, in plain words:
- Change fee and fare difference rules; refundability (to cash or only to credit/voucher, and its expiry).
- Checked-bag allowance (many basic fares exclude it).
- Seat selection, minimum connection time, same-ticket vs separate tickets.
- **Separate tickets (self-transfer):** if leg 1 is late, the second carrier owes nothing.
  Make the risk explicit and get the client's acceptance in writing.
Record what was explained and when — disputes are won by notes.

## 3. Travel document check (every traveller, every booking)
- **Passport validity:** many countries require 6 months beyond travel; Schengen requires
  ≥ 3 months beyond departure *and* issued within the last 10 years.
- **Visas / electronic authorisations:** e.g. US ESTA, Canada eTA, UK ETA, Australia ETA,
  and the EU's ETIAS once in force. *Uncertain: entry schemes and start dates change —
  check the official government source or Timatic at booking and again before travel.*
- **Transit rules:** an airside transit can still need a transit visa.
- Name on ticket must match passport (minor typos may be correctable; name changes rarely
  allowed).
- Minors travelling with one parent: consent letters may be required.
- Health requirements (yellow fever certificates for some routes).
Advise in writing; the client owns compliance, but a missed check is the agency's reputational risk.

## 4. Schedule changes and disruption
**Schedule change queue item arrives** (airline changes timing):
1. Check whether the itinerary still works: connection times above minimum, same day, client's plans intact.
2. If acceptable → accept in the GDS/airline system, reissue or revalidate the ticket as
   required, notify the client.
3. If not → offer alternatives the airline's waiver allows (other flights, often other
   dates, sometimes refund). Act early: the good alternatives go first.

**Cancellation or missed connection on the day:**
1. Get the client's location and status (at airport? checked bags?).
2. Check the airline's **published waiver/policy** and protected options first, including
   partner carriers if the ticket allows.
3. Rebook and reissue; send new itinerary and e-ticket receipt.
4. Advise on rights: EU261/UK261 (care, possible compensation for flights from the EU/UK or
   on EU/UK carriers into them), the US DOT refund rule for cancellations/significant
   changes, plus travel insurance claims for extra costs. Keep receipts.
5. Adjust downstream bookings: hotel first night, transfers, car hire — call them.

## 5. Gotchas
- A ticket that was **voided, exchanged or refunded** wrongly can leave a client with a
  seat but no valid ticket — always check ticket status after changes.
- Don't cancel a "no-showed" segment carelessly; skipping a sector cancels the rest of the
  journey on most fares.
- Time zones: speak to clients in local time and state the zone.

## Verify
- [ ] Needs recorded; fare rules explained and noted in the booking file.
- [ ] Every traveller's passport validity, visa/ETA and transit needs checked and advised in writing.
- [ ] Schedule changes processed and tickets revalidated/reissued.
- [ ] Disruptions rebooked under the airline waiver; downstream bookings adjusted; rights explained.
- [ ] Final itinerary and ticket status confirmed after every change.
