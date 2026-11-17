---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-export-admission-violations-disk
name: opa-gatekeeper-export-admission-violations-disk
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, export, admission-export, disk-driver, queue-limits, jsonl, best-effort]
level: sme
status: docs-checked
description: "Enable alpha admission-violation export (v3.24+) on the disk driver and understand its fixed queue, segment and retention limits and best-effort delivery."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/export.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper export admission violations disk

Admission export is independent from audit export and off by default. Set `--enable-admission-violation-export=true` on the controller-manager deployment (enabling audit export does not enable it). Routing uses the same `--audit-connection` and `--audit-channel` flags. Only the disk driver is supported: the Helm chart rejects `enableAdmissionViolationExport: true` unless `exportBackend: disk`. A reader sidecar is disabled by default; configure a production reader or enable the demo reader.

Files are newline-delimited JSON, named `admission-<timestamp>-<random>.log` (audit files use `<audit-run-id>.log`), with in-progress `.open` segments. Messages use `eventType: violation_admission` and include operation, resource, dry-run state and the requesting user identity.

Fixed alpha limits per controller-manager pod: queue 1,024 messages and 16 MiB; batch up to 64 records; record 64 KiB; segment 1 MiB, 1,000 records or 1 minute; spool 20 completed segments, 20 MiB, 24 hours; 16 MiB free-space reserve.

Delivery is best effort and never delays the admission response. Messages are dropped on encode failure, full queues or shutdown (5 seconds of drain), and failed publishes are not retried. Dropped reasons are reported as `marshal_error`, `message_too_large`, `queue_bytes_full`, `queue_full` or `shutdown` in `gatekeeper_admission_export_dropped_count`. Default `emptyDir` volumes lose unconsumed files when the pod is deleted.

## Checked

2026-11-04. Confirmed against export.md (admission export, default queue and disk limits, delivery behavior). Removed or corrected: nothing.

Method: documentation only; no commands were run.
