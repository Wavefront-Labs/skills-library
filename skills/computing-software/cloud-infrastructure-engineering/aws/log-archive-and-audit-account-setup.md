---
id: computing-software.cloud-infrastructure-engineering.aws.log-archive-and-audit-account-setup
name: log-archive-and-audit-account-setup
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, log-archive-account, audit-account, security-tooling, organization-trail, multi-account]
level: practitioner
status: docs-checked
description: "Set up a dedicated Log Archive account and organization trail: protected S3 log storage, KMS, Object Lock, integrity validation, and Control Tower logging and security accounts."
sources:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/log-archive.html
  - https://docs.aws.amazon.com/controltower/latest/userguide/accounts.html
  - https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log Archive account and organization trail

## 1. Purpose of the Log Archive account
The AWS Security Reference Architecture (SRA) dedicates a Log Archive account to ingesting and archiving all security-related logs and backups. The objectives: immutable storage, accessed only by controlled, automated and monitored mechanisms, built for durability (replication and archival). Logs shown in the SRA include the CloudTrail organization trail, VPC flow logs, CloudFront and WAF access logs, and Route 53 DNS logs. SRA recommends consolidating operational log data into this account too, filtering and restricting access as your governance requires.

With AWS Control Tower, a logging account (default name: CloudTrail administrator) and a security account (default name: Config aggregator) are the accounts Control Tower expects. When you bring existing accounts for those roles, Control Tower checks for conflicting resources (for example a logging bucket with the name it requires) and that STS is enabled and the account is not suspended; it does not remove existing resources.

## 2. Log bucket protections
Many AWS services (CloudTrail, VPC Flow Logs, Elastic Load Balancing, GuardDuty, Config, WAF) log to S3, so integrity comes from S3 object integrity, confidentiality from S3 access controls, and availability from S3 Object Lock, object versions and Lifecycle rules.
- New objects are encrypted by default with SSE-S3, where access is controlled only by IAM policies. SSE-KMS with a key you manage adds a second access-control layer: readers need S3 read permission and decrypt permission under the key policy.
- To protect or verify CloudTrail logs, use log file integrity validation (detects modification or deletion after delivery) and/or S3 Object Lock.
- Least privilege: the managed policy `AWSCloudTrail_FullAccess` lets holders disable or reconfigure auditing, so limit it to as few people as possible.
- Detective controls: AWS Config and IAM Access Analyzer monitor the preventive controls for unexpected changes.

## 3. Organization trail
- Create it from the management account or a delegated administrator; permissions in that account are required.
- Console-created organization trails are multi-Region. The CLI can create single-Region or multi-Region trails. To cover all partitions create a multi-Region organization trail in each.
- A copy of the trail with the same name appears in member accounts. Member accounts can see it but cannot delete it, stop logging or change what is logged. Accounts joining the organization get the trail and the `AWSServiceRoleForCloudTrail` service-linked role automatically.
- Logs for the whole organization go to one S3 bucket: a folder named for the organization ID with a subfolder per account ID. By default only the management account can access that bucket and logs.
- A trail is still created in member accounts if validation fails (for example a wrong bucket policy or no KMS permission); check `get-trail-status` in the member account.
- Event history shows only the signed-in account's last 90 days of management events.
```bash
aws cloudtrail create-trail --name org-trail --s3-bucket-name <LOG_BUCKET> --is-organization-trail \
  --is-multi-region-trail --enable-log-file-validation --kms-key-id <KEY_ARN>
aws cloudtrail start-logging --name org-trail
```
The bucket policy and KMS key policy must allow CloudTrail to deliver and encrypt; consult the CloudTrail user guide pages for the exact statements.

## Verify
- [ ] `get-trail-status` shows no delivery or KMS errors; new account events appear in the bucket under the organization and account folders.
- [ ] `aws cloudtrail validate-logs` passes for a sample window.
- [ ] Access to the log bucket and key is limited to controlled roles, with Config or Access Analyzer monitoring changes.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the SRA Log Archive page, the Control Tower accounts page and the CloudTrail organization trail page. CLI commands checked against the botocore model. Removed as not stated by the pages: the bucket and KMS policy statements, `aws:SourceOrgID` conditions, SCP deny lists, Glacier lifecycle timings, the 15-minute delivery figure, the list of delegated administrator services for the audit account, and the exact object key prefix.
