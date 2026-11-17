---
id: computing-software.digital-forensics-incident-response.log-analysis.velociraptor-client-event-monitoring
name: velociraptor-client-event-monitoring
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-event-monitoring, velociraptor, vql, edr, dfir]
level: advanced
status: draft
description: "Configure Velociraptor client event (monitoring) artifacts: event queries, ETW and log watchers, server-side event processing, alerting and resource limits."
sources: ["https://docs.velociraptor.app/docs/clients/monitoring/", "https://docs.velociraptor.app/docs/vql/events/", "https://docs.velociraptor.app/artifact_references/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Velociraptor client event monitoring

**Goal:** beyond on-demand hunts, Velociraptor clients can run continuous event queries
(CLIENT_EVENT artifacts) that stream results to the server - a lightweight EDR-like capability during an incident.

## Enable
- GUI: **Client Events** > select label or "All" > Update client monitoring table > add artifacts.
- Examples of built-in event artifacts:
  - `Windows.Events.ProcessCreation` (WMI or ETW process start)
  - `Windows.Detection.Usn` / `Windows.Forensics.Usn` style USN watchers for file creation in paths
  - `Windows.Events.ServiceCreation`, `Windows.Events.DNSQueries` (ETW DNS client)
  - `Windows.ETW.*` (various ETW providers), `Generic.Events.FileWatcher`
  - `Linux.Events.ProcessExecutions` (eBPF/audit), `Linux.Events.SSHLogin`
- Scope with labels (e.g. only hosts in the incident scope) to control load.

## Custom event artifact
```yaml
name: Custom.Events.SuspiciousRclone
type: CLIENT_EVENT
sources:
  - query: |
      SELECT * FROM Artifact.Windows.Events.ProcessCreation()
      WHERE CommandLine =~ "(?i)(copy|sync).*--(transfers|config)" OR Name =~ "(?i)rclone"
```

## Server side
- Results land per client in the monitoring store; view under the client's "Client Events".
- **SERVER_EVENT** artifacts can consume client events and alert: `Server.Alerts.*`, or custom VQL with `watch_monitoring()` sending to Slack/Teams/email (`http_client`, `mail`).
```sql
SELECT * FROM watch_monitoring(artifact="Custom.Events.SuspiciousRclone")
```

## Resource control
- Event queries run continuously: test CPU/memory on pilot hosts; use `rate`/`throttle` where available.
- Retention of monitoring data on the server grows quickly; set expiry.

## Gotchas
- WMI-based process events miss very short-lived processes; ETW-based artifacts are better.
- Changing the monitoring table pushes to clients when they next check in; offline clients get it later.

## Verify
A test action on a pilot host (e.g. run a renamed benign binary with rclone-like flags) appears in client events and triggers the server alert.
