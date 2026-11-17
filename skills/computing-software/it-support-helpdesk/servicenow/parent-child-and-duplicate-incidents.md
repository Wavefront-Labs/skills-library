---
id: computing-software.it-support-helpdesk.servicenow.parent-child-and-duplicate-incidents
name: parent-child-and-duplicate-incidents
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-management, parent-child-incidents, duplicate-tickets, incident-linking, mass-incident, related-records, ticket-merge]
level: practitioner
status: draft
description: "Handle many tickets for one fault: create or find the parent incident, link children so they inherit updates and resolution, merge true duplicates, and keep each user informed."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://support.atlassian.com/jira-service-management-cloud/"
  - "https://support.zendesk.com/hc/en-us"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# parent-child-and-duplicate-incidents

Goal: 80 tickets about the same outage become one piece of work, with 80
users still kept informed.

## Parent / child (one cause, many affected users)
- Create the **parent incident** describing the service-level fault (or use
  the major incident).
- Link each user's incident as a **child** (ServiceNow: Parent field on the
  child, or "Add" in the Child Incidents related list; bulk via list edit).
- ServiceNow behaviour: when the parent is resolved, active children are
  resolved with the parent's resolution details and their callers are
  notified; whether parent work notes/comments copy to children is set in
  the incident properties (System Properties → Incident) — check your
  instance before relying on it.
- Agents: when a new call matches, search active parents first (portal and
  agent workspace often show "known issues/major incidents").

## Duplicates (same user, same issue, multiple tickets)
- Keep the oldest (or most detailed), mark the others duplicates with a link,
  close them with "Duplicate" code, tell the user which number is live.
- JSM: link issues "duplicates" and close; Zendesk: **Merge tickets** (moves
  comments into the target).
- Email reply loops creating new tickets: fix the inbound email action /
  watermark handling, not just the tickets.

## Not a child
Same symptom, different cause (two users with "Outlook won't open" for
unrelated reasons) — don't link just because the words match. Check scope and
timing; a child should resolve when the parent's fix lands.

## Communication
- Update children via the parent (copy comments) rather than 80 separate
  notes.
- Users who report later still get a reference: "This is part of INC-PARENT,
  updates every 30 minutes."

## Reporting
Count of children per parent is a better impact measure than ticket volume;
exclude children from per-agent productivity metrics or they skew it.

## Gotchas
- Resolving the parent before confirming everyone is fixed auto-resolves
  children who are still broken — sample before resolving.
- Children with additional, separate problems need splitting into a new
  incident first.

## Verify
After the event: all related tickets are linked, children closed with the
parent's resolution, and none left orphaned in queues.
