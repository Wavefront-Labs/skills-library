---
id: architecture-construction.site-supervision-trade-coordination.procore.running-rfis-daily-logs-and-punch-lists-in-procore
name: running-rfis-daily-logs-and-punch-lists-in-procore
category: architecture-construction
field: site-supervision-trade-coordination
product: procore
tags: [site-supervision-trade-coordination, procore, construction-management-software, rfi, rfis, ball-in-court, daily-log, site-diary, drawings, drawing-markup, current-set, revisions, punch-list, snagging, observations, photos, submittals, field-app, mobile-app, document-control, autodesk-build, aconex, fieldwire]
level: practitioner
status: draft
description: "Use Procore in the field: raise and track RFIs with ball-in-court, keep daily logs that stand up later, mark up current drawings, and close punch items with photos."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running RFIs, daily logs and punch lists in Procore

**Goal:** use Procore so the field record is complete, current and defensible: questions
answered quickly, a daily log you'd be happy to show in a dispute, and punch items closed
with evidence.

*Menu names and permissions depend on your company's Procore configuration and version;
the workflow below is the general pattern (draft, not checked against the current UI).*

## 1. Drawings — always work off the current set
- Open drawings from the **Drawings** tool on the mobile app, not downloaded PDFs; it
  shows the latest revision and flags superseded sheets.
- Download the sheets you need for offline use before going to areas with no signal,
  and re-sync when back.
- **Markups:** personal markups are for you; published markups are visible to others —
  use published ones to link RFIs, photos and punch items to a location.
- Before any trade starts, confirm their sheet revision matches yours.

## 2. RFIs
- One question per RFI. Title that someone can search later ("Level 2 grid C/4 — beam
  penetration for 150 mm duct?").
- Body: what you found, where (link the drawing/area), what the conflict is, and a
  **proposed solution** — designers answer faster when you give them something to accept
  or reject.
- Attach photos and a marked-up drawing snip. Mark cost/schedule impact if known.
- Set the **due date** per contract response time; assign the **ball-in-court** person.
- Track the RFI log weekly: overdue RFIs are your schedule risk. Escalate in the meeting
  minutes, not just by chasing.
- When answered, push the answer to the field: link it on the drawing and tell the
  foreman. An answered RFI nobody saw is worthless.

## 3. Daily log
Fill in **every day**, same day:
- Manpower by company and headcount (and hours if tracked).
- Weather (many projects pull it automatically — add site-specific conditions: "rain
  09:00–11:30, pour postponed").
- Work performed by area; deliveries; equipment on site; inspections and visitors.
- **Delays and issues** with time and cause; notes of instructions received (who, what,
  when).
- Photos with captions.
A daily log is evidence for delay claims, variations and disputes. Facts, not opinions;
no blame language.

## 4. Punch lists
- Walk by area. Create each item with: location (pinned on drawing), description of the
  defect and the required fix, responsible trade, due date, photo.
- Trades mark "ready for review" with an after photo; the supervisor verifies on site
  before closing — never close from the office on a photo alone for anything critical.
- Run punch reports by trade before handover meetings.

## 5. Observations and submittals (brief)
- Observations for safety or quality issues not part of the formal punch.
- Submittals: check the status (approved/approved as noted/revise and resubmit) before a
  trade installs — "approved as noted" means read the notes.

## Gotchas
- Working from a printed old revision while Procore holds the new one.
- RFIs with no proposal or location → slow answers.
- Daily logs filled in at week's end from memory → worthless in a dispute.
- Closing punch items without seeing the work.

## Verify
- [ ] Field devices synced; current drawing revision shown on the sheet you're using.
- [ ] Every open RFI has a ball-in-court, due date and proposal.
- [ ] Daily log done today with manpower, weather, work, delays, photos.
- [ ] Punch items closed only after on-site verification.

*Status: draft — workflow from typical general-contractor practice; tool names may vary
by Procore version and permissions.*
