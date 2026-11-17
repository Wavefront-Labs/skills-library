---
id: computing-software.it-support-helpdesk.servicenow.measuring-self-service-deflection
name: measuring-self-service-deflection
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, self-service-portal, self-service, deflection-measurement, contact-deflection, knowledge-usage, containment-rate, channel-shift]
level: practitioner
status: draft
description: "Measure self-service deflection honestly: deflection vs containment definitions, data from portal search, article views and bot sessions, per-channel baselines and cost saved."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
  - "https://www.serviceinnovation.org/kcs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# measuring-self-service-deflection
Goal: a defensible number for how many contacts self-service prevented,
not a vanity count of page views.

## Definitions
- **Self-service success (deflection)**: a user who started in self-
  service and did not open a ticket or call about the same issue within a
  window (commonly 24-72 hours).
- **Containment** (bots): conversations resolved without live agent or
  ticket.
- **Self-service usage**: visits, searches, views. Activity, not outcome.

## Data sources
- Portal search events with no ticket created by that user within N hours.
- Knowledge article views followed by "Was this helpful? Yes" and no ticket.
- Virtual agent: topic completion without transfer.
- SSPR: successful resets (Entra audit) vs reset tickets.
- Catalog: requests submitted via portal (that is channel shift, report
  separately from deflection).

## A simple calculation
deflection rate = sessions with intent and no follow-up contact ÷ sessions
with intent. Exclude navigation-only visits. Sample-validate: pull 50
"deflected" sessions and check the users did not email or phone instead.

## Baselines and trends
- Track contacts per 100 employees per month; real deflection should push
  it down while headcount is steady.
- Compare top incident categories before/after a new article or bot topic
  for that category.

## Value
Contacts avoided × cost per assisted contact (see cost-per-ticket skill)
minus self-service run cost. Report as a range and state assumptions.

## Gotchas
- Users who give up and phone appear as "deflected" if you only check
  tickets; include phone/chat contacts in the follow-up check.
- Counting every article view as a deflected call inflates numbers 5-10x.
- Portal requests replacing phone requests are channel shift, not
  deflection (the work still happens).

## Verify
The deflection figure has a written definition, a follow-up window, a
validated sample, and moves with changes you made to self-service.
