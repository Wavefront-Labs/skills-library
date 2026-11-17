---
id: computing-software.cloud-infrastructure-engineering.netdata.streaming-troubleshoot-logs
name: streaming-troubleshoot-logs
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, journalctl, message-id, streaming-logs]
level: practitioner
status: docs-checked
description: "Diagnose Parent-Child streaming problems by filtering Netdata journald logs on the connection MESSAGE_ID values, in the Logs tab or with journalctl."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Netdata logs to systemd-journald by default, so streaming problems appear there.

UI: open the Logs tab and filter the `MESSAGE_ID` field for "Netdata connection from child" (Parents) and "Netdata connection to parent" (Children).

Terminal on a Parent:

```
journalctl -r --namespace=netdata MESSAGE_ID=ed4cdb8f1beb4ad3b57cb3cae2d162fa
```

Terminal on a Child:

```
journalctl -r --namespace=netdata MESSAGE_ID=6e2e3839067648968b646045dbf28d66
```

Checklist:
- API key in the Child `[stream]` matches the `[API_KEY]` section name on the Parent, which must have `enabled = yes`.
- `destination` is `PARENT_HOSTNAME_OR_IP:19999`; for TLS the docs append `:SSL` to the destination (their example is `203.0.113.0:SSL`).
- Netdata restarted after saving `stream.conf` (and both nodes restarted for TLS).
- Replication progress: use the `Netdata-streaming` Function under the Live tab, or `http://agent-ip:19999/api/v2/node_instances` on both sides.

## Checked

2026-11-04. Confirmed against the Netdata metrics centralization configuration page: journald as the default log target, the Logs tab MESSAGE_ID names, both journalctl commands and IDs, the API key and enabled = yes sections, the destination format with port and :SSL, and the restart notes. The Netdata-streaming Function and node_instances endpoint are from the Replication of Past Samples page. Removed the closing gotcha about logs elsewhere, which no page states.

Method: documentation only; no commands were run.
