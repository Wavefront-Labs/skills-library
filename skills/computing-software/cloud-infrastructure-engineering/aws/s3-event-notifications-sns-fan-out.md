---
id: computing-software.cloud-infrastructure-engineering.aws.s3-event-notifications-sns-fan-out
name: s3-event-notifications-sns-fan-out
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-to-sns, sns-fan-out, s3-event-notifications, sqs]
level: practitioner
status: docs-checked
description: "Fan out S3 event notifications to several consumers through an SNS topic: topic and key policies, notification config, SQS subscriptions and filter policies."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 to SNS fan-out

**Why:** notification configurations with filters cannot define overlapping prefixes or suffixes for the same event types, and one rule has one destination. Send once to a standard SNS topic in the bucket's Region (SNS FIFO topics are not allowed), then fan out.

## 1. Topic policy
```json
{"Effect":"Allow","Principal":{"Service":"s3.amazonaws.com"},"Action":"SNS:Publish",
 "Resource":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:uploads",
 "Condition":{"ArnLike":{"aws:SourceArn":"arn:aws:s3:::uploads-prod"},"StringEquals":{"aws:SourceAccount":"<ACCOUNT_ID>"}}}
```
Encrypted topic: with a customer managed KMS key, its key policy must let `s3.amazonaws.com` call `kms:GenerateDataKey` and `kms:Decrypt`.

## 2. Bucket notification
```bash
aws s3api put-bucket-notification-configuration --bucket uploads-prod --notification-configuration '{
 "TopicConfigurations":[{"TopicArn":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:uploads",
   "Events":["s3:ObjectCreated:*"],"Filter":{"Key":{"FilterRules":[{"Name":"prefix","Value":"incoming/"}]}}}]}'
```
This call replaces the whole notification configuration; include existing entries. S3 verifies that SNS and SQS destinations exist and that the bucket owner may publish.

## 3. Subscribers
```bash
aws sns subscribe --topic-arn <TOPIC_ARN> --protocol sqs --notification-endpoint <QUEUE_ARN> \
  --attributes '{"RawMessageDelivery":"true"}'
```
- Each queue's access policy must allow `sns.amazonaws.com` `SendMessage` with `aws:SourceArn` = topic.
- Without raw delivery, the S3 event JSON is a string inside the SNS envelope's `Message` field.
- To filter per consumer, set the subscription attributes `FilterPolicy` and `FilterPolicyScope` (`MessageAttributes` is the default; `MessageBody` filters on message body properties). SNS filter policies support string prefix and suffix matching; changes take up to 15 minutes to take full effect.

## 4. Alternative
EventBridge notifications on the bucket (`EventBridgeConfiguration`) give rule-based fan-out to many
targets without SNS, with richer filtering.

## Verify
- [ ] Uploading `incoming/images/a.jpg` lands one message in each subscribed queue whose filter matches, and none in the others.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: filter overlap rule and standard-SNS-only, same-Region destination, SNS topic policy with `aws:SourceArn` and `aws:SourceAccount`, KMS key-policy actions for S3, put replaces the whole configuration (botocore model), SNS `Subscribe` attributes `RawMessageDelivery`, `FilterPolicy`, `FilterPolicyScope`, and the 15-minute filter-policy propagation. Removed an SNS body-filter example whose handling of the `Records` array is not documented.

Method: documentation only; no commands were run.
