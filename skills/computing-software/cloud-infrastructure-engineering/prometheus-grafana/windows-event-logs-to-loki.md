---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.windows-event-logs-to-loki
name: windows-event-logs-to-loki
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [windows-event-log-loki, loki-source-windowsevent, loki-ingest, grafana-alloy, windows]
level: practitioner
status: gated
description: "Ship Windows Event Logs (Application, System, Security, custom channels) to Loki with Alloy loki.source.windowsevent, XPath filters, bookmarks and labels."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.windowsevent/", "https://learn.microsoft.com/en-us/windows/win32/wes/consuming-events", "https://grafana.com/docs/alloy/latest/set-up/install/windows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows event logs to Loki

## Alloy config (Alloy installed as a Windows service)
```alloy
loki.source.windowsevent "application" {
  eventlog_name          = "Application"
  xpath_query            = "*[System[(Level=1 or Level=2 or Level=3)]]"   // critical, error, warning
  use_incoming_timestamp = true
  labels                 = {job = "windows-events"}
  forward_to             = [loki.process.win.receiver]
}

loki.source.windowsevent "security" {
  eventlog_name = "Security"
  xpath_query   = "*[System[(EventID=4625 or EventID=4740)]]"           // failed logon, lockout
  labels        = {job = "windows-events"}
  forward_to    = [loki.process.win.receiver]
}

loki.process "win" {
  stage.json { expressions = {level = "levelText", source = "source", event_id = "event_id"} }
  stage.labels { values = {level = ""} }
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```
Events are emitted as JSON; a real Application event had `source`, `channel`, `computer`, `event_id`, `level` (a number), `levelText`, `taskText`, `opCodeText`, `keywords`, `timeCreated`, `eventRecordID`, `execution`, `security`, `event_data` and `message`. The component also adds the stream labels `channel` (the event's channel name with its original case, for example `Application`) and `computer`.

## Notes
- `bookmark_path` (default `DATA_PATH/bookmark.xml`) stores the last read position so restarts do not resend or skip events; a first start with no bookmark delivered only new events in the test, not the existing history. Pick a path the Alloy service account can write.
- The Security log needs the service account to have read rights to that channel (gated: unconfirmed, source is paywalled or blocked): the Windows group requirement was not checked.
- Custom channels: `eventlog_name = "Microsoft-Windows-PowerShell/Operational"` (name format from the Windows event-log channel list; not run here (gated: unconfirmed, source is paywalled or blocked)).

## Labels
Keep labels to `job`, `channel`, `level`, host; event IDs and sources stay in the line (or structured metadata) to avoid cardinality.

## Verify
- [ ] Query `{job="windows-events", channel="Application"} | json | event_id="1000"` (note the capital A: the label value is the event's channel name, so `channel="application"` matches nothing) returns the test event created with `eventcreate /T ERROR /ID 1000 /L APPLICATION /SO MyTest /D "test"` from an elevated prompt (without `/SO` the tool uses its own source; `/SO` is allowed for custom sources).

## Checked
Ran Alloy v1.21.1 on Windows 11 as a console process with the page's Application source (XPath level filter, `use_incoming_timestamp`, a bookmark file in scratch), a Security-channel source, `loki.process` with `stage.json` and `stage.labels`, and `loki.write` to a local Loki 3.7.9. After `eventcreate /T ERROR /ID 1000 /L APPLICATION /SO RV162 /D test` (elevated) the entry arrived with the JSON fields listed above, labels `job`, `channel="Application"`, `computer`, `level="Error"` (from `levelText`), and `{job="windows-events"} | json | event_id="1000"` matched, while `channel="application"` returned nothing. The page's attribute names were checked against the Alloy v1.21.1 `loki.source.windowsevent` reference (`eventlog_name`, `xpath_query`, `bookmark_path`, `use_incoming_timestamp` default false, `labels`, `exclude_*`, `poll_interval`). The original block failed `alloy validate` only for the missing `loki.write` (a snippet issue). The Windows-service install path and the Event Log Readers statement are gated as marked.
