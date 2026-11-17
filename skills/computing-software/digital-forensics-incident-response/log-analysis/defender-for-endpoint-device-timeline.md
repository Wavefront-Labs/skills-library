---
id: computing-software.digital-forensics-incident-response.log-analysis.defender-for-endpoint-device-timeline
name: defender-for-endpoint-device-timeline
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [mde-timeline, edr, edr-process-tree, advanced-hunting, dfir]
level: practitioner
status: docs-checked
description: "Investigate with the Microsoft Defender for Endpoint device timeline: date range, flagging, exporting, retention, and pivoting to Advanced Hunting."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/investigate-machines", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Endpoint device timeline

**Goal:** the device timeline in the Microsoft Defender portal gives a chronological view of events and associated alerts on a device, the fastest way to reconstruct activity around an alert.

## Navigate
- Open the device page, then the **Timeline** tab.
- By default the timeline shows the past 30 days. Use the calendar icon to show the past day, week, 30 days or a custom range.
- Search with the search bar; use **Filters** to pick data type (events or techniques) and event group, and to choose which columns show.
- Selecting an event opens a side panel with details and the process tree; MITRE ATT&CK techniques appear as bold text with a blue icon.
- Firewall events appear only if the audit policy for Filtering Platform connection is enabled; the page lists firewall events 5025, 5031 and 5157.

## Working an alert
1. Open the alert's process tree; note the first suspicious process time.
2. In the timeline, narrow the range around that time and read process creations and network connections in order.
3. **Flag** relevant events with the flag icon in the Flag column; later enable the **Flagged events** filter and Apply to see only those.
4. Select **Hunt for related events** to run an advanced hunting query returning the selected event and others around the same time on the same endpoint.

## Export
- Export the timeline for the current date or a chosen range of up to seven days at a time; repeat for longer windows.
- For bulk and long ranges, use Advanced Hunting (native data is available for up to 30 days) and export results. To keep hunting tables longer than 30 days, onboard a Microsoft Sentinel workspace and configure retention there.

## Retention
By default timeline events are retained for 90 days per the Defender for Endpoint page; a connected Sentinel or Log Analytics workspace with custom retention may hold events longer. Check your tenant's configured retention before relying on old data.

## Gotchas
- Absence of an event in the timeline is not proof it did not happen; note retention and sensor limits in conclusions.
- If the EDR client is low on resources it enters critical mode and does not process new events until it recovers; a timeline event records the switch.

## Verify
Flagged timeline events are exported with the case and key ones confirmed in Advanced Hunting.

## Checked
2026-11-01. Confirmed against the Defender for Endpoint "Investigate devices" page and the advanced hunting overview: 30-day default range, date range options, seven-day export, flag icon and Flagged events filter, Hunt for related events, firewall event ids, 90-day default retention, critical mode, 30-day hunting range and Sentinel retention. Removed: the 180-day retention figure (page says 90-day default), the event-type and detection-level filter list, entity prevalence pivot, time zone and sampling claims, and the per-table listing (see the defender-advanced-hunting-tables skill).
Method: documentation only; no commands were run.
