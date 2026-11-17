---
id: sales-marketing.trade-show-and-event-sales.lead-capture-and-scoring.badge-scan-notes-and-floor-scoring
name: badge-scan-notes-and-floor-scoring
category: sales-marketing
field: trade-show-and-event-sales
product: lead-capture-and-scoring
tags: [lead-capture-and-scoring, lead-capture, lead-retrieval, badge-scanning, badge-scanner, lead-app, qr-code, trade-show, expo, conference, lead-qualification, lead-scoring, hot-warm-cold, qualification-notes, custom-qualifiers, crm-import, salesforce, hubspot, gdpr, consent, data-hygiene, event-sales]
level: practitioner
status: draft
description: "Get usable leads out of a show: lead-retrieval setup with custom qualifiers, fast standard notes, hot/warm/cold scoring rules, consent capture, and same-day export to the CRM."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Badge scans, notes and floor scoring

**Goal:** every lead leaving the show has a score, a reason, a next step and a consent
status — so follow-up can start the next day instead of a week of guessing.

## 1. Set up lead retrieval before the show
- Order the organiser's **lead-retrieval** licences (app on staff phones, or rented
  scanners) — usually priced per device or user; order enough for peak staffing plus a spare.
- Configure **custom qualifier fields** in the app (most lead-retrieval apps support
  picklists; field names differ by vendor):
  - Score: Hot / Warm / Cold
  - Interest: product lines (multi-select)
  - Timeline: <3 months / 3–12 months / >12 months / none
  - Role in decision: decision-maker / influencer / user / other
  - Next step: meeting booked / demo / send info / call / none
  - Consent: marketing OK / follow-up on request only
  - Free-text note
- Test a scan end to end, including the export file, the day before the show opens.
- Badge with no scannable code? Keep a backup: a short web form on a tablet, or
  photograph the business card into the app.

## 2. Scoring rules (write them down, same for every staffer)
| Score | Rule |
|---|---|
| **Hot** | Relevant role + active project/need + timeline ≤ ~3–6 months, or asked for a meeting/pricing |
| **Warm** | Relevant role and a real interest, but no near-term project or not the decision-maker |
| **Cold** | Curious, wrong fit, student, vendor, prize-draw only |
Adjust thresholds to your sales cycle; the point is consistency across staff.

## 3. Notes at speed (10 seconds after each conversation)
Use a fixed shorthand pattern so notes are searchable:
`NEED: <problem in their words> | NOW: <current tool/vendor> | WHO: <other stakeholders> |
NEXT: <agreed step + date> | PERSONAL: <one hook for the follow-up email>`
Example: `NEED: manual reconciliation, 5-day close | NOW: spreadsheets | WHO: CFO signs |
NEXT: demo Tue 10am | PERSONAL: ran the Boston marathon`.
Write the note *after* stepping away, not while they're talking — but before the next
conversation. Unwritten notes are forgotten within the hour.

## 4. Discipline on the floor
- Scan only real conversations, or tag drive-by scans clearly (e.g. "Cold – giveaway").
- Booth captain reviews each staffer's scans at lunch and end of day: missing scores or
  notes get filled while memories are fresh.
- Hot leads with a booked meeting: put the meeting in the rep's calendar on the spot.

## 5. Consent and data protection
Badge scans give contact data; consent to *marketing* is a separate question in many
jurisdictions (GDPR in the EU/UK in particular). Ask or tick the consent field, and
honour "send me this one thing only". Store exports securely; don't email spreadsheets
of attendee data around. Confirm requirements with your legal/privacy team (not verified here).

## 6. Export and hand-off — same day
- Export from the lead app each evening (CSV or direct CRM integration if offered).
- Map columns to CRM fields once, save the mapping; import with a **campaign/source tag**
  (e.g. `Event – <Show> <Year>`) so pipeline can be attributed later.
- De-duplicate against existing contacts and open opportunities; route existing-account
  leads to the account owner.
- Hot leads to sales within 24 h; warm/cold to marketing nurture (see
  sales-marketing.trade-show-and-event-sales.post-event-follow-up.follow-up-cadence-by-lead-score).

## Gotchas
- Organiser exports sometimes arrive days later — use the app's own export if available.
- Custom qualifiers set up on one device but not synced to others.
- "Hot" inflation by enthusiastic staff; audit a sample against the written rules.
- Business-card photos never transcribed.

## Verify
- [ ] Lead app configured with the qualifier fields and tested end to end.
- [ ] Written scoring rules in every staffer's briefing.
- [ ] Every scan has score, next step and consent status; notes follow the pattern.
- [ ] Daily export imported to CRM with campaign tag and de-duplicated.
- [ ] Hot leads assigned to an owner within 24 hours.
