---
id: computing-software.cloud-infrastructure-engineering.graylog.aws-s3-and-kinesis-inputs
name: aws-s3-and-kinesis-inputs
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [aws-s3, kinesis, cloudwatch-logs, dynamodb-permissions, kcl]
level: advanced
status: docs-checked
description: "AWS S3 and Kinesis/CloudWatch inputs: SQS notifications, required IAM actions and KCL DynamoDB permissions in 7.2."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/aws_s3_input.htm
  - https://go2docs.graylog.org/current/getting_in_log_data/aws_kinesis_cloudwatch_input.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# aws s3 and kinesis inputs

**AWS S3 input** (pull). Supports JSON Array, CSV, GELF (newline delimited) and Text (newline delimited, usable for newline-delimited JSON). Setup: configure bucket notifications via SNS topic or SQS queue; create an SQS queue Graylog reads, with an access policy letting the bucket publish; create an IAM role allowing `sqs:ReceiveMessage`, `sqs:DeleteMessage` and `s3:GetObject`. Input fields include AWS SQS Region, AWS S3 Region, SQS Queue Name and Enable Throttling (stops reading when Graylog falls behind).

**AWS Kinesis/CloudWatch input** is built on the Kinesis Client Library (KCL), which uses DynamoDB to track progress and CloudWatch for metrics, so the IAM identity needs those permissions too. Since Graylog 7.2 it uses KCL 3.5, which needs additional DynamoDB permissions for every such input, including existing ones. Send CloudWatch logs to Kinesis per AWS docs, choosing Other as the log format in the subscription filter wizard.

## Checked

2026-11-04. Confirmed against the AWS S3 and Kinesis input pages. Nothing removed.

Method: documentation only; no commands were run.
