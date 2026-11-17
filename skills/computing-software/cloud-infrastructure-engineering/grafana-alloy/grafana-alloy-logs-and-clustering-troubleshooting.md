---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-logs-and-clustering-troubleshooting
name: grafana-alloy-logs-and-clustering-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [logging-block, logfmt, journalctl, cluster-split-brain, node-name-conflict, cluster-log-messages]
level: practitioner
status: docs-checked
description: "Read Alloy logs, tell normal from problematic cluster messages, and diagnose common clustering symptoms."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/troubleshoot/debug.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/logging.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy logs and clustering problems

## logging block
Optional, unlabeled, once per file.
```alloy
logging {
  level  = "info"   // error, warn, info, debug
  format = "logfmt" // or json
}
```
`destination` is `stderr`, or `windows_event_log` (the default when running as a Windows service; startup fails if set on other platforms). `write_to` tees Alloy's own log entries to `loki.*` receivers, such as `loki.write.default.receiver`.

Retrieving logs: `journalctl -u alloy` (systemd), `docker logs CONTAINER_ID`, Windows Event Viewer for services. Started directly, Alloy writes to stderr.

## Normal messages
`starting controller`, `starting server`, `configuration loaded`, `module content loaded`, `started scheduled components`, and cluster messages such as `starting cluster node`, `discovered peers`, `rejoining peers`, `minimum cluster size reached, marking cluster as ready to admit traffic`. Expected warnings at startup: `failed to get peers to join at startup; will create a new cluster`, `failed to resolve provided join address`.

Needs attention: `failed to bootstrap a fresh cluster with no peers` (for example address in use), `failed to rejoin list of peers` and `failed to refresh list of peers`. The warning `deadline passed, marking cluster as ready to admit traffic` appears when the wait timeout passes before the minimum cluster size is met.

## Cluster symptoms
- **Not converging**: usually network connectivity; compare each peer's UI.
- **Split brain**: nodes think they are alone; check join address format and reachability.
- **Configuration drift**: all nodes need the same config at roughly the same time; check reload logs and the graph page.
- **Name conflicts**: node names must be unique; conflicting nodes are rejected.
- **Stuck terminating**: verify on the clustering page that the process is really gone.
Missing metrics may be a scrape or discovery problem rather than a clustering one.

## Checked

2026-11-08. Read in full the raw Alloy docs pages behind both cited URLs (docs/sources/troubleshoot/debug.md and docs/sources/reference/config-blocks/logging.md): logging arguments and defaults, destination rules, retrieve-logs commands, the message lists and the cluster symptoms. Moved the deadline-passed message out of the needs-attention list, since the page shows it under cluster size management.

Method: documentation only; no commands were run.
