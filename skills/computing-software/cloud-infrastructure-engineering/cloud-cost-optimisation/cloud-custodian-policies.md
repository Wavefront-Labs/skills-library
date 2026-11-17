---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cloud-custodian-policies
name: cloud-custodian-policies
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, cloud-custodian-policies, cloud-custodian, c7n, cost-automation-policies, off-hours, mark-for-op]
level: practitioner
status: docs-checked
description: "Write Cloud Custodian policies for cost: find idle or untagged resources, notify owners, mark-for-op with grace periods, off-hours schedules, and run in pull or event mode."
sources: ["https://cloudcustodian.io/docs/quickstart/index.html", "https://cloudcustodian.io/docs/aws/examples/offhours.html", "https://cloudcustodian.io/docs/aws/lambda.html", "https://cloudcustodian.io/docs/aws/examples/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Custodian cost policies

## Pattern
Policies are YAML files with a resource, filters and actions. For anything destructive use two stages: a first policy
tags candidates and notifies owners, and a second policy acts only on resources whose grace period has expired.
Look up the exact filter and action names for each resource type in the Cloud Custodian resource reference rather than
copying them from memory.

## Common cost policies
- Unattached volumes, unused Elastic IPs, idle load balancers, old snapshots.
- Untagged resources: notify, then stop (non-prod) after a grace period.
- **Off-hours**: the `offhour` and `onhour` filters stop and start non-production instances; the schedule is read from
  a resource tag (the docs example uses `custodian_downtime`).
- Oversized or idle instances using CloudWatch metrics filters.

## Running
- Pull mode: `custodian run --dryrun -s <output-dir> policy.yml` first, then without `--dryrun`; schedule it in CI or
  a container.
- Event and periodic modes deploy a policy as a Lambda function (`mode:` `periodic` or `cloudtrail` among others, per
  the AWS Lambda page); with `--assume` the role is also the Lambda execution role, otherwise set `role` in the mode
  config block.
- Switching a deployed policy between `periodic` and `schedule` does not remove the old EventBridge rule; the docs point
  to `tools/ops/mugc.py` for cleanup.

## Gotchas
- Delete actions without a grace period and owner notification cause incidents.
- Run with least-privilege roles per policy set.

## Verify
- [ ] Dry run output reviewed; notifications reach owners before any destructive action.

## Checked
2026-11-01. Confirmed in the Cloud Custodian quickstart (`custodian run --dryrun -s`), the offhours example
(`offhour`/`onhour`, `custodian_downtime`) and the AWS Lambda mode page (periodic, cloudtrail, `--assume`, `role`,
EventBridge rule behaviour, mugc.py). Removed: the sample ebs mark-for-op and notify YAML, the SQS notify transport,
c7n-org and c7n-mailer claims, and the Azure Functions claim (not confirmed in the pages read); the cited
usage/offhours page returned 404 and was replaced.
Method: documentation only; no commands were run.
