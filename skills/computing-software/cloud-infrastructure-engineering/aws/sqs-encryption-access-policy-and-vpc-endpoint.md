---
id: computing-software.cloud-infrastructure-engineering.aws.sqs-encryption-access-policy-and-vpc-endpoint
name: sqs-encryption-access-policy-and-vpc-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sqs, sqs-sse, sqs-policy, sqs-vpc-endpoint, sse-sqs, sse-kms, kms-data-key-reuse-period, queue-policy, resource-policy, aws-sourcearn, cross-account-sqs, privatelink, interface-endpoint, least-privilege, messaging, encryption]
level: practitioner
status: docs-checked
description: "Lock down an SQS queue: SSE-SQS vs SSE-KMS with data-key reuse, queue policies that let only named services/accounts send (aws:SourceArn), and an interface VPC endpoint with aws:sourceVpce."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-key-management.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-basic-examples-of-sqs-policies.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-internetwork-traffic-privacy.html", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-security-best-practices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQS security: encryption, queue policies and VPC endpoints

**Goal:** messages are encrypted with a key you control, only the intended producers can
send and only the intended consumer can receive, and traffic from your VPC never touches the
public internet.

## 1. Encryption at rest
- **SSE-SQS** (the default when a queue is created over HTTPS without encryption attributes): SQS-owned
  keys, AES-256, no additional fee, no keys for you to manage (`SqsManagedSseEnabled`). Only one SSE
  option is supported per queue. Use it unless you need your own KMS key and its audit trail.
- **SSE-KMS**: `KmsMasterKeyId` = your key (the AWS managed key alias is `alias/aws/sqs`);
  `KmsDataKeyReusePeriodSeconds` (60 s to 86,400 s, default 300) controls how long SQS reuses a data
  key before calling KMS again: longer means fewer KMS requests (cost), shorter is tighter. Producers
  that differ get different data keys, so KMS call volume scales with the number of distinct principals.
  An encrypted queue that uses the AWS managed key cannot invoke a Lambda function in a different account.
