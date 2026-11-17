---
id: hospitality-culinary.guest-accommodation.revenue-management.pricing-rooms-with-pickup-forecasting-and-overbooking
name: pricing-rooms-with-pickup-forecasting-and-overbooking
category: hospitality-culinary
field: guest-accommodation
product: revenue-management
tags: [revenue-management, guest-accommodation, hotel-revenue-management, revenue-manager, rm, dynamic-pricing, bar, best-available-rate, adr, revpar, occupancy, goppar, trevpar, pickup, pickup-report, booking-pace, on-the-books, otb, forecasting, demand-forecasting, overbooking, wash, no-shows, walking-guests, length-of-stay, los, min-stay, cta, ctd, stop-sell, channel-mix, ota, booking-com, expedia, direct-booking, commission, rate-parity, str, comp-set, rms, ideas, duetto]
level: advanced
status: draft
description: "Hotel revenue basics: read ADR/RevPAR, track pickup against pace, set BAR by demand, use length-of-stay controls, calculate a safe overbooking level, and manage OTA vs direct mix."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pricing rooms with pickup, forecasting and overbooking

**Goal:** sell each night's rooms to the right guests at the highest rate the
market will bear, without leaving rooms empty or walking guests you promised a bed.

## 1. The numbers
- **Occupancy** = rooms sold ÷ rooms available.
- **ADR** (average daily rate) = room revenue ÷ rooms sold.
- **RevPAR** = room revenue ÷ rooms available = occupancy × ADR. The headline metric:
  a 10% rate cut that adds only 5% occupancy lowers RevPAR.
- Also watched: **TRevPAR** (all revenue), **GOPPAR** (profit), net ADR after commissions.
- **Comp set:** 4–8 hotels your guests actually compare you against; benchmark
  index (e.g. RevPAR index vs comp set from a benchmarking service such as STR) —
  100 = fair share.

## 2. Pickup and pace
- **On the books (OTB):** rooms already reserved for a future date.
- **Pickup:** how many were added since the last snapshot (yesterday, last week).
- **Pace:** OTB today vs OTB at the same days-before-arrival last year (or a typical
  curve). Run it daily, per future date, for the next 90–365 days.
Reading it:
- Ahead of pace and comp set priced higher → raise rate.
- Behind pace with no event or seasonality reason → check rate position, visibility
  and restrictions before discounting.
- Sudden pickup spike → find out why (concert, conference, competitor closed) and
  raise rate on remaining inventory.

## 3. Setting BAR and fences
- **BAR** (best available rate) moves by demand; derived rates (advance purchase,
  non-refundable, member, packages) hang off it as percentages.
- **Fences** stop high-paying guests trading down: advance purchase requires
  prepayment; corporate rates require a company profile.
- Change price in steps and give each change a day or two to show in pickup — very
  frequent changes make the signal unreadable (RMS tools automate this).

## 4. Length-of-stay controls
- **Min LOS** on peak nights stops a one-night booking blocking a 3-night stay.
- **CTA / CTD** (closed to arrival / departure) shape stays around peaks.
- **Stop sell** a channel or rate when you no longer need it.
Remove restrictions quickly as the date approaches if they're blocking demand.

## 5. Overbooking
Hotels oversell because some reservations **no-show or cancel late** (the "wash").
A simple rule:
`overbook limit ≈ expected no-shows + late cancels for that date`, using historical
rates by day of week, segment and season.
Example: 200 rooms, history says 4% no-show + 2% late cancel on Tuesdays → about
12 rooms of wash; overbook a little less (say 8–10) because walking a guest is costly.
Weigh: **cost of an empty room** (lost rate) vs **cost of a walk** (paid room
elsewhere, transport, compensation, reputation, maybe a loyalty penalty).
Never walk VIPs, loyalty elites, or multi-night stays if avoidable; walk early in
the evening with a pre-booked alternative, transport and a sincere apology.

## 6. Channel mix
- OTA commissions are commonly quoted around 15–25% — confirm your contracts.
  A direct booking at the same rate is worth more net.
- Use OTAs for visibility and fill; push direct with member rates (where parity
  clauses allow — rules vary by country and contract).
- Track net revenue per channel, cancellation rate per channel, and booking window.

## Gotchas
- Chasing occupancy with discounts and destroying ADR (and RevPAR).
- Forgetting groups and events in the forecast — check group wash separately.
- Restrictions left on near arrival, blocking real bookings.
- Overbooking from gut feel rather than no-show history by segment.
- Rate parity breaches flagged by OTAs.

## Verify
- [ ] Occupancy, ADR and RevPAR known for yesterday, MTD and vs comp set.
- [ ] Pickup and pace reviewed daily for the forward window.
- [ ] Each rate change has a reason tied to pace, comp set or an event.
- [ ] LOS restrictions reviewed and lifted as dates approach.
- [ ] Overbooking limit derived from wash history; a walk procedure exists.
- [ ] Net (after-commission) revenue reviewed by channel.

*Uncertain:* commission ranges and parity rules are approximate; the overbooking
rule is a simplification of what RMS software models statistically.
