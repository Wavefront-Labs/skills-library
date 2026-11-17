---
id: computing-software.cloud-infrastructure-engineering.aws.listing-applied-vs-default-service-quotas
name: listing-applied-vs-default-service-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, list-service-quotas, applied-quota, quota-codes, usage-metrics, quota-audit]
level: practitioner
status: docs-checked
description: "Audit quotas with the Service Quotas CLI: find quota codes, compare applied vs default values, read usage via CloudWatch, and export across regions and accounts."
sources: ["https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html", "https://docs.aws.amazon.com/cli/latest/reference/service-quotas/index.html", "https://docs.aws.amazon.com/servicequotas/latest/userguide/configure-cloudwatch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing applied vs default service quotas

## 1. Find the service and quota codes
```bash
aws service-quotas list-services --query 'Services[?contains(ServiceName,`Lambda`)]'
aws service-quotas list-aws-default-service-quotas --service-code lambda \
  --query 'Quotas[].{code:QuotaCode,name:QuotaName,default:Value,adjustable:Adjustable}' --output table
```
Quota codes (the `L-...` values in `QuotaCode`) are what requests and alarms use; look them
up with the commands above rather than hard-coding them from memory.

## 2. Applied (account-specific) values
```bash
aws service-quotas list-service-quotas --service-code ec2 \
  --query 'Quotas[].{code:QuotaCode,name:QuotaName,value:Value,adj:Adjustable,global:GlobalQuota}' --output table
aws service-quotas get-service-quota --service-code lambda --quota-code <QUOTA_CODE>
aws service-quotas get-aws-default-service-quota --service-code lambda --quota-code <QUOTA_CODE>
```
`list-service-quotas` returns the **applied** value for your account. For some quotas only
the default is available; if the applied value is not available the quota is not returned
(ask Support for it). Pass `--quota-applied-at-level ACCOUNT`, `RESOURCE` or `ALL` to choose
account-level, resource-level or all applied values. The account's applied value can be lower
than the AWS default for a recently created or minimally used account.

## 3. Usage
Quotas that support it return a `UsageMetric` (CloudWatch metric identifiers) from
`get-service-quota`; read the namespace, metric name and dimensions from that output:
```bash
aws service-quotas get-service-quota --service-code ec2 --quota-code <QUOTA_CODE> \
  --query 'Quota.UsageMetric'
```
Graph usage / quota with CloudWatch metric math `SERVICE_QUOTA(m1)` (m1 must be a usage metric):
```
e1 = 100 * m1 / SERVICE_QUOTA(m1)
```
and alarm at a threshold you choose (for example 80%).

## 4. Across regions and accounts
```bash
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  v=$(aws service-quotas get-service-quota --region $r --service-code ec2 --quota-code <QUOTA_CODE> --query Quota.Value --output text 2>/dev/null)
  echo "$r $v"
done
```
For many accounts, run the same loop through a cross-account role from a tooling account.

## 5. Request history
```bash
aws service-quotas list-requested-service-quota-change-history --service-code ec2 \
  --query 'RequestedQuotas[].{code:QuotaCode,desired:DesiredValue,status:Status,created:Created}'
```
Statuses: `PENDING`, `CASE_OPENED`, `APPROVED`, `DENIED`, `CASE_CLOSED`, `NOT_APPROVED`, `INVALID_REQUEST`.

## Gotchas
- Quotas are per region unless `GlobalQuota` is true.
- Some limits are not in Service Quotas; check the individual service guides.

## Verify
- [ ] Inventory of critical quotas with applied value, usage and headroom per region.
- [ ] Usage alarms at 80% on quotas with usage metrics.
- [ ] Request history reviewed; pending increases tracked.

## Checked

2026-10-28. Confirmed against the Service Quotas user guide (viewing default and applied values, QuotaAppliedAtLevel ACCOUNT/RESOURCE/ALL, applied value may be lower for new accounts, quotas without applied values not returned), the CloudWatch metric math page (SERVICE_QUOTA function) and the service-quotas botocore model (RequestStatus enum, GlobalQuota). Removed (unconfirmed): hard-coded quota codes, the AWS/Usage namespace and example usage-metric dimensions, the list of global quotas, Trusted Advisor and Quota Monitor suggestions. Read end to end.

Method: documentation only; no commands were run.
