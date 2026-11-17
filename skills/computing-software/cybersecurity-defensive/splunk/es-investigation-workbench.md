---
id: computing-software.cybersecurity-defensive.splunk.es-investigation-workbench
name: es-investigation-workbench
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, enterprise-security, es-investigation-workbench, investigations, incident-review, artifacts, timeline]
level: practitioner
status: draft
description: "Run Splunk Enterprise Security investigations: create investigations from notables, add artefacts and events, use workbench panels, and record a defensible timeline."
sources: ["https://docs.splunk.com/Documentation/ES/7.3.0/User/Startaninvestigation", "https://docs.splunk.com/Documentation/ES/7.3.0/User/Investigations", "https://docs.splunk.com/Documentation/ES/7.3.0/Admin/Customizeinvestigations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ES investigation workbench (ES 7.x)

Investigations group notables, events, notes and artefacts for one incident and keep a timeline.

## Start one
- From Incident Review, select notables > Add Selected to Investigation > new or existing.
- Or Investigations > Create New Investigation; add collaborators (they need `ess_analyst`).
- Name with the case ID from your ticketing system so the two stay linked.

## Workbench
- **Artifacts** panel: assets/identities/files/URLs. Add from notable fields ("Add artifacts"), then
  select artefacts and run the panels on them.
- Panels (tabs) run searches against selected artefacts: Asset/Identity, Endpoint data
  (process, file, registry from Endpoint DM), Network data, Risk. Admins add custom panels and
  tabs under Configure > Content > Workbench using prebuilt panels or saved searches with
  `$artifact$` tokens.
- **Timeline**: add events from any search (Investigation Bar action "Add event to investigation"
  in the search page) plus notes with times. Use note entries for actions taken (contained host at
  14:02) so the timeline also records response.
- **Summary** tab: description, status, findings. Export as PDF or to the ticket.

## Working practice
1. Add the triggering notable and its key artefacts.
2. Run endpoint and network panels; add each relevant raw event with a one-line note why.
3. Record hypotheses and dead ends as notes; reviewers need them.
4. Close the investigation with disposition; close linked notables with the same disposition.

## Gotchas
- Investigation data is stored in KV store collections (`investigation`, `investigation_attachment`);
  include them in KV store backups.
- Panels use data model searches; if the DM is not accelerated or CIM-mapped, panels show nothing.
- ES 8 replaces this with Mission Control findings and investigations; plan migration of open items.

## Verify
Timeline export contains the trigger, each pivot event, and containment notes in time order;
linked notables show the investigation ID.
