---
id: computing-software.cloud-infrastructure-engineering.google-cloud.quotas-and-quota-management
name: quotas-and-quota-management
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, quotas, quota-management, resource-exhausted, quota-increase, cloud-quotas-api, quota-adjuster, quota-alerts, capacity-planning]
level: practitioner
status: docs-checked
description: "Manage GCP quotas: tell rate from allocation quotas, request changes through the Cloud Quotas API, and alert on quota usage before CPUs, IPs or API calls run out."
sources: ["https://cloud.google.com/docs/quotas/overview", "https://cloud.google.com/docs/quotas/view-manage", "https://cloud.google.com/docs/quotas/quota-adjuster", "https://cloud.google.com/monitoring/alerts/using-quota-metrics", "https://cloud.google.com/sdk/gcloud/reference/beta/quotas/preferences/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quotas and quota management

**Goal:** no launch, migration or autoscaling event fails on `RESOURCE_EXHAUSTED`, and no runaway
job can consume an unbounded budget.

## 1. Two kinds
- **Rate quotas** restrict the rate at which you consume a resource over a time period, and reset
  automatically. Per-day quotas reset at midnight Pacific Time; per-minute quotas reset one minute
  after your first request, in a rolling window. Back off and retry when you hit one.
- **Allocation quotas** restrict how much of a resource Google Cloud allocates to you (for example the number of
  VMs in a project). Free resources or ask for an increase.

## 2. See what you have
```bash
gcloud compute regions describe europe-west1 --format='yaml(quotas)'   # compute, per region
gcloud compute project-info describe --format='yaml(quotas)'          # compute, global
gcloud alpha services quota list --service=run.googleapis.com --consumer=projects/<PROJECT_ID>   # alpha command
```
The console Quotas & System Limits page filters by service and metric. Monitoring metrics:
`serviceruntime.googleapis.com/quota/allocation/usage`, `.../quota/limit`,
`.../quota/rate/net_usage` and `.../quota/exceeded`.

## 3. Request a change
Console → Quotas → select → edit → value plus justification, or the Cloud Quotas API:
```bash
gcloud beta quotas preferences create --service=<SERVICE> --quota-id=<QUOTA_ID> \
  --preferred-value=<VALUE> --dimensions=region=<REGION> --project=<PROJECT_ID> \
  --justification="<REASON>" --email=<CONTACT_EMAIL>
```
`--email` should belong to an account with quota update permission, or a request that needs more
information is denied. You do not need a paid Customer Care plan to request an adjustment.
The **quota adjuster** observes consumption and proactively submits increase requests (typically
around 10-20%) when peak usage approaches the quota value; it needs enough usage history to predict.

## 4. Lower a quota
The same `quotas preferences create` command can set a lower `--preferred-value`. A reduction of
more than 10 percent needs `--allow-high-percentage-quota-decrease`, and going below current usage needs
`--allow-quota-decrease-below-usage`. A value of -1 means unlimited.

## 5. Alert before you hit it
Alert on `quota/allocation/usage` against `quota/limit` (a ratio threshold such as 0.8 is your
choice), and on `serviceruntime.googleapis.com/quota/exceeded` for quota errors. The
using-quota-metrics page has the exact filters for allocation and rate quotas.

## Verify
- [ ] Capacity plan lists CPU, IP, disk and load balancer quotas per region against projected peak.
- [ ] A test alert fires when a sandbox project's usage ratio passes the threshold.

## Checked

2026-10-28. Confirmed against: Cloud Quotas overview (allocation and rate quota definitions, reset behaviour, no paid support needed, adjuster needs usage history), the quota adjuster page (peak-usage check, typical 10-20% increase), the using-quota-metrics page (metric names `quota/allocation/usage`, `quota/limit`, `quota/rate/net_usage`, `quota/exceeded`), and the `gcloud beta quotas preferences create` reference (flags, -1 means unlimited, 10 percent decrease flag). `gcloud services quota list` exists only in the alpha track (command checker).

Removed: HTTP 429 and error-code mappings, zone stock-out and per-region claims, the quota ID and BigQuery override example (`gcloud services quota update` with metric and unit values not found in the pages read), approval-time and lead-time figures, new-project approval claims, the headroom percentage, and all gotchas.

Method: documentation only; no commands were run.
