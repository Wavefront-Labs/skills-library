---
id: computing-software.cloud-infrastructure-engineering.aws.cloudtrail-and-config-audit
name: cloudtrail-and-config-audit
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudtrail, aws-config, config-rules, audit-trail, organization-trail, management-events, data-events, insights-events, log-file-validation, cloudtrail-lake, event-data-store, config-recorder, config-aggregator, conformance-packs, managed-rules, custom-rules, config-remediation, ssm-automation, compliance, lookup-events, cis-alarms, metric-filters, audit-logging, configuration-history, config-advanced-query]
level: practitioner
status: draft
description: "Set up tamper-evident CloudTrail (org trail, data events, validation, Lake) and AWS Config (recorder, aggregator, rules, conformance packs, auto-remediation) with cost control."
sources: ["AWS CloudTrail User Guide - Creating a trail for an organization", "AWS CloudTrail User Guide - Logging data events and Insights events", "AWS CloudTrail User Guide - Validating CloudTrail log file integrity", "AWS CloudTrail User Guide - Working with AWS CloudTrail Lake", "AWS Config Developer Guide - Setting up AWS Config, aggregators and recording", "AWS Config Developer Guide - Managed rules, conformance packs and remediation", "CIS Amazon Web Services Foundations Benchmark - Monitoring section"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudTrail and AWS Config — who did what, and what does the estate look like

**Goal:** an immutable record of every API call across every account and region, a
queryable history of every resource's configuration, and rules that flag (or fix) drift
from policy — without a surprise bill from data events or config items. Security
findings built on top of these are in `...aws.guardduty-security-hub-inspector-macie`.

## 1. CloudTrail: one org trail, done right
- **Event history** (90 days, management events, per account/region) exists without
  any trail and is free; `aws cloudtrail lookup-events --lookup-attributes
  AttributeKey=EventName,AttributeValue=DeleteBucket` is the first thing to run in an
  incident. For retention, cross-account search and data events you need a trail.
- Create **one organization trail** from the management account (or a delegated
  admin): multi-region, all management events, `--is-organization-trail`,
  delivering to the **Log Archive** account's bucket with SSE-KMS and
  `--enable-log-file-validation`. Member accounts cannot modify or stop it. Control
  Tower creates exactly this; do not add a second one — the first copy of management
  events is free, every additional trail that records them costs USD 2 per 100k events.
- Bucket policy must allow `cloudtrail.amazonaws.com` `s3:PutObject` on
  `AWSLogs/<org-id>/*` with `s3:x-amz-acl: bucket-owner-full-control`, plus
  `s3:GetBucketAcl`; add `aws:SourceArn` of the trail. Enable Object Lock
  (compliance mode) or at least versioning + MFA delete on this bucket: this is the
  evidence store.
- **Data events** are opt-in and billed (USD 0.10 per 100k): S3 object-level, Lambda
  `Invoke`, DynamoDB item-level, plus newer resource types. Use **advanced event
  selectors** to scope them — e.g. `resources.ARN StartsWith arn:aws:s3:::prod-` and
  `readOnly = false` — rather than "all S3 buckets", and never include the trail's own
  log bucket (write loop).
- **Insights events** (unusual API call rate or error rate per account) cost USD 0.35
  per 100k management events analysed; enable on the org trail if you lack other
  anomaly detection.
- **Log file validation** writes hourly digest files signed by CloudTrail;
  `aws cloudtrail validate-logs --trail-arn <ARN> --start-time <ISO>` proves nothing
  was altered or deleted — auditors ask for this.
- **CloudTrail Lake** is the alternative to S3 + Athena: an **event data store**
  (`create-event-data-store --retention-period 2557 --organization-enabled`)
  queryable with SQL from the console/CLI, optionally also ingesting Config items and
  non-AWS events. Billed on ingestion (one-year or seven-year retention pricing) plus
  per-TB scanned; a 7-year store for management events is cheaper than it looks because
  the free-copy rule does not apply — compare before migrating an S3 pipeline.
- Ship to CloudWatch Logs as well (`--cloud-watch-logs-log-group-arn`) only in the
  account where you need **metric filters + alarms** for the CIS controls (root login,
  unauthorised API calls, IAM policy changes, CloudTrail config changes, security group
  changes). Set retention; CloudTrail to CloudWatch Logs is the common hidden ingest cost.

## 2. AWS Config: recorder, delivery, aggregation
- Per account per region: a **configuration recorder** (what to record), a **delivery
  channel** (S3 bucket in Log Archive, optional SNS) and `start-configuration-recorder`.
  Control Tower and most landing zones do this; verify with
  `aws configservice describe-configuration-recorder-status`.
- **Recording scope is the cost lever.** Each configuration item (CI) costs USD 0.003.
  Recording *all* resource types including global ones in every region triggers a flood
  during deployments (every ECS task, every Lambda version, every ENI). Use the
  recording strategy to exclude noisy types (`AWS::EC2::NetworkInterface`,
  `AWS::ECS::TaskDefinition` revisions if you do not audit them) and set **daily
  recording** for types where you need the state but not every change. Record global
  types (IAM) in **one** region only.
- A **Config aggregator** in the Audit account
  (`put-configuration-aggregator --organization-aggregation-source AllAwsRegions=true,RoleArn=...`)
  gives an org-wide inventory and `select-aggregate-resource-config` SQL
  (`SELECT resourceId, accountId WHERE resourceType = 'AWS::EC2::Volume' AND configuration.encrypted = false`).
- Retention: `put-retention-configuration --retention-period-in-days 2557` (max 7 years).

## 3. Config rules and conformance packs
- **Managed rules** cover most policy: `s3-bucket-public-read-prohibited`,
  `restricted-ssh`, `encrypted-volumes`, `rds-storage-encrypted`, `required-tags`
  (with parameters), `iam-user-mfa-enabled`, `cloudtrail-enabled`, `acm-certificate-expiration-check`.
  Rules are evaluated on change (`ConfigurationItemChangeNotification`) and/or on a
  schedule (`MaximumExecutionFrequency: TwentyFour_Hours`); each evaluation costs
  USD 0.001 for the first 100k per region.
- **Custom rules**: Lambda-backed (any logic, any language) or **Guard** policy-as-code
  (`CUSTOM_POLICY` source, no Lambda to maintain). Guard is the right default for
  "field X must equal Y" rules.
- **Conformance packs** bundle rules + remediation into a CloudFormation-like YAML
  deployable org-wide (`put-organization-conformance-pack`). AWS publishes sample packs
  (Operational Best Practices for CIS, PCI, NIST, HIPAA); copy and trim one rather than
  starting from zero. Organization rules/packs cannot be deleted by member accounts.
- **Auto-remediation** attaches an SSM Automation document to a rule:
  `put-remediation-configurations` with `TargetId AWS-DisablePublicAccessForSecurityGroup`,
  an `AutomationAssumeRole`, `Automatic: true`, `MaximumAutomaticAttempts 3` and
  `RetryAttemptSeconds 60`. Start with `Automatic: false` (manual trigger from the
  console) to see what it would touch. Common safe ones: `AWS-ConfigureS3BucketLogging`,
  `AWS-DisableS3BucketPublicReadWrite`, `AWSConfigRemediation-EnableCloudTrailLogFileValidation`,
  `AWS-PublishSNSNotification` (just page someone).

## 4. Day-two operations
- Compliance timeline per resource and `get-resource-config-history` give the "what
  changed at 02:13" answer; pair with CloudTrail `lookup-events --lookup-attributes
  AttributeKey=ResourceName,AttributeValue=<id>` for "who".
- CloudTrail delivers within ~5 minutes on average, 15 minutes worst case; Config CIs
  can lag minutes to an hour under load. Neither is real-time — use EventBridge rules on
  the API event (`detail-type: AWS API Call via CloudTrail`) when you need seconds.
- Export the Security Hub/Config compliance summary monthly; auditors want trend, not a screenshot.

## Gotchas
- A trail's `IsLogging` can be silently false after a KMS key policy or bucket policy
  change breaks delivery — alarm on `cloudtrail:StopLogging` **and** on the S3 bucket
  receiving zero objects per hour.
- Global service events (IAM, STS, CloudFront) are recorded once, in the trail's home
  region; a single-region trail elsewhere misses them.
- `lookup-events` searches only management events and only the current account and
  region; org-wide search needs Athena over the bucket or CloudTrail Lake.
- Config `required-tags` evaluates only resource types it supports; untagged Lambda
  functions pass by omission unless you add a custom rule.
- Deleting the Config recorder deletes nothing from S3 but stops rule evaluation; rules
  then report stale `COMPLIANT` indefinitely.
- Config resource types added by AWS later are **auto-included** when recording "all"
  — the bill can rise without any change on your side; review the recording group quarterly.

## Verify
- [ ] Exactly one org trail: multi-region, validation on, SSE-KMS, Object Lock/versioned bucket in Log Archive; `validate-logs` passes for last 24 h.
- [ ] Data events scoped by advanced selectors to named prefixes; trail bucket excluded.
- [ ] Config recorder running in every governed region; aggregator shows all accounts; global types recorded in one region only.
- [ ] CIS metric-filter alarms fire on a test (e.g. create then delete a security group rule) within 15 minutes.
- [ ] One conformance pack deployed org-wide; one remediation executed end to end on a non-prod resource and reversible.
