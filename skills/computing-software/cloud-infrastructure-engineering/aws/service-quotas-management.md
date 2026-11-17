---
id: computing-software.cloud-infrastructure-engineering.aws.service-quotas-management
name: service-quotas-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, quotas, service-limits, limit-increase, quota-request-template, lambda-concurrency-limit, capacity-planning]
level: practitioner
status: docs-checked
description: "Manage AWS service quotas before they cause an outage: applied vs default values, adjustable quotas, CLI increase requests and organization request templates."
sources:
  - https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html
  - https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html
  - https://docs.aws.amazon.com/servicequotas/latest/userguide/organization-templates.html
  - https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service quotas — the outage that is a support ticket away

**Goal:** no scale-out, deployment or DR failover stops on a quota error; usage is tracked against quotas, increases are requested ahead of need, and new accounts start with sensible values.

## 1. Know the vocabulary
- Service Quotas shows the AWS **default** value and the **applied** value of a quota, plus utilization and whether the quota is **adjustable** (at account level or resource level).
- Your account's applied value can be lower than the AWS default if the account is new or lightly used.
- If the applied value or utilization is not available, the console shows "Not available"; request the applied value through Support Center.
- Lambda marks quotas as adjustable or not; adjustable ones are raised through Service Quotas. Account concurrent executions default to 1,000 per Region.

## 2. See and request
```bash
aws service-quotas list-service-quotas --service-code ec2
aws service-quotas request-service-quota-increase --service-code ec2 --quota-code <QUOTA_CODE> --desired-value <VALUE>
aws service-quotas list-requested-service-quota-change-history-by-quota --service-code ec2 --quota-code <QUOTA_CODE>
```
- Smaller increases are usually approved automatically; larger requests go to Support.
- **Request templates** let an organization pre-configure quota increases for new accounts; enable the template so every new account in the organization requests them ("Using Service Quotas request templates").
- Quotas not available in Service Quotas need an AWS Support case.

## 3. Plan ahead
- Quotas are per Region: raising one Region does nothing for your DR Region, so compare and raise DR-Region quotas before you need them.
- Before load tests or launches, list the quotas for each service involved and request increases early.
- Read the applied value instead of assuming a default; defaults change over time.

## Verify
- [ ] DR-Region quotas for critical services are at least production's (scripted comparison, re-run regularly).
- [ ] The organization request template is enabled and a freshly created account shows the raised values.
- [ ] Every critical quota has an owner who knows how to request an increase.

## Checked
2026-10-28. Confirmed on the Service Quotas User Guide pages "Viewing service quotas", "Requesting a quota increase" and "Using request templates", and the Lambda quotas page: default vs applied values, adjustable at account or resource level, new-account applied values, "Not available" display, small increases auto-approved and large ones sent to Support, request templates for new accounts, Lambda 1,000 default concurrency; `check_commands.py` accepted the three CLI commands.
Removed as unconfirmed: the table of default quota numbers (VPCs, EIPs, RDS, DynamoDB, CloudFormation, S3, ACM and others), the `AWS/Usage` metrics and `SERVICE_QUOTA()` alarm guidance, Trusted Advisor and Quota Monitor claims, `InsufficientInstanceCapacity` advice, template CLI operation names, and the quota-code example.
Method: documentation only; no commands were run.
