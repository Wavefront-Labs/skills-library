---
id: computing-software.cloud-infrastructure-engineering.google-cloud.live-migration-and-host-maintenance-policies
name: live-migration-and-host-maintenance-policies
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, live-migration, on-host-maintenance, availability-policy, maintenance-event, simulate-maintenance]
level: practitioner
status: docs-checked
description: "Control what happens to VMs during host maintenance and failures: MIGRATE vs TERMINATE, restart-on-failure, maintenance-event notices, simulation and on-demand maintenance."
sources: ["https://cloud.google.com/compute/docs/instances/live-migration-process", "https://cloud.google.com/compute/docs/instances/setting-vm-host-options", "https://cloud.google.com/compute/docs/instances/simulating-host-maintenance", "https://cloud.google.com/compute/docs/instances/monitor-plan-host-maintenance-event"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live migration and host maintenance policies

## 1. Availability policy
| Setting | Values | Default |
|---|---|---|
| `onHostMaintenance` | `MIGRATE` (live-migrate the VM) or `TERMINATE` (stop, then restart if allowed) | MIGRATE for standard VMs; some machine families only support TERMINATE, so check your machine type's page |
| `automaticRestart` | restart after host failure or terminate-on-maintenance | standard VMs only; cannot be set on Spot or preemptible |
| Spot / preemptible | TERMINATE is the default and only option, no automatic restart | |
```bash
gcloud compute instances set-scheduling db-1 --zone=<Z> --maintenance-policy=MIGRATE --restart-on-failure
gcloud compute instances describe db-1 --zone=<Z> --format='yaml(scheduling)'
```
Host error detection: `--host-error-timeout-seconds` (API field `hostErrorTimeoutSeconds`, 90 to 330 in steps of 30) sets the host error timeout; if unset, the default recovery behaviour applies.

## 2. Get notice inside the VM
```bash
curl -s -H 'Metadata-Flavor: Google' \
 'http://metadata.google.internal/computeMetadata/v1/instance/maintenance-event?wait_for_change=true'
# NONE normally; becomes MIGRATE_ON_HOST_MAINTENANCE when a live migration starts
```
Drain the node (stop accepting work, checkpoint, fail over a DB primary) when it changes. When a
VM is terminated for maintenance, Compute Engine waits 60 s for a clean shutdown, then forces it.
Scheduled maintenance is visible in advance on the VM
(`gcloud compute instances describe db-1 --zone=<Z> --format='yaml(resourceStatus.upcomingMaintenance)'`)
and can be started early with `gcloud compute instances perform-maintenance db-1 --zone=<Z>`.

## 3. Test it
```bash
gcloud compute instances simulate-maintenance-event db-1 --zone=<Z>
```
Watch application latency and logs; system event log shows
`compute.instances.migrateOnHostMaintenance` (or `terminateOnHostMaintenance`).

## Gotchas
- Live migration briefly pauses the VM (usually sub-second); timing-sensitive clustering (Pacemaker, short heartbeat DB clusters) may fail over spuriously — lengthen timeouts.
- `automaticRestart=false` + TERMINATE means a maintenance event leaves the VM stopped until someone starts it.
- After a host error or maintenance event Compute Engine tries to recover Local SSD data; `--local-ssd-recovery-timeout` bounds how long it tries, and data is lost if recovery exceeds it. Keep replicas.
- Sole-tenant node groups have their own `--maintenance-policy` (default, restart-in-place, migrate-within-node-group).

## Verify
- [ ] Simulated maintenance on a staging replica causes no failed requests.
- [ ] Alert exists on the `compute.instances.terminateOnHostMaintenance` and `compute.instances.upcomingMaintenance` system events.

## Checked

Checked 2026-10-27 against Set the host maintenance policy, Live migration process, Simulate a host maintenance event, Monitor and plan for a host maintenance event, the gcloud reference for instances set-scheduling and sole-tenancy node-groups create, and the Compute Engine v1 API discovery document. Confirmed: onHostMaintenance MIGRATE or TERMINATE, Spot and preemptible VMs are TERMINATE only with no automatic restart, hostErrorTimeoutSeconds 90 to 330 in steps of 30, the 60-second clean-shutdown wait on terminate, disruption typically well under a second, the system event names and the node-group maintenance policies. Fixed: upcomingMaintenance lives under resourceStatus; removed the TERMINATE_ON_HOST_MAINTENANCE value, the 60-second notice claim, the GPU and TPU forced-terminate claim and the hostError event name, none of which the documentation supports.

Method: documentation only; no commands were run.
