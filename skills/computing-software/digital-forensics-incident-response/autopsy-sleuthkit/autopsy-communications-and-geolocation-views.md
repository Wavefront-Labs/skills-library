---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.autopsy-communications-and-geolocation-views
name: autopsy-communications-and-geolocation-views
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [communications-view, geolocation, autopsy, accounts, call-logs, messages, mobile-forensics, dfir]
level: practitioner
status: docs-checked
description: "Use Autopsy's Communications and Geolocation views to map who talked to whom and where devices were, from messages, call logs and GPS artifacts."
sources: ["https://sleuthkit.org/autopsy/docs/user-docs/latest/communications_page.html", "https://sleuthkit.org/autopsy/docs/user-docs/latest/geolocation_page.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Communications and geolocation views (Autopsy)

**Goal:** visualise relationships and movement across one or many data sources (computers,
phone extractions), useful in insider, fraud and harassment cases. Both views only show what
ingest modules extracted, so run the relevant modules first.

## Communications view (Tools > Communications)
- **Left column:** choose devices, data types and an optional time range, or limit to the most
  recent communications; click Apply to update the tables.
- **Middle column:** each account with its device, type and number of associated messages
  (emails, call logs, etc.), sorted by frequency by default. Both tables have a UI Quick Search.
- **Right column tabs** for the selected account: Summary (counts per data type, files the
  account was found in, and with the Central Repository enabled any personas and other cases
  containing the account), Messages (threaded or under "Unthreaded"; attachments on the
  Attachments tab), Call Logs, Contacts, Media Attachments.
- **Visualize tab:** right-click an account and choose "Add Selected Account to Visualization"
  or "Visualize Only Selected Account". Nodes can be dragged; selecting nodes and edges shows
  their messages or relationships in the right tab. "Snapshot Report" writes a two-page report
  (case summary, then the graph with your filter settings) to the case's Reports folder.

## Geolocation view (Tools > Geolocation, or the Geolocation button)
- Shows artifacts that have longitude and latitude attributes as waypoints; types are
  colour-coded with a key at lower left, and a track is highlighted when you select one of its
  points. Left-click a waypoint for a details pop-up; right-click for a menu like the Result
  Viewer's.
- Filters (click Apply): timestamp within N days of the most recent waypoint (not today's
  date, with a choice to include waypoints without a timestamp); data sources that contain
  geolocation data; waypoint types, with counts.
- The KML Report button exports only the currently visible waypoints to the case's Reports
  folder; the Google Earth KML report module covers all geolocation data in the case.
- Map tiles (Options dialog, Geolocation panel): default online server (Microsoft Virtual
  Earth, bing.com/maps), an OpenStreetMap tile server, an OSM tile zip file (offline), or an
  MBTiles file (offline; download raster, not vector, tiles from OpenMapTiles). Missing tiles
  show grey but waypoints still display. If you cannot or should not use the online default
  server, use one of the offline options.

## Workflow
1. Narrow the time range or date filter to the period of interest.
2. Identify the most active and unknown accounts; read their messages, calls and contacts.
3. Compare waypoints with the times of key messages or events.
4. Export the snapshot and KML reports as needed.

## Gotchas
- Coverage depends on what the ingest modules extracted; a missing account or waypoint may be
  a parsing gap, not proof of absence.
- Normalise times across devices before correlating.

## Self-check
Every relationship or location you report links to its source artifact and timestamp, and you
noted which modules produced the data.

## Checked
2026-11-09. Confirmed on the Autopsy user guide Communications Visualization Tool and Geolocation pages (both read in full): column layout, tabs, Visualize options, Snapshot Report, geolocation filters, KML reports, tile options, offline MBTiles/zip, grey tiles. Removed: the list of specific ingest modules (ALEAPP, iLEAPP etc.), EXIF GPS stripping/spoofing claim, Cellebrite remark, tag/Generate Report HTML/Excel export, edge thickness, pinning, device-correlation claim.
Method: documentation only; no commands were run.
