---
id: computing-software.it-support-helpdesk.servicenow.kcs-evolve-loop-new-vs-known-analysis
name: kcs-evolve-loop-new-vs-known-analysis
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, new-vs-known, kcs-evolve-loop, knowledge-centered-service, content-health, knowledge-management]
level: practitioner
status: draft
description: "Run the KCS Evolve loop new-vs-known analysis: sample closed tickets, classify them as known or new, and use the ratios to fix findability and target content work."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/040/010"
  - "https://www.serviceinnovation.org/kcs/"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# kcs-evolve-loop-new-vs-known-analysis

New vs known analysis (KCS v6 Evolve loop, Process Integration and Content Health) tells
you how much of the desk's work is solving things already solved, and why.

## Definitions
- **Known**: an article existed (published or draft) that resolved the ticket at the time
  it was opened.
- **New**: no article existed; this ticket generated (or should have) a new article.

## Running the analysis
1. Pick a recent period and one queue or product area. Sample 50-100 closed tickets.
2. For each: was an article linked? If yes, did it exist before the ticket? If no
   article linked, search the KB: does one exist that would have solved it?
3. Classify: known-linked, known-not-linked (findability or linking problem), new with
   article created, new with no article (capture problem).
4. Record why for the known-not-linked ones: search terms used, article title mismatch,
   article not visible to that role, agent didn't search.

## Reading the result
| Pattern | Meaning | Action |
|---|---|---|
| High known, linked | KB works; candidates for self-service/automation | Publish to portal, automate top fixes |
| High known, not linked | Findability or habit | Fix titles/keywords to user language; coach search-early |
| High new | Product change or immature KB | Capture in the workflow; review with problem mgmt |
| New, no article | Capture not happening | Coaching, check licensing/rights to create |
A high known ratio at L2 is a shift-left signal: L1 could have solved those.

## Cadence
Quarterly per area, with knowledge domain experts. Track the ratio over time and share it
with team leads; publish the actions taken.

## Verify
The analysis lists specific articles fixed, coaching delivered, and a re-sample next
quarter shows known-not-linked falling.
