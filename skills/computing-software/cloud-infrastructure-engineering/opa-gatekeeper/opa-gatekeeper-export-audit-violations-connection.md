---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-export-audit-violations-connection
name: opa-gatekeeper-export-audit-violations-connection
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, export, connection, dapr, disk, enable-violation-export, audit-channel, pubsub]
level: sme
status: docs-checked
description: "Export Gatekeeper audit violations to a message system with a Connection resource and the dapr or disk driver, avoiding constraint status limits."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/export.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper export audit violations connection

Audit export (alpha, v3.13+, formerly "consuming violations using Pubsub") pushes violations to a backend so you are not bound by the per-constraint status cap.

On the audit deployment set `--enable-violation-export=true`, plus `--audit-connection` (default `audit-connection`) and `--audit-channel` (default `audit-channel`). Create a `Connection` custom resource whose `spec` has `driver` (valid values `dapr` or `disk`) and a driver-specific `config` object, for example which pubsub component or queue to send to. Dapr exports with its pubsub model; Disk writes to the file system.

The Connection `status.byPod` reports per pod: `connectionErrors` (up to 500, with type such as `UpsertConnection` and message) and `publishStatuses` grouped by `source` (`audit` or `webhook`) with `active`, `lastAttemptTime`, `lastSuccessTime` and `errors` (up to 500). Each publisher only replaces its own entry.

Limitations: export is best effort with a risk of dropped messages (more so over a network backend), and it adds a dependency on the backend system. Compare with the other reading methods in the audit guide.

## Checked

2026-11-04. Confirmed against export.md (Connection, drivers, status.byPod) and audit.md (limitations of exporting violations). Removed or corrected: the count of other reading methods.

Method: documentation only; no commands were run.
