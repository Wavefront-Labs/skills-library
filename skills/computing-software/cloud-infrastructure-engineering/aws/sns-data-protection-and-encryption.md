---
id: computing-software.cloud-infrastructure-engineering.aws.sns-data-protection-and-encryption
name: sns-data-protection-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sns, sns-data-protection, sns-encryption, data-protection-policy, pii-masking, de-identify, audit-findings, sse-kms, kms-key-policy, topic-policy, aws-sourcearn, sns-vpc-endpoint, secure-transport, messaging]
level: practitioner
status: docs-checked
description: "Encrypt SNS topics with KMS without breaking service publishers, write data protection policies that audit or mask PII in transit, and lock topic policies to named publishers."
sources: ["https://docs.aws.amazon.com/sns/latest/dg/sns-key-management.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-policies.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-operations.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-managed-data-identifiers.html", "https://docs.aws.amazon.com/sns/latest/dg/sns-access-policy-use-cases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNS encryption, data protection policies and topic policies

**Goal:** an encrypted topic whose publishers (services and apps) can still deliver, PII that
is detected and masked before it reaches subscribers that must not see it, and a topic
policy nobody else can publish to.

## 1. SSE-KMS on a topic
```bash
aws sns set-topic-attributes --topic-arn "$TOPIC" --attribute-name KmsMasterKeyId --attribute-value alias/sns-app
```
Use a symmetric encryption KMS key (SNS does not support other key types). Publishers need
`kms:GenerateDataKey*` and `kms:Decrypt` on the key. For AWS services that publish to the topic, use a
**customer managed key** and add the service principal to the key policy with the same two actions:
```json
{"Sid":"PublishersViaSNS","Effect":"Allow",
 "Principal":{"Service":["cloudwatch.amazonaws.com","events.amazonaws.com","s3.amazonaws.com"]},
 "Action":["kms:GenerateDataKey*","kms:Decrypt"],"Resource":"*"}
```
The SNS docs list the principals per source (for example `cloudwatch.amazonaws.com`, `events.amazonaws.com`,
`s3.amazonaws.com`, `ses.amazonaws.com`, `redshift.amazonaws.com`, `events.rds.amazonaws.com`); some sources
(EC2 Auto Scaling, AWS Config, CodePipeline, Elastic Beanstalk, AWS IoT, Elastic Transcoder, EC2 Image Builder)
need an IAM role in the key policy instead of a service principal. Add `aws:SourceAccount` and `aws:SourceArn`
conditions against confused-deputy, except for EventBridge-to-encrypted-topic, where they are not supported.
SNS reuses a data key for up to 5 minutes, so KMS request volume scales with the number of publishing principals.
KMS error names you may see: `KMSAccessDeniedException`, `KMSDisabledException`, `KMSInvalidStateException`,
`KMSNotFoundException`, `KMSOptInRequired`, `KMSThrottlingException`.

## 2. Data protection policies
**Availability: AWS states that Amazon SNS message data protection is no longer available to new customers**
(see the availability-change page linked from the SNS docs); existing users can keep using it. Check that
page before designing anything new around it.

A policy on the topic that scans messages for managed data identifiers (for example credit card numbers,
email addresses, AWS secret keys; the docs list about 45 types by category and country) and then audits,
denies or de-identifies. `DataDirection` is `Inbound` (Publish requests) or `Outbound` (deliveries).
```json
{"Name":"pii-policy","Version":"2021-06-01","Statement":[
 {"Sid":"audit","DataDirection":"Inbound","Principal":["*"],
  "DataIdentifier":["arn:aws:dataprotection::aws:data-identifier/EmailAddress","arn:aws:dataprotection::aws:data-identifier/CreditCardNumber"],
  "Operation":{"Audit":{"SampleRate":"99","FindingsDestination":{"CloudWatchLogs":{"LogGroup":"/aws/vendedlogs/sns-pii-findings"}}}}},
 {"Sid":"mask-for-analytics","DataDirection":"Outbound","Principal":["arn:aws:iam::<ACCOUNT_ID>:role/analytics-consumer"],
  "DataIdentifier":["arn:aws:dataprotection::aws:data-identifier/EmailAddress"],
  "Operation":{"Deidentify":{"MaskConfig":{"MaskWithCharacter":"#"}}}},
 {"Sid":"block-secrets","DataDirection":"Inbound","Principal":["*"],
  "DataIdentifier":["arn:aws:dataprotection::aws:data-identifier/AwsSecretKey"],
  "Operation":{"Deny":{}}}]}
```
```bash
aws sns put-data-protection-policy --resource-arn "$TOPIC" --data-protection-policy file://policy.json
```
- Only one data protection policy per topic; it can have several deny or de-identify statements but only
  **one audit statement**. `Version` is `2021-06-01`.
- Audit: `SampleRate` is an integer 0 to 99; `FindingsDestination` and `NoFindingsDestination` accept a CloudWatch
  Logs `LogGroup` (in the topic's Region, name starting `/aws/vendedlogs/`), a Firehose `DeliveryStream`
  (Direct PUT, same Region) or an S3 `Bucket`. The caller of `PutDataProtectionPolicy` needs the logging permissions
  listed in the docs (for example `logs:CreateLogDelivery`, `logs:PutResourcePolicy`). Audit also emits the
  `MessagesWithFindings` and `MessagesWithNoFindings` metrics. Findings record the identifier name, count and
  positions of detections, not the sensitive value.
- `Deidentify` takes `MaskConfig` (`MaskWithCharacter`, one supported character such as `#` or `*`) or
  `RedactConfig` (`{}`, removes the data). De-identification happens after the audit operation on inbound messages.
- `Principal` is the IAM principal calling `Publish` (inbound) or, for outbound, the **subscription principal**:
  the identity that called `Subscribe`, readable as `SubscriptionPrincipal` from `GetSubscriptionAttributes`.
  That is how one topic can give one subscriber the raw value and another the masked one.
- `Deny`: inbound, the `Publish` caller gets `AuthorizationError`; outbound, the message is not delivered and
  delivery status logging shows a FAILURE with status code 403.

## 3. Topic access policy
By default only the topic owner can publish or subscribe; other principals need a topic policy statement.
```json
{"Statement":[
 {"Sid":"AlarmsOnly","Effect":"Allow","Principal":{"Service":"cloudwatch.amazonaws.com"},"Action":"sns:Publish",
  "Resource":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:alerts","Condition":{"ArnLike":{"aws:SourceArn":"arn:aws:cloudwatch:<REGION>:<ACCOUNT_ID>:alarm:*"}}},
 {"Sid":"SubscribeOnlyHttpsAndSqs","Effect":"Deny","Principal":"*","Action":"sns:Subscribe","Resource":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:alerts","Condition":{"StringNotEquals":{"sns:Protocol":["https","sqs"]}}}]}
```
Condition keys in the SNS access-control examples: `sns:Protocol` (limit subscription protocol; `AddPermission`
cannot express it, so write the policy and set it with `SetTopicAttributes`), `aws:SourceAccount` and
`aws:SourceArn` for services (`aws:SourceOwner` is deprecated), `aws:PrincipalOrgID` for organisation-wide
publish, and `aws:sourceVpce` to deny `sns:Publish` unless it comes from a named VPC endpoint (it takes the
endpoint ID, for example `vpce-1ab2c34d`).

## Gotchas
- `Deny` on inbound returns `AuthorizationError` to the publisher: make sure publishers log it distinctly from IAM denials.
- Policy JSON `Version` for data protection is `2021-06-01`, not `2012-10-17`.

## Verify
- [ ] Publishing a message containing a test credit-card number (e.g. 4111 1111 1111 1111) produces an audit finding in `/sns/pii-findings`; the analytics subscription receives the number masked with the configured character, the fraud subscription the raw number.
- [ ] A message that the `AwsSecretKey` identifier detects is rejected with `AuthorizationError` (use a synthetic key from the AWS docs).
- [ ] A CloudWatch alarm action publishes successfully after the key policy change (alarm history shows `Successfully executed action`).

## Checked

Date 2026-10-23. Documentation release: current Amazon SNS Developer Guide (key management, data protection policies, operations, managed data identifiers, access-control examples).
Confirmed: symmetric keys only; `kms:GenerateDataKey*` and `kms:Decrypt` for publishers and service principals (plus the principal list and IAM-role exceptions); 5-minute data key reuse; data protection policy structure, `Version` 2021-06-01, one policy per topic and one audit statement; Audit, De-identify and Deny fields and behaviour; subscription principal; identifiers `EmailAddress`, `CreditCardNumber`, `AwsSecretKey`; access-policy condition keys and the VPC-endpoint deny example. NEW: SNS message data protection is no longer available to new customers.
Corrected: the Audit log group must start with `/aws/vendedlogs/`; `budgets.amazonaws.com` is not in the documented principal list; "200+ identifiers" and evaluation-order claims were not in the docs.
Removed (not in docs): failure symptoms of missing grants, "subscribers need nothing on the topic key", body-only encryption remark, multi-region key remark, custom regex identifiers, FIFO and payload-size limits, policy size cap, latency and cost remarks, `sns:Endpoint` advice, `KmsMasterKeyId` change effects.
Sources: https://docs.aws.amazon.com/sns/latest/dg/sns-key-management.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-policies.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-operations.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-managed-data-identifiers.html ; https://docs.aws.amazon.com/sns/latest/dg/sns-access-policy-use-cases.html

Method: documentation only; no commands were run.
