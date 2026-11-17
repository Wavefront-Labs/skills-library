---
id: computing-software.it-support-helpdesk.servicenow.shift-handover-and-follow-the-sun
name: shift-handover-and-follow-the-sun
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-desk, tiered-support, shift-handover, follow-the-sun, handover-notes, major-incident]
level: practitioner
status: draft
description: "Hand over service desk shifts without dropping tickets: handover log format, open P1/P2 and promises due, queue ownership in ServiceNow, and follow-the-sun across regions."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# shift-handover-and-follow-the-sun
Goal: nothing a user was promised is lost when one shift or region hands
to the next.

## Handover content (same template every time)
1. **Live incidents**: P1/P2 open, current status, bridge details, next
   update time, who is incident manager.
2. **Promises due**: call-backs and follow-ups committed for the next
   shift (ticket numbers, time, what was promised).
3. **Queue state**: unassigned count, SLA breaches imminent (use the "SLA
   at risk" list), aged tickets needing action.
4. **Known issues**: outages, workarounds in use, banners posted.
5. **Changes tonight**: scheduled changes that may generate calls.
6. **People**: VIP situations, difficult callers, escalations in flight.

## Mechanics
- Written log (shared doc, Teams channel post, or a ServiceNow handover
  record), plus a 10-15 minute verbal overlap for P1/P2.
- Reassign tickets the leaving agent personally owns that need action
  before they return; leave a work note "Handed to <name>, next action X
  by HH:MM".
- Outgoing shift lead confirms the incoming lead has acknowledged.

## Follow-the-sun
- Regions (e.g. APAC → EMEA → Americas) with overlapping hours of 1-2
  hours for handover calls.
- Global queues with region-agnostic assignment groups; a ticket in a
  regional queue at region close is reassigned to the global queue
  with a work note.
- Common knowledge base and categorisation so the next region can act.
- Time zone shown in ticket promises ("call back 09:00 Europe/London").

## Gotchas
- "Nothing much to hand over" is how P2 updates get missed; always use the
  template.
- Ownership by agent name strands tickets on leave; prefer group ownership
  plus explicit work notes.
- Language/culture differences across regions: write handover notes in
  plain, full sentences, no internal shorthand.

## Verify
Sampling a week, every promised call-back was made on time across shift
boundaries, and every P1/P2 had continuous ownership.
