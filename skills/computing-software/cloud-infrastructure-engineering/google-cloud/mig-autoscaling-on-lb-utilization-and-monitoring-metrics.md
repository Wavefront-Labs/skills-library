---
id: computing-software.cloud-infrastructure-engineering.google-cloud.mig-autoscaling-on-lb-utilization-and-monitoring-metrics
name: mig-autoscaling-on-lb-utilization-and-monitoring-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, managed-instance-groups, autoscaling-custom-metrics, lb-utilization-autoscaling, pubsub-backlog-autoscaling, autoscaler-signals]
level: practitioner
status: docs-checked
description: "Configure MIG autoscalers on load balancer serving capacity or Cloud Monitoring metrics (per-instance or per-group, e.g. Pub/Sub backlog), combine signals, and avoid flapping."
sources: ["https://cloud.google.com/compute/docs/autoscaler/scaling-load-balancing", "https://cloud.google.com/compute/docs/autoscaler/scaling-cloud-monitoring-metrics", "https://cloud.google.com/compute/docs/autoscaler/multiple-signals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIG autoscaling on LB utilization and Monitoring metrics

## Load balancing serving capacity
Backend service defines capacity (`--balancing-mode=RATE --max-rate-per-instance=100` or
`UTILIZATION --max-utilization=0.8`); autoscaler targets a fraction of it:
```bash
gcloud compute instance-groups managed set-autoscaling web-mig --region=<R> \
  --min-num-replicas=3 --max-num-replicas=30 --target-load-balancing-utilization=0.7 --cool-down-period=90
```
Supported only for external Application Load Balancers and internal Application Load Balancers; other load balancer types are not supported. The backend needs a balancing mode with a maximum (UTILIZATION or RATE); regional MIGs do not support a maximum rate per group.

## Cloud Monitoring metric, per-instance
```bash
gcloud compute instance-groups managed set-autoscaling worker-mig --region=<R> \
  --min-num-replicas=1 --max-num-replicas=50 \
  --custom-metric-utilization=metric=agent.googleapis.com/memory/percent_used,utilization-target=70,utilization-target-type=GAUGE
```
A per-instance metric is written against `resource.type` `gce_instance` and is matched to each VM by its `instance_id`; `agent.googleapis.com/memory/percent_used` is an Ops Agent metric.

## Per-group metric (queue depth)
```bash
gcloud compute instance-groups managed set-autoscaling worker-mig --region=<R> \
  --min-num-replicas=0 --max-num-replicas=50 \
  --update-stackdriver-metric=pubsub.googleapis.com/subscription/num_undelivered_messages \
  --stackdriver-metric-filter='resource.type="pubsub_subscription" AND resource.labels.subscription_id="jobs"' \
  --stackdriver-metric-single-instance-assignment=200
```
`single-instance-assignment=200` = each VM handles 200 backlog messages. A MIG can scale in to zero when you set the minimum to 0 and use a per-group metric with a single instance assignment (per-instance metrics cannot).

## Multiple signals
Autoscaler computes a recommendation per signal and uses the **largest**. Combining CPU + LB
utilization is common. Scale-in uses a stabilization period (default 10 minutes, configurable) and any scale-in controls.

## Gotchas
- `cool-down-period` (the initialization period, default 60 s) must cover boot + app warmup or it overscales.
- For rate-based (delta) metrics use `utilization-target-type=DELTA_PER_SECOND` or `DELTA_PER_MINUTE`; `GAUGE` averages the value.

## Verify
- [ ] `gcloud compute instance-groups managed describe worker-mig --region=<R> --format='value(status.autoscaler)'` returns the autoscaler URL, and that autoscaler's `recommendedSize` follows the backlog.

## Checked

Checked 2026-10-27 against Autoscaling groups of instances, Scale based on load balancing, Scale based on Cloud Monitoring metrics, Scale based on multiple signals and the gcloud reference for set-autoscaling. Fixed: load-balancer scaling supports only external and internal Application Load Balancers; the verification command no longer expects an ACTIVE value in status.autoscaler (it holds the autoscaler URL). Confirmed the largest-signal rule, 10-minute default stabilization period, 60-second default initialization period, scale to zero with a per-group metric and single instance assignment, and the target types GAUGE, DELTA_PER_SECOND and DELTA_PER_MINUTE.

Method: documentation only; no commands were run.
