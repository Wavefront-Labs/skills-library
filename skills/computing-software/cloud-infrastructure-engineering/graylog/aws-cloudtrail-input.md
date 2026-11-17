---
id: computing-software.cloud-infrastructure-engineering.graylog.aws-cloudtrail-input
name: aws-cloudtrail-input
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [aws-inputs, aws-cloudtrail, sqs, s3-notifications, iam-role]
level: advanced
status: docs-checked
description: "Ingest AWS CloudTrail via S3 and SQS: trail, queue policy, S3 event notifications and the IAM role Graylog uses."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/aws_cloudtrail_input.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# aws cloudtrail input

Pull input. Required AWS setup:
1. Create a CloudTrail trail delivering to an S3 bucket; note bucket name and region.
2. Create an SQS queue in the region Graylog will poll. Record queue name and region.
3. Give the S3 bucket permission to send to the queue: an access policy allowing `sqs:SendMessage` from the bucket. Without it, S3 event notifications silently fail to enqueue.
4. Add an S3 event notification for `s3:ObjectCreated:*` targeting the queue directly (single consumer) or an SNS topic the queue subscribes to (multiple consumers). The SNS topic name is used only inside AWS.
5. Create an IAM role with permissions to read the SQS queue and S3 objects, used by the Graylog input.

The IAM role needs `sqs:ReceiveMessage`, `sqs:DeleteMessage` and `s3:GetObject`.

Then create the input with the SQS queue name and region.

## Checked

2026-11-04. Confirmed against the AWS CloudTrail input page. Removed: the claim to enable Illuminate content, which the page does not state. Added the permissions and delivery hint the page lists.

Method: documentation only; no commands were run.
