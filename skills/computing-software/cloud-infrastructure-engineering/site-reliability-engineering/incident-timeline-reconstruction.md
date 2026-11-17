---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-timeline-reconstruction
name: incident-timeline-reconstruction
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, postmortems, incident-timeline-reconstruction, postmortem-timeline]
level: practitioner
status: docs-checked
description: "Write the postmortem timeline the way the SRE Book example does: UTC times, outage and incident boundaries marked, and each entry a plain fact."
sources: ["https://sre.google/sre-book/example-postmortem/", "https://sre.google/workbook/postmortem-culture/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building the incident timeline

**Goal:** a factual sequence of what happened and when, as the backbone of a blameless postmortem.

## What the Google examples show
- The SRE Book example postmortem has a Timeline section headed by the date and "all times UTC". Its footnote calls the
  timeline a "screenplay" of the incident and says to use the incident timeline from the Incident Management document
  to start filling in the postmortem's timeline, then supplement it with other relevant entries.
- Entries are one line each: time, then the event. The example separates distinct boundaries in capitals:
  - `OUTAGE BEGINS` (when the service started failing, here before anyone was paged),
  - `INCIDENT BEGINS` (when an incident was declared and an incident commander named),
  - `OUTAGE MITIGATED`, `OUTAGE ENDS`,
  - `INCIDENT ENDS`, which in the example records that it "reached exit criterion of 30 minutes' nominal performance".
- Each entry states what a named person or system observed or did (a page, a finding in logs, a load balancing change),
  including steps that did not work: one entry records an order-of-magnitude error found in a capacity calculation, and
  traffic shifting was reverted and retried in stages.
- The example summary block also lists Impact, Root Causes, Trigger, Detection and Action Items beside the timeline, so
  the timeline supports those fields rather than replacing them.

## Process notes (Workbook, Postmortem Culture)
- Write the postmortem promptly: the Workbook's example postmortem was published four months after the incident and the
  incident recurred in the interim. Without a timely postmortem, team members forget key details.
- Prefer a single owner with multiple collaborators.
- Use blameless language; a clear review and communication plan helps stop blameful phrasing.
- Templates make postmortems complete and shareable; Google's postmortem template is linked from the page.

## Procedure
1. Start from the incident channel's own timeline, then add entries from monitoring, pager and change records.
2. Put every time in UTC and say so in the heading.
3. Mark outage start, detection, declaration, mitigation, outage end and incident end as separate entries.
4. Review the draft with the responders for accuracy.

## Verify
- [ ] Heading states the date and that times are UTC; boundary events are marked.
- [ ] Entries are plain facts, including failed attempts, with no blame language.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book example postmortem (timeline format, event boundaries, summary
fields) and the SRE Workbook Postmortem Culture page (timeliness, single owner, blameless language, templates).
Removed: the Atlassian template source (not read), the table of data sources (audit logs, feature flag log, status page),
the milestone and TTD/TTM definitions, the sample timeline with invented times, the practice of recording responder
hypotheses and the advice to flag gaps as questions, none of which appear on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
