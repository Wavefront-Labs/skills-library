---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.service-quotas
name: service-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, service-quotas, service-limits, quota-monitoring, quota-increase, api-rate-limits, capacity-headroom, dr-region-quotas]
level: practitioner
status: docs-checked
description: "Manage cloud quotas as a reliability risk: hard vs soft limits, utilisation monitoring, raising ahead of growth and failover, DR-region quotas, API rate limits."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/manage-service-quotas-and-constraints.html", "https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html", "https://learn.microsoft.com/azure/quotas/quotas-overview", "https://cloud.google.com/docs/quotas/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service quotas and limits management

Quota exhaustion looks like an outage: autoscaling can't add instances, failover region can't
start capacity, and deploys fail with a quota error.

## Steps
1. **Inventory** quotas relevant per workload: vCPU per instance family/region, IPs per subnet
   (subnet sizing is a hard limit), load balancers, ENIs, Lambda concurrency, API Gateway
   throttles, KMS request rates, DynamoDB table throughput, managed DB instances, Kubernetes
   pods per node (CNI IP limits).
2. Distinguish **adjustable** (request increase) from **hard** limits (design around them, e.g.
   with sharding or multiple accounts).
3. **Monitor utilisation**: AWS Service Quotas (its Automatic Management feature can notify you before
   quotas run out); the Azure Quotas page can create alerts when usage reaches a threshold you set;
   in Google Cloud use the quota adjuster or alerting on quota usage. Pick an alert threshold that leaves time to raise the limit.
4. **Raise ahead**: before launches, migrations and seasonal peaks, since approval is not instant.
5. **DR and failover regions** need the same quotas as primary — often forgotten until failover.
6. **New accounts** can start with lower quotas (the Lambda page says AWS raises them with usage) — build quota requests into account vending.
7. API rate limits (control plane) can block deploys at scale; spread calls, use backoff.

## Checked
2026-10-28. Confirmed: AWS Service Quotas intro (default versus applied quotas, Automatic Management notifications), Azure Quotas overview (adjustable versus non-adjustable quotas, usage alerts at thresholds), Google Cloud quotas overview (project, folder and organisation scope; global, regional and zonal; quota adjuster), the AWS reliability pillar practice on keeping a gap between quotas and peak usage including failover, and the Lambda page on reduced new-account quotas. Removed: the `LimitExceeded` code, the Google metric name, the 80% threshold, Trusted Advisor, request templates and the "days" claim (not in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Quota dashboard with usage alarms for top constraints per region.
- [ ] DR region quotas match primary.
- [ ] Load-test or launch checklist includes quota check.
