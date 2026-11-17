---
id: computing-software.cybersecurity-defensive.splunk.splunk-add-on-for-aws-and-microsoft-cloud-ingestion
name: splunk-add-on-for-aws-and-microsoft-cloud-ingestion
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-add-on-for-aws, splunk-add-on-for-microsoft-cloud-services, cloudtrail, sqs-based-s3, event-hub, data-onboarding, cloud-logging, heavy-forwarder, inputs-data-manager]
level: practitioner
status: draft
description: "Ingest AWS CloudTrail/GuardDuty and Microsoft 365/Entra/Azure logs into Splunk with the AWS and Microsoft Cloud Services add-ons using SQS-based S3 and Event Hub inputs."
sources: ["https://docs.splunk.com/Documentation/AddOns/released/AWS/About", "https://docs.splunk.com/Documentation/AddOns/released/AWS/SQS-basedS3", "https://docs.splunk.com/Documentation/AddOns/released/MSCloudServices/About", "https://docs.splunk.com/Documentation/AddOns/released/MSO365/About"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cloud log ingestion with the Splunk AWS and Microsoft add-ons

Goal: get cloud control-plane and security logs into Splunk reliably, CIM-mapped, without polling
APIs in ways that drop data.

## Where the add-ons run
Install the input side on a heavy forwarder or IDM / Splunk Cloud Victoria search head (inputs run
there); install the same add-on on search heads (and indexers for index-time props) for parsing.

## AWS (Splunk Add-on for AWS)
- Use **SQS-based S3** inputs for CloudTrail, VPC Flow Logs, ELB/CloudFront access logs, S3 access
  logs and Config. Flow: S3 bucket -> event notification -> SNS -> SQS -> add-on reads SQS, fetches the
  object. Scales horizontally (several HFs on the same queue) and tracks state in SQS, not on disk.
- Create a dead-letter queue and set the main queue visibility timeout above the add-on's processing
  time (300 s is a safe start); messages that land in the DLQ are logs you lost.
- Generic S3 inputs keep a checkpoint per key and crawl the bucket; avoid them for large buckets.
- GuardDuty, Security Hub, IAM Access Analyzer: route EventBridge -> Kinesis Data Firehose -> HEC
  (Firehose sourcetype `aws:firehose:json`) or EventBridge -> SQS for the add-on.
- IAM: role per input with `s3:GetObject`, `sqs:ReceiveMessage/DeleteMessage/GetQueueAttributes`,
  `kms:Decrypt` for SSE-KMS buckets. Use an assumed role per account for multi-account orgs.
- Sourcetypes: `aws:cloudtrail`, `aws:cloudwatchlogs:vpcflow`, `aws:config`, all mapped to CIM.

## Microsoft
- **Splunk Add-on for Microsoft Office 365**: Management Activity API (audit general, Exchange,
  SharePoint, Entra ID) plus message trace; needs an Entra app registration with
  `ActivityFeed.Read` and admin consent. Tenant may need audit enabled first.
- **Splunk Add-on for Microsoft Cloud Services**: Azure Event Hub inputs for Entra sign-in/audit logs,
  Azure activity and resource diagnostics (configure Diagnostic settings to stream to the hub); use a
  dedicated consumer group per Splunk input.
- **Microsoft Security add-on** (Defender alerts/incidents via Graph) for XDR alerts.

## Gotchas
- CloudTrail organisation trails put every account under one prefix; one SQS input handles them all.
- KMS-encrypted objects silently fail without `kms:Decrypt`; check `_internal` for AccessDenied.
- Event Hub throughput units throttle at peak; watch the hub's ThrottledRequests metric.
- O365 API content blobs become available with 30-90 minutes delay; do not alert on absence sooner.

## Verify
- `index=_internal sourcetype=aws:sqsbaseds3:log ERROR` and `source=*splunk_ta_o365*` show no errors.
- `| tstats count where index=aws sourcetype=aws:cloudtrail by _time span=1h` has no holes.
- DLQ message count stays at zero.
