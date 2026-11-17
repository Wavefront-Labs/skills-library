---
id: engineering-technology.chemical-engineering.process-control.alarm-flood-analysis
name: alarm-flood-analysis
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-alarms-and-interface, alarm-flood-analysis, alarm-flood, alarm-statistics, bad-actors]
level: practitioner
status: gated
description: "Analyse alarm floods from the historian: alarm rates, top bad actors, stale alarms and flood event reviews."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
  - "https://www.isa.org/products/ansi-isa-18-2-2016-management-of-alarm-systems-for"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alarm flood analysis

**Goal:** Analyse alarm floods from the historian: alarm rates, top bad actors, stale alarms and flood event reviews.

## Steps
1. Export alarm and event logs for several weeks to months and compute the alarms per operator per hour and per ten minutes.
2. Define flood periods (for example above a threshold count per ten minutes, per ISA-18.2 (ANSI/ISA-18.2-2016, Management of Alarm Systems for the Process Industries) and EEMUA 191 guidance; confirm the numbers used (gated: unconfirmed, source is paywalled or blocked)) and measure the fraction of time in flood.
3. Rank the top bad actors (the few alarms that cause most of the count); fix chattering and repeats first.
4. Find stale alarms standing for long periods and the consequential alarms in a flood, and apply suppression or grouping.
5. Re-measure after the changes and report the trends.

## Gotchas
- Raw counts need a context of plant state; startup periods show floods.
- Maintain the log data quality.

## Verify
- [ ] Top 10 alarms are identified.
- [ ] Post-change rates are compared with the baseline.
