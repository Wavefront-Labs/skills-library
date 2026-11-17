---
id: computing-software.cloud-infrastructure-engineering.netdata.log-centralization-design
name: log-centralization-design
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, log-centralization, journal-remote, windows-event-forwarding]
level: advanced
status: docs-checked
description: "Choose a log transport for Netdata: journal-remote and upload, Windows Event Forwarding or OpenTelemetry, with where each appears and when no central point is needed."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/logs-centralization-points-with-systemd-journald/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Netdata does not need a centralization point; it reads each node's logs where they already are.

| Transport | Platform | Explorable under |
|---|---|---|
| `systemd-journal-remote` on the central point, `systemd-journal-upload` on production systems | Linux | `systemd-journal` |
| Windows Event Forwarding | Windows | `windows-events` |
| OpenTelemetry (OTLP over gRPC or HTTP) | Any | `otel-logs` |

Notes:
- Journal and WEF data stays in OS-native format, so `journalctl`, Event Viewer and SIEM agents on the aggregation point still read it.
- OTLP is the path into Netdata's own log store, with its own retention and optional `fs`/`s3` archiving. Journal and WEF data is not stored that way.
- Linked guides cover passive centralization with and without encryption (self-signed certificates), an active journal source, journal namespaces and Forward Secure Sealing.

Design rules:
- Logs and metrics centralization points need not be the same, though unified points are recommended unless operations or regulation say otherwise.
- The logs point may or may not also be a metrics Parent.
- Netdata Cloud unifies access, not the log streams: you pick one node or aggregation point and the query runs on its data.
- Decide where each system's logs converge, since an aggregation point combines its senders into one view.

## Checked

2026-11-04. Confirmed against the Netdata Logs Centralization Points page: no centralization point needed, the transport table with sources, native-format readability, OTLP as the route into Netdata's own store with fs and s3 archiving, the linked guides, the unified-points recommendation, Cloud unifying access only, and the choosing section. Nothing removed.

Method: documentation only; no commands were run.
