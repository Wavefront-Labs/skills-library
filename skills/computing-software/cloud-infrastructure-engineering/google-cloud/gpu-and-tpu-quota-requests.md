---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gpu-and-tpu-quota-requests
name: gpu-and-tpu-quota-requests
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, quotas, gpu-quota, accelerator-quota, tpu, cloud-quotas-api, dynamic-workload-scheduler]
level: practitioner
status: docs-checked
description: "Get GPU and TPU capacity: find the right regional, global and preemptible quota names, file Cloud Quotas preferences, and fall back to reservations."
sources: ["https://cloud.google.com/compute/resource-usage#gpu_quota", "https://cloud.google.com/docs/quotas/view-manage", "https://cloud.google.com/sdk/gcloud/reference/beta/quotas/preferences/create", "https://cloud.google.com/tpu/docs/quota"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU and TPU quota requests

## 1. Know which quotas gate you
A GPU VM needs **all** of:
- a regional quota per GPU model in each region. Names in the GPU quota table include `NVIDIA_A100_80GB_GPUS`, `NVIDIA_A100_GPUS`, `COMMITTED_NVIDIA_*_GPUS` (committed use) and `PREEMPTIBLE_NVIDIA_*_GPUS` (Spot); for H100 and L4 the table lists the family form `GPU_FAMILY:NVIDIA_H100` / `GPU_FAMILY:NVIDIA_L4`, so look the exact quota up in the Compute Engine "GPU quota" table for your machine series;
- the global "GPUs (all regions)" quota, which new accounts and projects have and which counts GPUs of all types in all regions: request it alongside the per-model quota;
- regular CPU and disk quotas in the region (new projects can also have a global "CPUs (All Regions)" quota).
```bash
gcloud compute regions describe us-central1 --project=<P> --format=json   # quotas list
gcloud beta quotas info list --service=compute.googleapis.com --project=<P> --format=json
```
Cloud TPU API quotas are per zone and per TPU version, split into on-demand and preemptible (spot) quota, and are measured in cores. If you manage TPUs through GKE or Compute Engine, you use Compute Engine API quota instead, which is separate. Requests for TPU v4 quota in us-central2-b always need manual approval.

## 2. Request
```bash
gcloud beta quotas preferences create --project=<P> --service=compute.googleapis.com \
  --quota-id=<QUOTA_ID_FROM_INFO_LIST> --dimensions=region=us-central1,gpu_family=NVIDIA_L4 \
  --preferred-value=16 --email=<CONTACT_EMAIL> \
  --justification="<WORKLOAD, GPU COUNT, ZONES, LAUNCH DATE>"
gcloud beta quotas preferences describe <PREF_ID> --project=<P>
```
Use an `--email` whose account has quota update permission, or a request that needs more information is denied. Raise the global "GPUs (all regions)" quota in the same pass. For Cloud TPU API quota, requests below the auto-approve threshold on the TPU quota page are approved automatically; otherwise they are reviewed.

## 3. When quota is not the problem
Quota is not capacity: a zone can lack free GPUs even when quota is available.
- Spread across zones and regions.
- Use reservations for guaranteed capacity.
- Check the Compute Engine documentation for Dynamic Workload Scheduler options for your machine series.

## Gotchas
- Spot GPU usage counts against the `PREEMPTIBLE_NVIDIA_*` quotas, not the on-demand ones; request the right one.

## Verify
- [ ] `quotas preferences describe` shows the granted value you requested.

## Checked

2026-10-28. Confirmed against: the Compute Engine GPU quota table (quota name forms `NVIDIA_A100_*`, `COMMITTED_*`, `PREEMPTIBLE_*`, `GPU_FAMILY:` for H100 and L4; global GPU quota for new projects; request both per-model and all-regions quota), the Cloud TPU quotas page (zone and version quotas, on-demand versus preemptible, Compute Engine API quota is separate for GKE and Compute Engine, auto-approve thresholds, us-central2-b manual approval) and the `gcloud beta quotas preferences create` reference (flags, email requirement). Commands were checked with the command checker.

Removed: `GPUS_ALL_REGIONS` as a metric name and "often 0", the jq filters, the example numbers and dates, approval-strategy claims, the Dynamic Workload Scheduler mode details and runtime limit, the `ZONE_RESOURCE_POOL_EXHAUSTED` and `QUOTA_EXCEEDED` error claims, and the billing-account gotcha.

Method: documentation only; no commands were run.
