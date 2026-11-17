---
id: computing-software.cloud-infrastructure-engineering.aws.cloudtrail-network-activity-events
name: cloudtrail-network-activity-events
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudtrail, network-activity-events, vpc-endpoints, data-perimeter, advanced-event-selectors]
level: advanced
status: docs-checked
description: "Log CloudTrail network activity events for VPC endpoints to see API calls through endpoints, including calls denied by endpoint policy (VpceAccessDenied)."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudTrail network activity events for VPC endpoints

**Use:** see who calls AWS APIs through your VPC endpoints, especially attempts to reach resources
outside your data perimeter that the endpoint policy blocks.

## 1. Enable with advanced event selectors
```bash
aws cloudtrail put-event-selectors --trail-name main --advanced-event-selectors '[
 {"Name":"S3 VPCE denied","FieldSelectors":[
   {"Field":"eventCategory","Equals":["NetworkActivity"]},
   {"Field":"eventSource","Equals":["s3.amazonaws.com"]},
   {"Field":"errorCode","Equals":["VpceAccessDenied"]}]}]'
```
- Only certain services' VPC endpoints are supported; check the current list on the CloudTrail network activity events page.
- Network activity events are for **VPC endpoint owners**: they record API calls made through the owner's endpoints.

## 2. What you see
`eventCategory: NetworkActivity`, `vpcEndpointId`, `vpcEndpointAccountId`, the calling principal, the target
resource, and `errorCode: VpceAccessDenied` when the endpoint policy denied the request.

## 3. Uses
- Exfiltration attempts: principal inside your VPC writing to a bucket in an unknown account.
- Testing a stricter endpoint policy: log denials for a week before enforcing elsewhere.

## Cost
See the CloudTrail pricing page; filter with `errorCode` to only log denials if volume is high.

## Verify
- [ ] From an instance, `aws s3 cp f s3://<FOREIGN_BUCKET>/` through an endpoint whose policy limits to your org yields a `VpceAccessDenied` network activity event.

## Checked

2026-10-28

Confirmed: put-event-selectors with --trail-name and --advanced-event-selectors, vpcEndpointId, vpcEndpointAccountId, errorCode, VpceAccessDenied for endpoint policy violations, network activity events are recorded for VPC endpoint owners (CloudTrail User Guide pages, check_commands).

Removed: the KMS selector example and the supported-service list, cross-account delivery claim, billing statement.

Method: documentation only; no commands were run.
