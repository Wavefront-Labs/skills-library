---
id: hospitality-culinary.guest-accommodation.property-management-systems.reservations-rates-folios-and-channel-sync-in-a-pms
name: reservations-rates-folios-and-channel-sync-in-a-pms
category: hospitality-culinary
field: guest-accommodation
product: property-management-systems
tags: [property-management-systems, guest-accommodation, pms, hotel-pms, opera, oracle-opera, opera-cloud, mews, cloudbeds, protel, rms-cloud, little-hotelier, apaleo, stayntouch, reservations, room-inventory, room-types, rate-codes, rate-plans, availability, restrictions, folio, folio-routing, split-folio, guest-profile, channel-manager, siteminder, ota, booking-engine, overbooking, mapping, inventory-sync, allotment, group-block]
level: practitioner
status: draft
description: "Hotel PMS craft (Opera, Mews, Cloudbeds, Protel and similar): build room types and rate plans, make and modify reservations, route folios, and keep channel-manager mapping and inventory in sync."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reservations, rates, folios and channel sync in a PMS

**Goal:** the PMS is the single source of truth — every room type, rate and
reservation in it is correct, and every OTA and the booking engine show exactly
what the PMS says.

Concepts are common across Oracle Opera/Opera Cloud, Mews, Cloudbeds, Protel,
Apaleo, RMS Cloud and others; **screen names and menus differ and aren't given
here.** Use a training/sandbox property to practise.

## 1. Setup that everything depends on
- **Room types** (inventory buckets you sell: e.g. Standard King, Deluxe Twin)
  vs **rooms** (the physical numbers, each with features: floor, view, accessible,
  connecting). Keep room types few and meaningful — every one needs mapping to
  every channel.
- **Rate plans / rate codes**: a base (BAR) plus derived rates (± % or fixed amount)
  with their own rules: cancellation policy, deposit, inclusions (breakfast),
  market segment and source codes for reporting.
- **Restrictions**: min/max stay, CTA/CTD, stop-sell, per rate and room type.
- **Packages / inclusions** post to the right revenue department (breakfast to F&B,
  not rooms) — this matters for accounting.

## 2. Reservations
1. Search the **guest profile** first to avoid duplicates; merge duplicates when found.
2. Dates, room type, rate code, guests (adults/children), guarantee type (card,
   deposit, company), market segment and source.
3. Special requests and preferences as structured traits where possible, not only notes.
4. Confirmation sent from the PMS template.
- **Modifications:** changing dates or room type can re-price the stay — check the
  rate after any change.
- **Group blocks / allotments:** hold inventory with a cut-off date; release unsold
  rooms back to general inventory at cut-off (diary it).

## 3. Folios and routing
- Each reservation can have multiple **folios (windows)**: e.g. window 1 room and tax
  to the company, window 2 incidentals to the guest.
- **Routing instructions** send charge types automatically to the right folio or to
  another room (a parent paying for children's rooms).
- **City ledger / direct bill**: approved companies settle on account after
  check-out; needs a credit-approved account set up first.
- Corrections: use the PMS's adjustment/rebate function with reason codes, never
  delete history.

## 4. Channel manager sync
The channel manager (built-in or third-party such as SiteMinder) pushes
availability, rates and restrictions to OTAs and pulls bookings back.
- **Mapping:** each PMS room type + rate plan is mapped to each OTA's room and
  rate. A missing or wrong mapping = bookings at the wrong rate, or not delivered.
- After any new rate or room type: map it, then **test** (look at the OTA extranet
  or do a test booking per the channel's process).
- Watch for **sync errors / failed deliveries** in the channel manager log daily.
- Overbooking risk: if a channel caches availability, a sudden sell-out can still
  take bookings — keep a small buffer or fast stop-sell on high-demand dates.
- OTA virtual cards (VCC): note the activation date before charging.

## 5. Daily housekeeping of the data
- Clear past-date unresolved reservations (no-shows, early departures).
- Review the **rate check/discrepancy** report.
- Check that arrivals from channels have a valid guarantee.

## Gotchas
- Duplicate guest profiles — history and loyalty get split.
- Changing a base rate and forgetting derived rates move with it (by design).
- New room type created in the PMS but not mapped → invisible on OTAs, or worse,
  bookings with no matching type.
- Inclusions posted to rooms revenue, inflating ADR.
- Group cut-off not released; the hotel looks full for no reason.

## Verify
- [ ] Each room type and rate plan has rules, segment and source codes set.
- [ ] Reservations checked for duplicate profiles and correct guarantee.
- [ ] Folio windows and routing match who pays what.
- [ ] Every room type × rate plan mapped and test-checked on each channel.
- [ ] Channel manager error log checked today.
- [ ] Group blocks have cut-off dates diarised.

*Uncertain:* feature names and capabilities vary by PMS vendor and version.
