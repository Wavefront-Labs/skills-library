---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.outage-tracking-and-tagging
name: outage-tracking-and-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [outage-tracker, incident-tagging, outage-analysis, outalator, incident-database, postmortems]
level: practitioner
status: docs-checked
description: "Run an outage tracker like Google's Outalator: group alerts into incidents, tag them, and analyse trends across teams and months to steer reliability work."
sources: ["https://sre.google/sre-book/tracking-outages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outage tracking and tagging

SRE Book "Tracking Outages": improving reliability needs a known baseline and a way to track progress. Outalator passively
receives all alerts from monitoring and lets users annotate, group and analyse them. Postmortems cover only
high-impact incidents, so frequent small issues and horizontal opportunities with poor per-case cost/benefit fall
outside them; an outage tracker fills that gap.

## What it does
- Shows a time-interleaved list of notifications from several queues at once.
- Stores a copy of the original notification and saves email replies; annotations can be marked "important" so other
  text collapses.
- **Groups** several alerts into one incident. A single event often triggers multiple alerts (a network failure alerts
  every affected team), and grouping allows separate analysis of "incidents per day" versus "alerts per day".

## Tagging
- Tags add metadata to notifications at any level, to separate false positives, test events and mistargeted emails from
  real incidents.
- In Outalator tags are mostly free-form single words; a colon is a semantic separator, which encourages hierarchical
  namespaces such as `cause:network:switch`. Suggested prefixes (primarily "cause" and "action") come from each
  team's historical usage.
- Tags can become links (for example `bug:76543` links to the bug tracker); `bogus` is widely used for false positives.
- The Book deliberately avoids a predetermined tag list: letting teams find their own standards gave more useful data,
  despite typos. Tags proved a powerful way to see a service's pain points even without formal analysis.

## Analysis layers
1. Counting and basic aggregates: incidents per week, month or quarter, alerts per incident.
2. Comparison across teams, services and time, to judge whether an alert load is normal against a service's own record.
3. Semantic analysis for wider issues, such as which infrastructure component causes the most incidents.
Useful questions the Book lists: alerts per on-call shift, the ratio of actionable to nonactionable alerts over the
last quarter, and which service creates the most toil.

## Reporting
Select incidents and email their subjects, tags and important annotations to the next on-call to pass state between
shifts; a report mode expands important annotations for the weekly production review.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Tracking Outages" (Outalator, aggregation, tagging, analysis,
reporting). Corrected: the skill recommended a fixed controlled vocabulary; the Book says it chose free-form tags with
namespaces on purpose. Removed: the incident record table, the vocabulary lists, the tool list, the SQL, the
budget-consumed field and the verify items.
Method: documentation only; no commands were run.
