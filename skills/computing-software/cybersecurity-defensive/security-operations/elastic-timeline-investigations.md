---
id: computing-software.cybersecurity-defensive.security-operations.elastic-timeline-investigations
name: elastic-timeline-investigations
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, elastic-timeline, investigation, eql-correlation, timeline-templates, case-management, alert-investigation]
level: practitioner
status: docs-checked
description: "Investigate alerts in Elastic Security Timeline: building timelines from alerts, EQL correlation tab, pinned events and notes, templates, and attaching to cases."
sources: ["https://www.elastic.co/guide/en/security/current/timelines-ui.html", "https://www.elastic.co/guide/en/security/current/timeline-templates-ui.html", "https://www.elastic.co/guide/en/security/current/cases-overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Timeline investigations

**Goal:** turn an alert into a reconstructed sequence of events with evidence and notes
that another analyst can follow.

## Start from the alert
Alerts table > *Investigate in timeline* opens a timeline filtered to the alert's
source events. Add context with the drag-and-drop field values or the query bar:
```
host.name : "WS-0142" and @timestamp >= "2026-10-15T09:00" and @timestamp <= "2026-10-15T11:00"
```
Widen step by step: same host in a time window, then same user across hosts, then the
network destination across the estate.

## Tabs
- **Query:** KQL search with column selection (add the process, user and
  network fields you need).
- **Correlation:** EQL, for sequences inside the timeline:
  `sequence by host.id [authentication where event.outcome=="success"] [process where process.name=="psexec.exe"]`
- **Analyzer:** process tree for endpoint events (parent/child, network and file events).
- **Session view:** Linux interactive sessions captured by Elastic Defend.
- **Pinned:** only the events you pinned; this is the story.
- **Notes:** timeline-level and per-event notes in Markdown.

## Working method
1. Pin each event that proves a step (initial access, execution, persistence, lateral movement).
2. Add a note per pinned event: what it shows, why it matters, ATT&CK technique.
3. Save the timeline with a clear title (`INC-2026-114 WS-0142 Qakbot`).
4. Attach the timeline to a **case** (Cases > Create), add alerts to the case, and track
   tasks and status there; push to Jira/ServiceNow via the case connector.

## Timeline templates
Save common investigations as templates with placeholder fields (`{host.name}`) and link
them to rules (rule setting *Timeline template*) so *Investigate in timeline* opens a
pre-built query for that detection.

## Gotchas
- Timelines query the selected data view; events in other indices are invisible until you
  switch or extend the data view.
- Unsaved timelines are lost; save early.
- Large time ranges over high-volume indices are slow; filter by host or user first.

## Verify
A second analyst opens the saved timeline from the case and can describe the attack chain
from pinned events and notes alone.

## Checked

Date: 2026-10-28

- Confirmed in the Timeline and template pages: drag fields to build the query, query builder, notes on alerts/events/timeline, save before leaving the page, data view selection, timeline templates attach to detection rules, create a rule from a timeline, visual event analyzer.
- Removed: the ECS field list for columns. Example hostnames, times and process names are illustrative values.
Method: documentation only; no commands were run.

