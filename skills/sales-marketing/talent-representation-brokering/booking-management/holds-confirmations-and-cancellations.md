---
id: sales-marketing.talent-representation-brokering.booking-management.holds-confirmations-and-cancellations
name: holds-confirmations-and-cancellations
category: sales-marketing
field: talent-representation-brokering
product: booking-management
tags: [booking-management, booking-agent, talent-agent, model-agency, live-music, speaker-bureau, availability, holds, first-hold, second-hold, option, challenge, confirmation, booking-contract, deposit, rider, double-booking, calendar, radius-clause, cancellation, force-majeure, kill-fee, advancing, tour-routing]
level: practitioner
status: draft
description: "Run a represented client's calendar: hold/option ladder, challenge rules, written confirmation and deposit, radius checks, advancing the date, and handling cancellations without double-booking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Holds, confirmations and cancellations — booking management

**Goal:** every date on the client's calendar is in exactly one known state, no date is
ever sold twice, and a cancellation costs the client as little as possible.

Terminology follows common live-music and model-agency practice ("holds" vs "options");
exact conventions vary by agency and territory, so agree definitions with buyers up front.

## 1. One calendar, explicit states
Keep a single master calendar (shared calendar, booking software or a spreadsheet — one
source, not three). Every date carries one state:
| State | Meaning | Who can change it |
|---|---|---|
| Available | Nothing pencilled | agent |
| Hold 1 / Hold 2 / Hold 3 | Ranked pencils from different buyers | agent |
| Option (model/talent) | Buyer has priority until expiry date | agent, on expiry |
| Confirmed | Signed contract or written confirmation + deposit | agent + client |
| Personal block | Client unavailable | client |
| Travel / routing | Committed to getting somewhere | agent |
Each entry records: buyer, contact, fee offered, expiry date/time, date created.

## 2. The hold ladder and challenges
- First hold has priority. If a lower hold turns into a firm offer, **challenge** the
  first hold: tell that buyer they have a fixed window (commonly 24–48 h) to confirm
  or release.
- Put every hold's **expiry** in the calendar and review holds daily; stale holds block sales.
- Never upgrade a hold to confirmed without the client's yes.

## 3. Confirmation — make it real
A date is confirmed only when you have:
1. Written offer accepted by the client (email is the minimum).
2. Booking contract or confirmation sheet: date, times (load-in, set/performance length,
   curfew), venue/location, fee, payment terms, deposit amount and due date, cancellation
   terms, rider/tech attached, billing/credit, usage rights (for shoots), radius clause.
3. Deposit received where the contract requires one (often a percentage up front).
Then: move state to Confirmed, notify the client, and release or re-rank other holds.

## 4. Double-booking prevention
- Check **radius clauses** before confirming: a festival may bar the client from playing
  within X miles/km for Y days before and after.
- Check travel: can the client physically get from yesterday's date to this one?
- Check exclusivity in existing deals (e.g. a brand contract blocking a competitor shoot).
- Two-person rule for confirmations on busy rosters: the booker enters, a second person
  checks the calendar before the contract goes out.

## 5. Advancing (a week or two out)
Reconfirm with the buyer: times, address, contacts on the day, parking/load-in, tech,
hospitality, payment method for any balance. Send the client a one-page day sheet.

## 6. Cancellations
- **Buyer cancels:** apply the contract's cancellation schedule (e.g. kill fee rising as
  the date approaches); invoice promptly; reopen the date and tell holds-in-waiting.
- **Client cancels:** tell the buyer immediately, offer a replacement or reschedule;
  check force-majeure/illness clauses and whether a medical note is required.
- Weather/venue failure: read the force-majeure clause — who keeps the deposit varies.
- Log every cancellation with reason and money outcome.

## Gotchas
- "Soft yes" on the phone that never gets written down — the commonest dispute.
- Time zones on international dates; write times with the zone.
- Calendar sync lag between tools; the master calendar wins.
- Releasing a hold verbally and forgetting to update the calendar.

## Verify
- [ ] Every future date has exactly one state and an owner.
- [ ] Every hold/option has an expiry, reviewed today.
- [ ] Every confirmed date has a signed confirmation and (if required) a received deposit.
- [ ] Radius, travel and exclusivity checks recorded on the booking.
- [ ] Day sheet sent to the client after advancing.
