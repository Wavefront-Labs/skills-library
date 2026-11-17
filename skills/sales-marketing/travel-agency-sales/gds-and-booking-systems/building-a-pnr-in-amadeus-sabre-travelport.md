---
id: sales-marketing.travel-agency-sales.gds-and-booking-systems.building-a-pnr-in-amadeus-sabre-travelport
name: building-a-pnr-in-amadeus-sabre-travelport
category: sales-marketing
field: travel-agency-sales
product: gds-and-booking-systems
tags: [gds-and-booking-systems, gds, global-distribution-system, amadeus, sabre, travelport, galileo, worldspan, apollo, pnr, passenger-name-record, booking-reference, record-locator, cryptic-entries, availability-display, fare-display, fare-quote, ticketing-time-limit, queues, ssr, osi, apis, ndc, cruise-booking-portal, tour-operator-portal, travel-agent]
level: practitioner
status: draft
description: "Book through the trade systems: build a complete PNR (the five mandatory elements) with cryptic entries in Amadeus, Sabre and Travelport, check fares, set ticketing limits, and use supplier portals."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a PNR in Amadeus, Sabre and Travelport

**Goal:** create a complete, priced, correctly timed booking record (PNR) that won't be
auto-cancelled, and know when to use the GDS versus a supplier's own booking portal.

**Uncertainty note:** the cryptic entries below are the commonly taught core formats; each
GDS has many variants, agency-specific settings and graphical front-ends (Amadeus Selling
Platform, Sabre Red 360, Travelport Smartpoint). Verify against your GDS's training
environment and help system (`HE` in Amadeus; Sabre and Travelport have their own format guides) before
using live — this skill has not been tested in a live terminal.

## 1. The five mandatory PNR elements ("PRINT")
**P**hone (contact), **R**eceived from (who requested it), **I**tinerary (at least one
segment), **N**ame(s), **T**icketing arrangement (time limit or ticketed). Missing any → the
system won't end the transaction. Add early: email and SSR APIS/DOCS (passport data) for
international travel, and the client's loyalty number.

## 2. Core entries side by side (example: London–New York, 20 Dec, 1 adult)
| Step | Amadeus | Sabre | Travelport (Galileo) |
|---|---|---|---|
| Availability | `AN20DECLONNYC` | `120DECLONNYC` | `A20DECLONNYC` |
| Sell 1 seat, class Y, line 1 | `SS1Y1` | `01Y1` | `N1Y1` |
| Name | `NM1SMITH/JOHN MR` | `-SMITH/JOHN MR` | `N.SMITH/JOHN MR` |
| Phone / contact | `AP <phone>` | `9<phone>` | `P.<phone>` |
| Ticketing arrangement | `TKTL<date>` (or `TKOK`) | `7TAW<date>/` | `T.TAU/<date>` |
| Received from | `RF<name>` | `6<name>` | `R.<name>` |
| Price itinerary | `FXP` (price & store) | `WP` | `FQ` |
| End transaction & redisplay | `ER` | `E` / `ER` | `ER` |
| Retrieve PNR | `RT<locator>` | `*<locator>` | `*<locator>` |
Exact suffixes for passenger types, fare-basis selection and storing the fare differ —
check the pricing format guides for children/infants and for storing a fare for ticketing.

## 3. Fare and availability displays
- Availability shows flights with booking classes and seats remaining (e.g. `Y9 B4 M0`).
  The booking class you sell determines the fare you can price.
- Fare displays (Amadeus `FQD`, Sabre `FQ`, Travelport `FD` — commonly taught; verify)
  list published fares with rules. Read the fare **rules** (change, refund, advance
  purchase, minimum stay) before quoting; tell the client the key restrictions in writing.
- Price the whole PNR before quoting; taxes and carrier surcharges move the total a lot.

## 4. Keep the booking alive
- **Ticketing time limits**: airlines enforce their own deadlines (via SSR messages) and
  may cancel unticketed space — watch queues for advisories.
- **Queues**: schedule changes, waitlist clearances and time-limit warnings land in
  queues; work them daily.
- **Married segments** and connections: don't cancel one segment of a married connection
  without understanding repricing.
- Add **SSR** (special service requests: meals, wheelchair, DOCS) and **OSI**
  (other service information) correctly so the airline sees them.

## 5. When to use supplier portals instead
- **Cruise lines and tour operators** usually have their own agent booking portals (and
  some are in GDS cruise/tour modules). Portals often show more cabin categories, promos,
  and accept agent ID login so commission tracks to you.
- **NDC** (New Distribution Capability) content: some airline fares and bundles are only
  available via NDC channels or direct airline agent portals, not classic EDIFACT GDS
  displays. Compare before quoting.
- Hotels: GDS rates vs consortium rates vs direct — compare inclusions, not just price.
- Record the supplier booking reference in the PNR or your agency system as a passive
  segment or note so everything lives in one record.

## Gotchas
- Name order/format errors (surname first, title last) — ticket names must match passport.
- Ending without received-from or ticketing element → transaction rejected.
- Selling a booking class that shows seats but pricing a fare from a different class.
- Leaving duplicate/speculative bookings — airlines penalise agencies for churn (ADMs).

## Verify
- [ ] PNR has phone, received-from, itinerary, names (passport format), ticketing element.
- [ ] Fare priced, rules read, key restrictions sent to the client.
- [ ] APIS/DOCS, loyalty numbers and SSRs added where needed.
- [ ] Ticketing deadline in your diary; queues checked daily.
- [ ] Supplier-portal bookings referenced in the master record under your agent ID.
