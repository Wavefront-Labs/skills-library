---
id: computing-software.systems-network-administration.windows-server.event-viewer-custom-views-and-subscriptions
name: event-viewer-custom-views-and-subscriptions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, event-logs, event-viewer, custom-views, event-subscriptions, collector-initiated, wecutil, administrative-events]
level: intro
status: gated
description: "Build Event Viewer custom views across logs, export and share them, and create collector-initiated event subscriptions to gather events from a few servers."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/wec/windows-event-collector
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom views and event subscriptions

## Custom views
Event Viewer > Custom Views > Create Custom View:
- Filter by log, source, level, event IDs, keywords, user, computer and time range.
- The XML tab lets you edit the query directly.
- Export a view to `.xml` and import it on other servers.

Example query for a "server health" view:
```xml
<QueryList><Query Id="0">
  <Select Path="System">*[System[(Level=1 or Level=2) and TimeCreated[timediff(@SystemTime) &lt;= 86400000]]]</Select>
  <Select Path="Application">*[System[(Level=1 or Level=2)]]</Select>
  <Suppress Path="System">*[System[(EventID=10016)]]</Suppress>
</Query></QueryList>
```

## Collector-initiated subscription (small scale)
The collector pulls from a named list of sources: good for a handful of servers; use
source-initiated (GPO) for hundreds.
1. Collector: `wecutil qc`.
2. Sources: `winrm quickconfig`; add the collector's computer account to the source's
   **Event Log Readers** group.
3. Event Viewer > Subscriptions > Create Subscription > Collector initiated > Select
   Computers > Query (same as custom view XML) > Advanced: machine account, delivery
   Normal/Minimize Bandwidth/Minimize Latency.
4. Events land in the **ForwardedEvents** channel (size the log for your volume).
```
wecutil es              # list subscriptions
wecutil gr <name>       # runtime status per source
```

## Verify
- [ ] Custom view opens with expected events; subscription sources Active and events
  arriving in Forwarded Events.

## Checked
2026-10-28. Confirmed on Learn (Windows Event Collector, setting up a source-initiated subscription): collector-initiated subscriptions
name their sources on the collector, Event Log Readers membership, ForwardedEvents channel, wecutil es/gr/qc. Removed as
unconfirmed: the include/exclude event ID syntax, Suppress-element and Administrative Events statements, the Views folder
path and GPP copy tip, the 20 MB default, Network Service for the Security log. The example `<QueryList>` XML is a standard
Event Viewer query not checked on a fetched page (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
