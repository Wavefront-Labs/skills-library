---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cloud-quota-management
name: cloud-quota-management
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [quota-management, cloud-quota-requests, capacity-planning, service-quotas, gcp-quotas, azure-quotas]
level: practitioner
status: docs-checked
description: "Treat cloud quotas as capacity: inventory limits per region, monitor usage vs quota, request increases ahead of launches and failover, and alert before quota blocks scaling."
sources: ["https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html", "https://cloud.google.com/docs/quotas/view-manage", "https://learn.microsoft.com/en-us/azure/quotas/quotas-overview", "https://sre.google/workbook/managing-load/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud quota management

In the cloud, capacity you cannot get is capacity you do not have. Quotas (vCPUs per region, IPs, load
balancers, GPUs, API rate limits) silently cap autoscaling and failover. Many outages are "the region
failed over and the other region hit its CPU quota".

## Inventory
List quotas that bound your critical paths, per region and account/project:
```bash
# AWS
aws service-quotas list-service-quotas --service-code ec2 --region <REGION>
aws service-quotas get-service-quota --service-code ec2 --quota-code <QUOTA_CODE>
# GCP
gcloud compute regions describe europe-west1 --format="table(quotas.metric,quotas.limit,quotas.usage)"
# Azure
az vm list-usage --location westeurope -o table
```

## Size quotas for failover, not steady state
```
required_quota(region) = peak_usage(region) + failover_share_from_other_regions + deploy_surge
```
Rolling deploys with a surge setting need extra capacity temporarily. If region B absorbs region A's traffic, B's
quota must cover both.

## Monitoring
- AWS: Service Quotas user guide covers viewing and managing quotas per account and Region.
- GCP: the Quotas page has usage charts and quota alerts (Set up quota alerts and monitoring).
- Azure: the Quotas page lets you monitor and create alerts when usage reaches a threshold you set.
- Set the alert threshold early enough to leave lead time for an increase.

## Requests
```bash
aws service-quotas request-service-quota-increase --service-code ec2 --quota-code <QUOTA_CODE> --desired-value <VALUE>
```
- Increases are not instant and are not guaranteed; file well before launches (part of
  `organic-and-inorganic-demand-planning`).
- Keep quota values in IaC or a tracked register so new accounts/projects get the same limits.

## Gotchas
- Quotas apply per account or per Region (AWS: check each quota's description); check yours per scope.
- API rate limits (e.g. control-plane calls) can block autoscaling during large scale events; check them too.

## Verify
- [ ] Quota register with usage, limit and failover requirement per region.
- [ ] Usage alerts exist and have fired in a test.

## Checked
2026-11-01. Commands checked against the AWS (botocore), gcloud and az references. Confirmed in the AWS Service Quotas user guide (quotas are per account or per Region), the Google Cloud quotas view-and-manage page (charts, alerts) and the Azure quotas overview (usage alerts). Removed: quota code and name, metric names and CloudWatch math, Trusted Advisor, alert percentages, surge percentage, increase timing, stockout statement.
Method: documentation only; no commands were run.
