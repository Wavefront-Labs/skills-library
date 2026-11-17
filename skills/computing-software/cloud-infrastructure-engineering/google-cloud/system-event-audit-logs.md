---
id: computing-software.cloud-infrastructure-engineering.google-cloud.system-event-audit-logs
name: system-event-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-audit-logs, system-event-audit-logs, live-migration-events, preemption-logs, autoscaler-events, host-maintenance]
level: practitioner
status: docs-checked
description: "Use System Event audit logs to see Google-initiated Compute Engine events such as preemptions, host errors and host maintenance, and build a log-based metric to alert on them."
sources: ["https://cloud.google.com/logging/docs/audit", "https://cloud.google.com/compute/docs/logging/audit-logging", "https://cloud.google.com/compute/docs/instances/host-maintenance-overview", "https://cloud.google.com/logging/quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System Event audit logs

System Event logs record actions taken **by Google systems**, not users. They are stored in the
`_Required` bucket (400 days, not configurable) and you cannot prevent them being stored. Log name:
`projects/<P>/logs/cloudaudit.googleapis.com%2Fsystem_event`.

## Useful queries
```
logName:"cloudaudit.googleapis.com%2Fsystem_event"
protoPayload.methodName=("compute.instances.preempted" OR "compute.instances.hostError"
  OR "compute.instances.migrateOnHostMaintenance" OR "compute.instances.automaticRestart"
  OR "compute.instances.guestTerminate" OR "compute.instances.terminateOnHostMaintenance")
```
```bash
gcloud logging read 'logName:"system_event" AND protoPayload.methodName="compute.instances.preempted"' \
  --freshness=7d --format="table(timestamp,protoPayload.resourceName)"
```
- `compute.instances.hostError` means a hardware or software issue on the physical host or data-centre infrastructure affected your instance (see the host maintenance overview).
- The Compute Engine system-event page lists the method names Google writes, including `compute.instances.guestTerminate`, `compute.instances.preempted` and `compute.instances.terminateOnHostMaintenance`.

## Alerting
Log-based metric, then an alert policy on it:
```bash
gcloud logging metrics create vm_host_errors \
  --log-filter='logName:"system_event" AND protoPayload.methodName="compute.instances.hostError"'
```
Pick the threshold from your workload: any occurrence for stateful VMs; a rate for Spot fleets.

## Gotchas
- Notifications of upcoming maintenance (on machine families that support maintenance preferences) come through Cloud Logging, the instance's metadata server, and `gcloud compute instances describe`; see the host maintenance overview.
- System Event logs cannot be disabled or excluded from `_Required`.

## Verify
- [ ] The query returns events for your project over a window that included a known maintenance or preemption event.

## Checked
2026-10-28. Confirmed against the Cloud Audit Logs overview, the Compute Engine system event audit log page (method names), the host maintenance overview (`hostError`, `migrateOnHostMaintenance`, `automaticRestart`, notification channels) and the Logging quotas page (400 days in `_Required`). gcloud commands checked with check_commands.py. Removed: GKE auto-upgrade and MIG autohealing claims, "live migrations are silent", the `maintenance-event` and `upcomingMaintenance` field names, the claim that `simulate-maintenance-event` produces an event.
Method: documentation only; no commands were run.
