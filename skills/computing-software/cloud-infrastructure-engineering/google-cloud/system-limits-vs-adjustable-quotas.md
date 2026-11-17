---
id: computing-software.cloud-infrastructure-engineering.google-cloud.system-limits-vs-adjustable-quotas
name: system-limits-vs-adjustable-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, quotas, system-limits, non-adjustable-limits, architecture-limits, design-constraints]
level: practitioner
status: docs-checked
description: "Distinguish Google Cloud system limits that cannot be raised from adjustable quotas, find them per product, and design around the ones that commonly block architectures."
sources: ["https://cloud.google.com/docs/quotas/overview", "https://cloud.google.com/vpc/docs/quota", "https://cloud.google.com/kubernetes-engine/quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System limits vs adjustable quotas

**Quotas** are allowances you can ask to raise: the Cloud Quotas system lets you request a change
to a quota value. Most adjustment requests are evaluated by automated systems; requests that do
not meet the criteria are denied, and using more resources can cost more.
**System limits** are fixed constraints that cannot be increased or decreased. Each product has
its own "quotas and limits" page.

## Limits that commonly shape designs
| Area | Limit (check current docs) | Design response |
|---|---|---|
| VPC | Peerings per VPC network is a quota; per-peering-group quotas use an effective limit across directly connected peers | Shared VPC or a hub instead of a mesh of peerings |
| VPC | Maximum secondary IP ranges per subnet is a system limit that cannot be increased (VPC quota page) | Plan IP space up front; use additional ranges or subnets |
| VPC | Subnet ranges per network count primary, secondary and IPv6 ranges | Budget ranges before adding pod/service ranges |
| GKE | Pods per node is set dynamically within a range (GKE quotas page) | Multiple clusters, fleet |
| Other products | Read each product's limits page: IAM, Cloud Run, Cloud Storage, Pub/Sub, BigQuery and labels each have fixed limits | Capture the ones you depend on in the design |

## How to check fast
Use the Quotas page in the console (or the Cloud Quotas API) for adjustable quotas. System limits
are only in the docs; capture the ones your design depends on in the architecture decision
record with the doc link and date checked.

## Gotchas
- Some VPC limits are per peering group and have an effective limit that depends on the peers; read the VPC quota page section on effective limits.
- Limits change; re-check during design reviews instead of trusting memory.
- Hitting a limit late often forces re-architecture; validate in design phase with a load test.

## Verify
- [ ] Architecture review lists every relevant system limit with headroom calculation.

## Checked
2026-10-31. Confirmed against the Cloud Quotas overview (quota adjustment, automated evaluation, system limits cannot be changed), the VPC quotas and limits page (peerings per VPC network quota, per-peering-group effective limits, secondary ranges per subnet cannot be increased, subnet ranges count) and the GKE quotas page (pods per node set dynamically). Removed unconfirmed figures for IAM, Cloud Run, Cloud Storage, Pub/Sub, BigQuery and label limits, the transitive-peering and firewall rows, the org policy row, the `gcloud compute project-info describe` quota command and the "Adjustable: No" note, because those pages were not fetched or did not state them.
Method: documentation only; no commands were run.
