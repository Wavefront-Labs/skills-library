---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gce-autoscaling
name: gce-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, gce, managed-instance-groups, mig, regional-mig, instance-templates, autoscaler, cpu-utilization, load-balancing-utilization, cloud-monitoring-metrics, predictive-autoscaling, schedule-based-autoscaling, scale-in-controls, initialization-period, autohealing, health-checks, rolling-update, canary-update, max-surge, max-unavailable, spot-vms, stateful-mig, distribution-shape, standby-pool]
level: practitioner
status: docs-checked
description: "Run Compute Engine fleets on regional MIGs: instance templates, autoscaler signals and scale-in controls, autohealing, Spot VMs and rolling or canary updates."
sources: ["https://cloud.google.com/compute/docs/instance-groups", "https://cloud.google.com/compute/docs/autoscaler", "https://cloud.google.com/compute/docs/instance-groups/autohealing-instances-in-migs", "https://cloud.google.com/compute/docs/instance-groups/rolling-out-updates-to-managed-instance-groups", "https://cloud.google.com/compute/docs/instances/spot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCE autoscaling — regional MIGs that scale, heal and roll

**Goal:** a managed instance group (MIG) that survives a zone loss, scales on the right
signal without thrashing, recreates broken VMs on its own, and rolls out a new template
with a canary and no capacity dip.

## 1. Instance templates
- Templates are **immutable**: create a new one per change (`app-v42`), never edit.
  Prefer **regional** instance templates.
- Reference an image **family** (`--image-family=app --image-project=<PROJECT_ID>`) only if
  you accept that each new VM may pick a newer image; for controlled rollout pin the
  image name in the template.
- Dedicated service account with minimal roles, no external IP (use Cloud NAT), Shielded VM on,
  OS Login via metadata `enable-oslogin=TRUE`.
- Startup scripts must be idempotent and fast; bake software into the image.

## 2. Regional MIG shape
- `gcloud compute instance-groups managed create app-mig --region=<REGION> --template=app-v42 --size=3`.
- **Target distribution shape:** `EVEN` (default, strict balance), `BALANCED` (prefers balance,
  tolerates stockouts), `ANY` (go where capacity is — best for Spot and batch),
  `ANY_SINGLE_ZONE` for tightly-coupled batch.
- Turn off proactive redistribution only if instances must not be recreated for rebalancing.

## 3. Autoscaler signals
- **CPU utilisation** target (e.g. 0.6). Simple, works for CPU-bound services.
- **HTTP load-balancing utilisation** (fraction of the backend's configured max RPS/utilisation).
- **Cloud Monitoring metric** — per-instance (`agent.googleapis.com/...`) or per-group
  (e.g. Pub/Sub `subscription/num_undelivered_messages` with a single-instance assignment target).
- Multiple signals: autoscaler computes a recommendation per signal and uses the **largest**.
- **Predictive autoscaling** (works only with CPU utilization): forecasts from the MIG's load history (3 days of
  CPU-based autoscaling history first, up to 3 weeks used) and scales ahead for cyclic load. Useful when initialisation is long.
- **Schedule-based** scaling sets a minimum during known windows.

## 4. Stop thrashing
- **Initialization period** (formerly cool-down period; default 60 seconds): time a new VM needs to reach steady
  state; autoscaler ignores its usage meanwhile. Measure it — too short over-provisions.
- **Scale-in controls:** e.g. at most 2 VMs or 10 % per 10 min. Prevents a traffic dip
  dropping capacity you'll need back minutes later.
- The default stabilization period is 10 minutes (configurable) and applies only to scale-in decisions — scale-in is
  slow by design; size `min` for the floor you need, not for cost hopes. Scale-in controls: `--scale-in-control=max-scaled-in-replicas=2,time-window=600`.

## 5. Autohealing
- Attach a **separate health check** for autohealing (not just the LB one), with a
  conservative threshold (e.g. check every 10 s, unhealthy after 3-5 failures) and an
  **initial delay** ≥ boot-to-healthy time. Too aggressive = healthy VMs recreated during
  load spikes, which worsens the spike.
- Allow health-check source ranges `35.191.0.0/16`, `130.211.0.0/22` in the firewall.

## 6. Updates
```bash
gcloud compute instance-groups managed rolling-action start-update app-mig --region=<REGION> \
  --version=template=app-v42 --canary-version=template=app-v43,target-size=10% \
  --max-surge=3 --max-unavailable=0
```
- For regional MIGs the default `max-surge` is the number of zones (3 by default) and the default for zonal MIGs is 1;
  `max-unavailable=0` needs `max-surge` above 0 and keeps full capacity during proactive updates.
- Promote canary by re-running with only `--version=template=app-v43`. Roll back the same way.
- `--type=proactive` is the default; `--type=opportunistic` does not proactively replace VMs and applies the new template when VMs are created or deleted anyway.
- `--minimal-action=refresh|restart|replace` — `refresh` applies changes such as metadata without stopping VMs; if you omit it the MIG update policy value is used, else `replace`.

## 7. Spot and special cases
- Spot VMs (`--provisioning-model=SPOT`, `--instance-termination-action=DELETE`) get ~30 s
  preemption notice via metadata/ACPI; use a shutdown script to drain. Separate MIGs for
  Spot and standard, both behind the same backend service, give a reliable floor.
- **Stateful MIGs** preserve instance names, persistent disks, instance-specific metadata and IP addresses; see the stateful MIG page for its autoscaling section.

## Gotchas
- Autoscaler can't scale above `max` or regional quota (CPUs, IPs, Spot quota); check quota before a launch event.
- LB-utilisation signal needs a backend `balancingMode` with max RPS/utilisation set, else it can't compute.
- Mixing an image family with autohealing means a healed VM may run a different image than its siblings.
- Deleting a VM manually in a MIG just triggers recreation; use `delete-instances` or resize.

## Verify
- [ ] Regional MIG across ≥ 3 zones, immutable versioned templates, no external IPs.
- [ ] Load test: scale-out before latency SLO breach; scale-in controls prevent a sawtooth.
- [ ] Killing the app process on one VM triggers autohealing within the expected window, not before initial delay.
- [ ] Canary update at 10 % then full rollout completes with `max-unavailable=0` and no request errors.
- [ ] `list-errors` on the MIG shows no repeated quota or stockout failures.

## Checked

Checked 2026-10-27 against Autoscaling groups of instances, Predictive autoscaling, Rolling out updates to MIGs, About stateful MIGs and the gcloud reference for set-autoscaling and rolling-action start-update. Replaced prose titles in sources with real URLs. Fixed: predictive autoscaling works only with CPU utilization and needs 3 days of history, the default stabilization period (10 minutes, scale-in only), initialization period default (60 seconds), regional max-surge default (the number of zones), --type default proactive and --minimal-action semantics. Removed the unconfirmed standby pool and stateful autoscaling statements.

Method: documentation only; no commands were run.
