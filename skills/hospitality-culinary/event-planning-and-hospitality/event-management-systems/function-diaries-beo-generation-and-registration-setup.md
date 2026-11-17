---
id: hospitality-culinary.event-planning-and-hospitality.event-management-systems.function-diaries-beo-generation-and-registration-setup
name: function-diaries-beo-generation-and-registration-setup
category: hospitality-culinary
field: event-planning-and-hospitality
product: event-management-systems
tags: [event-management-systems, event-planning-and-hospitality, event-software, sales-and-catering, s-and-c, opera-sales-and-catering, delphi, delphi-fdc, tripleseat, caterease, priava, function-diary, space-diary, room-holds, tentative, definite, beo-generation, beo, registration-software, cvent, eventbrite, bizzabo, ticketing, seating-chart, floor-plan-software, social-tables, allseated, attendee-data, integrations, double-booking]
level: practitioner
status: draft
description: "Event software craft: keep the function diary honest with tentative/definite holds, generate BEOs from the booking, set up registration and ticketing, and build seating charts that match the room."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Function diaries, BEO generation and registration setup

**Goal:** one system tells everyone which room is booked for whom, produces the
BEO from the same data, and the guest-side registration and seating tools feed
accurate numbers back — no double-booked ballrooms, no retyped menus.

Venue-side "sales and catering" systems (e.g. Oracle Opera Sales & Catering,
Delphi, Tripleseat, Caterease, Priava) and attendee-side platforms (e.g. Cvent,
Eventbrite, Bizzabo) and floor-plan tools (e.g. Social Tables, AllSeated) differ in
screens and names; **the concepts below are general, the menu paths are not given.**

## 1. The function diary (space diary)
- Every function space, with **combinable rooms** set up correctly (Ballroom = A+B+C;
  booking A blocks the full ballroom). Misconfigured combinations are the main source
  of double bookings.
- **Booking statuses** — typical ladder: Enquiry → Prospect → Tentative (first option,
  second option) → Definite → Actual / Cancelled / Lost. Each status rule: whether
  it blocks the space, and its expiry/decision date.
- **Option dates:** tentative holds have a decision date. Review expired holds weekly
  and either convert or release — stale holds make the house look full.
- Include **setup and breakdown time** around each function so a room isn't sold
  back-to-back with no turnover.
- Lost business: record the reason (price, date, competitor) — feeds sales strategy.

## 2. Generating BEOs from the booking
- Build menus, beverage packages, AV items and room setups as **catalogue items**
  with prices and departments, then attach them to the event. The BEO is generated
  from these, not typed.
- Set **guarantee** and expected numbers on the event; the BEO pulls them.
- Every change creates a **new revision**; distribution lists send the revised BEO to
  kitchen, banquets, AV, engineering, accounts. Mark changes (many systems highlight
  them).
- Resume / summary documents for the week ("BEO pack") printed for the weekly
  meeting.
- Post-event: actual numbers update the invoice (see banquet-coordination).

## 3. Registration and ticketing setup
- Ticket or registration types (early bird, member, speaker, comp) with prices,
  capacity and sale windows.
- Form fields: only what you'll use — name, organisation, email, dietary,
  accessibility, session choices, consent. Make dietary and accessibility
  **structured choices plus an "other" text field**.
- Session capacity limits for breakouts.
- Confirmation emails with calendar invite and venue details; reminder schedule.
- Privacy: collect consent appropriately; restrict who can export attendee data
  (local data-protection law applies).
- **Test the whole journey** with a test registration, including payment and refund,
  before opening.

## 4. Seating charts and floor plans
- Draw the room to scale using the venue's dimensions, with fixed features (pillars,
  doors, stage, bars, exits).
- Use the correct table sizes; let the software count seats and check aisle widths.
- Import attendee list; assign seats; export the alphabetical table plan and escort
  card list.
- Share a view-only link with the client; lock the plan after final numbers.

## 5. Integrations and data hygiene
- If the S&C system links to the PMS (group room blocks) or to accounting, check
  that sync errors are reviewed.
- One owner per event record; avoid side spreadsheets.
- Exports for the kitchen: dietary counts by table.

## Gotchas
- Combinable-room rules wrong → two clients in one ballroom.
- Tentative holds never expiring.
- BEO typed by hand outside the system — now it disagrees with the invoice.
- Registration form missing dietary/accessibility fields.
- Floor plan not to scale, so the "fits" layout doesn't.

## Verify
- [ ] Space combinations tested: booking a sub-room blocks the parent and vice versa.
- [ ] Every tentative hold has a decision date; expired ones reviewed weekly.
- [ ] BEOs generated from catalogue items, revisions distributed.
- [ ] Registration journey tested end-to-end, incl. payment and refund.
- [ ] Seating plan to scale, locked after final numbers, exported alphabetically.

*Uncertain:* status names and feature sets differ by vendor and edition.