```bash
aws sqs set-queue-attributes --queue-url "$Q" --attributes \
  '{"KmsMasterKeyId":"alias/sqs-app","KmsDataKeyReusePeriodSeconds":"3600"}'
```
- Every **producer** needs `kms:GenerateDataKey` + `kms:Decrypt` on the key; every consumer
  needs `kms:Decrypt` (a DLQ consumer also needs `kms:Decrypt` on the source queue's key). For AWS
  services that send to the queue, use a customer managed key and add the service principal to the
  **key policy** with `kms:Decrypt` and `kms:GenerateDataKey`: `events.amazonaws.com` (CloudWatch
  Events / EventBridge), `s3.amazonaws.com`, `sns.amazonaws.com`. Add `aws:SourceArn` or
  `aws:SourceAccount` conditions against confused-deputy.
- Only the message body is encrypted; queue metadata (name, attributes) and message metadata (ID,
  timestamp, attributes) are not. Messages already in the queue are not encrypted retroactively.
- After changing the KMS key, messages already encrypted stay encrypted with the old key: keep the old key
  usable until they are processed. All requests to an SSE queue must use HTTPS and Signature Version 4;
  anonymous requests are rejected.

## 2. Queue policy patterns
Use a queue (resource) policy to let AWS services and other accounts in.
```json
{"Version":"2012-10-17","Statement":[
 {"Sid":"SNSOnly","Effect":"Allow","Principal":{"Service":"sns.amazonaws.com"},
  "Action":"sqs:SendMessage","Resource":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders",
  "Condition":{"ArnEquals":{"aws:SourceArn":"arn:aws:sns:<REGION>:<ACCOUNT_ID>:order-events"}}},
 {"Sid":"ConsumerAccount","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<OTHER_ACCOUNT_ID>:role/worker"},
  "Action":["sqs:ReceiveMessage","sqs:DeleteMessage","sqs:ChangeMessageVisibility","sqs:GetQueueAttributes"],
  "Resource":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders"},
 {"Sid":"DenyInsecureTransport","Effect":"Deny","Principal":"*","Action":"sqs:*",
  "Resource":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders","Condition":{"Bool":{"aws:SecureTransport":"false"}}}]}
```
- `aws:SourceArn`/`aws:SourceAccount` on service principals prevents the confused-deputy
  case (any SNS topic in any account could otherwise publish).
- Cross-account consumer: the queue policy names the other account's role or user as `Principal`.
  Cross-account permissions do not apply to `AddPermission`, `CreateQueue`, `DeleteQueue`, `ListQueues`,
  `ListQueueTags`, `RemovePermission`, `SetQueueAttributes`, `StartMessageMoveTask`,
  `CancelMessageMoveTask`, `ListMessageMoveTasks`, `TagQueue` and `UntagQueue`.
- With SSE enabled, `aws:SourceArn` is supported for SNS, S3, CloudWatch Events, Lambda, CodeBuild, AWS
  Auto Scaling and Amazon Chime as event sources.
- `sqs:ReceiveMessage` and `sqs:DeleteMessage` are separate actions and can be granted separately.
- A queue policy is limited to 8,192 bytes, 20 statements, 50 principals and 10 conditions.

## 3. Private access from a VPC
```bash
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.<REGION>.sqs \
  --vpc-endpoint-type Interface --subnet-ids subnet-a subnet-b --security-group-ids sg-vpce --private-dns-enabled
```
With private DNS enabled, use the regional endpoint `sqs.<REGION>.amazonaws.com` (or `sqs.<REGION>.api.aws`
for dual-stack). Only HTTPS endpoints work through the VPC endpoint, and private DNS does not support the
legacy `queue.amazonaws.com` style names. FIPS endpoints use the `com.amazonaws.<REGION>.sqs-fips` service.
Then pin the queue to the endpoint (the condition takes the endpoint ID, not an ARN):
```json
{"Sid":"OnlyViaEndpoint","Effect":"Deny","Principal":"*","Action":"sqs:*",
 "Resource":"arn:aws:sqs:<REGION>:<ACCOUNT_ID>:orders",
 "Condition":{"StringNotEquals":{"aws:sourceVpce":"vpce-0123"}}}
```
Denying `sqs:*` this way forces every action, including the administrative ones needed to change
queue permissions, through that endpoint, which can lock you out of the queue policy. The AWS example
denies only `sqs:SendMessage` and `sqs:ReceiveMessage`; start there. Requests that do not come through your
endpoint (for example from AWS services publishing to the queue) will also be denied by this statement.

## Gotchas
- A VPC endpoint policy is a second control: it names the principals, actions and resources allowed
  through the endpoint (for example only `sqs:SendMessage` on one queue ARN). Users can still call other
  SQS actions from outside the VPC unless the queue policy denies them.
- SSE-KMS queues as **Lambda event sources**: the Lambda execution role needs `kms:Decrypt`.
- `set-queue-attributes` writes the whole `Policy` attribute: read the existing policy and merge before setting.

## Verify
- [ ] `aws sqs get-queue-attributes --attribute-names SqsManagedSseEnabled KmsMasterKeyId` shows the intended mode.
- [ ] A publish from an SNS topic not matching `aws:SourceArn` is not delivered; the allowed topic delivers.
- [ ] From an instance in the VPC, `nslookup sqs.<REGION>.amazonaws.com` returns private 10.x IPs; `aws sqs send-message` works with the instance's NAT route removed.
- [ ] `aws sqs send-message --endpoint-url http://...` (plain HTTP) is denied by the `aws:SecureTransport` statement.

## Checked

Date 2026-10-23. Documentation release: current Amazon SQS Developer Guide, API Reference and Lambda Developer Guide.
Confirmed: SSE-SQS default behaviour and no additional fee; `SqsManagedSseEnabled`, `KmsMasterKeyId`, `KmsDataKeyReusePeriodSeconds` (60 to 86,400, default 300); what SSE does and does not encrypt; producer and consumer KMS permissions; service principals for key policies; aws:SourceArn service list; cross-account action exclusions; policy size limits (8,192 bytes, 20 statements, 50 principals, 10 conditions); VPC endpoint requirements (private DNS, HTTPS only, legacy names unsupported, FIPS service); `aws:sourceVpce` takes an endpoint ID; the warning about denying `sqs:*`.
Removed or corrected: KMS key policy list now follows the docs (CloudWatch alarms and a specific SNS log error were not documented), "both halves required" cross-account claim, security-group-443 claim, endpoint policy default, Lambda ESM `Problem:` text, per-service SourceArn forms, Null-condition advice.
Sources: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html ; .../sqs-key-management.html ; .../sqs-configure-sqs-sse-queue.html ; .../sqs-internetwork-traffic-privacy.html ; .../sqs-creating-custom-policies-access-policy-examples.html ; .../sqs-basic-examples-of-sqs-policies.html ; .../quotas-messages.html

Method: documentation only; no commands were run.
