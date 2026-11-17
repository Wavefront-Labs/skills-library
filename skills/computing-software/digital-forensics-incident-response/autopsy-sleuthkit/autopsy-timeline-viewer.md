---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.autopsy-timeline-viewer
name: autopsy-timeline-viewer
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [autopsy-timeline, autopsy, timeline-analysis, event-filters, histogram, sleuthkit, dfir]
level: practitioner
status: docs-checked
description: "Use Autopsy's Timeline viewer to find activity bursts, filter by event type, zoom into incident windows and read events in order."
sources: ["https://sleuthkit.org/autopsy/docs/user-docs/latest/timeline_page.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autopsy timeline viewer

**Goal:** see when things happened across file system, web, registry and other events in a
case, spot bursts of activity and drill into the incident window without exporting to CSV.

## Prerequisites
Since Autopsy 4.13 timeline events are generated during ingest and stored in the case database,
so older cases no longer work with Timeline. Per the user guide, during ingest:
- enable the Hash Lookup module and use the NSRL to ignore known files;
- enable Recent Activity (web-related and other miscellaneous events);
- enable the Picture Analyzer module (events for image timestamps);
- enable Email Parser for email data, and the Android analyzer for mobile devices.

Open it with the Timeline button or Tools > Timeline. You can open it while an image is still
processing, but the data is incomplete until ingest finishes.

## Event taxonomy
Every event has a timestamp, a type and a description. Types: File System (Modified, Access,
Created, Changed); Web Activity (downloads, cookies, bookmarks, history, searches, form
autofill); Miscellaneous (messages, GPS routes, location history, calls, email, recent
documents, installed programs, Exif metadata, devices attached, log entry, registry).

## Views
- **Counts:** stacked bar chart of events per period, colour-coded by type; the default view.
  Shows how much activity occurred (when the computer was last used, how often), not specific
  events. Linear or logarithmic vertical scale; the log scale is applied per event type, so
  use actual counts (tooltips or result viewer) for absolute comparisons.
- **Details:** events clustered by description along the time axis; use it after Counts has
  identified a window. Settings: Band by Type, One event per Row, Truncate Descriptions,
  Description Visibility. The [+] and [-] buttons on a cluster expand and collapse it.
- **List:** every event in order within the selected range; useful for what happened before
  and after an event of interest. Narrow with filters first because there can be thousands.

## Zooming and range
Three zoom levels: Time Units, Event Type, Description Detail. Double-clicking changes only one
of them. Back and forward history buttons or Alt + Left/Right undo a navigation. Adjust the
visible range by typing start and end times, the hour-glass buttons, a preset, the range
slider, or right-drag a span then double-click it. The histogram behind the slider covers all
events and is not affected by filters or zooming; use it for context only.

## Filters
- Event Types filter (also the legend).
- Text filter: substring match against the full description, even if not displayed.
- Hide Known Files: needs the Hash Lookup module run with a known hash set enabled.

## Time zone
You can view events in local time zone or UTC; choose deliberately so the displayed times
match your report convention.

## Workflow
1. Start in Counts over the whole range and identify the incident window.
2. Zoom in, switch to Details or List, filter to the relevant event types, and read around the
   first event of interest.
3. Click an event to see its details in the lower right section.

## Gotchas
- At full Description Detail, little is clustered and the UI can lag; narrow the range or
  filter first.
- The histogram is for relative comparison, not exact numbers or times.

## Self-check
Your narrative cites events with exact times and states the time zone shown, and you confirmed
the ingest modules feeding those event types ran.

## Checked
2026-11-09. Confirmed on the Autopsy user guide Timeline page (read in full): ingest-time events since 4.13, recommended ingest modules, event taxonomy, three views and their uses, zoom levels, filters (Hide Known Files needs Hash Lookup), histogram behaviour, local/UTC time zone, history shortcut. Removed: first-launch database build, pinning, tagging events into the report, "View in Timeline", data source/hash set/tagged/file type filters, NtfsDisableLastAccessUpdate, EVTX/Plaso remarks, the autopsy.com source (landing page).
Method: documentation only; no commands were run.
