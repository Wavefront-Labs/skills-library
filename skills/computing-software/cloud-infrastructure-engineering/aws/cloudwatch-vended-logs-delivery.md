---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-vended-logs-delivery
name: cloudwatch-vended-logs-delivery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, vended-logs, log-delivery, delivery-source, delivery-destination, logs-kms, log-group-encryption, elb-access-logs, cross-account-log-delivery, firehose, s3-log-delivery]
level: practitioner
status: docs-checked
description: "Deliver AWS service (vended) logs to CloudWatch Logs, S3 or Firehose with the delivery API, encrypt log groups with KMS, and fix the bucket and key policies that break delivery."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html", "https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliverySource.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vended logs delivery and log encryption

**Goal:** service logs (ALB access logs, CloudFront, API Gateway, AppSync, Bedrock and the many
services listed in the CloudWatch Logs "Enable logging from AWS services" catalog) land where
they are needed, encrypted with your key, and nobody discovers a month later that delivery
silently failed.

## 1. Two delivery mechanisms
| Mechanism | Configured with |
|---|---|
| Service-native settings (e.g. ELB access logs to S3, VPC Flow Logs) | The service's own API (`elbv2 modify-load-balancer-attributes` with `access_logs.s3.enabled`, `create-flow-logs`) |
| **CloudWatch Logs delivery API** (source → destination → delivery) | `logs put-delivery-source` / `put-delivery-destination` / `create-delivery` |
Many services publish only to CloudWatch Logs; others use vended log delivery straight to S3
or Firehose. Some services need extra permissions first, or delivery fails: the catalog page
labels each service "V1 permissions" or "V2 permissions" and links the required policies.

## 2. Delivery API
```bash
aws logs put-delivery-source --name cf-access --resource-arn arn:aws:cloudfront::<ACCOUNT_ID>:distribution/E123 \
  --log-type ACCESS_LOGS --region us-east-1
aws logs put-delivery-destination --name cf-to-s3 \
  --delivery-destination-configuration destinationResourceArn=arn:aws:s3:::central-logs-<ACCOUNT_ID> \
  --output-format parquet
aws logs create-delivery --delivery-source-name cf-access \
  --delivery-destination-arn arn:aws:logs:us-east-1:<ACCOUNT_ID>:delivery-destination:cf-to-s3
aws logs describe-deliveries
```
- The log type is service-specific; take it from that service's logging page.
- Destination types are `S3`, `CWL` (CloudWatch Logs), `FH` (Firehose) and `XRAY`; output
  formats are `json`, `plain`, `w3c`, `raw` and `parquet`. `create-delivery` can also set
  `recordFields`, a field delimiter and, for S3, a suffix path and Hive-compatible paths.
- Cross-account: the destination account sets a delivery destination policy
  (`put-delivery-destination-policy`) for the source account.
- Even when logs go straight to S3 or Firehose, CloudWatch delivery charges apply; see the
  CloudWatch pricing page (Logs tab) rather than assuming a destination is cheaper.

## 3. Destination policies that must exist
- **S3 / Firehose / CloudWatch Logs**: the per-service policy in the catalog page's V1 or V2
  permissions link; use it rather than a hand-written policy.
- **ELB access logs (S3)**: the bucket must be in the load balancer's Region (it may belong to
  another account) and use SSE-S3 only (SSE-KMS is unsupported). Regions available before
  August 2022 used a Region-specific ELB account principal (legacy, still supported); the
  recommended policy grants the service principal `logdelivery.elasticloadbalancing.amazonaws.com`.
  A `Deny` that restricts service principals must allow that principal too, and `aws:SourceArn`
  can pin the bucket to one account and Region.

## 4. KMS for log groups
```bash
aws logs associate-kms-key --log-group-name /aws/vendedlogs/app --kms-key-id arn:aws:kms:<REGION>:<ACCOUNT_ID>:key/<KEY_ID>
```
Key policy statement (the service principal must be in the same Region as the key):
```json
{"Effect":"Allow","Principal":{"Service":"logs.<REGION>.amazonaws.com"},
 "Action":["kms:Encrypt","kms:Decrypt","kms:ReEncrypt*","kms:GenerateDataKey*","kms:Describe*"],
 "Resource":"*","Condition":{"ArnLike":{"kms:EncryptionContext:aws:logs:arn":"arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:*"}}}
```
- Use `ArnEquals` with one log group ARN to pin the key to a single log group.
- The caller of `AssociateKmsKey` (or `CreateLogGroup` with a key) needs `kms:DescribeKey` on the key.
- Only symmetric keys are supported. Only data ingested after association is encrypted with
  the key, and association changes can take up to five minutes to take effect.
- Revoking CloudWatch Logs' access to the key or deleting it makes encrypted data unretrievable.

## Gotchas
- Without the required permissions, delivery fails; check that objects or log events actually
  arrive, and for ELB the console/API reports a bucket-policy error on enable.
- ELB bucket-policy troubleshooting: the resource ARN must use the same bucket name (and no
  prefix if you did not set one) as the access-log setting.

## Verify
- [ ] `aws logs describe-deliveries` lists each intended source → destination.
- [ ] New objects/log events arrive within minutes of test traffic.
- [ ] `aws logs describe-log-groups --log-group-name-prefix /aws/vendedlogs/ --query 'logGroups[].kmsKeyId'` shows the CMK.
- [ ] A Config rule or scheduled check alarms on ALBs with `access_logs.s3.enabled=false`.

## Checked
2026-10-31. Confirmed against the botocore CloudWatch Logs model (`PutDeliverySource`, `PutDeliveryDestination`, `CreateDelivery` members, destination types, output formats), the "Enable logging from AWS services" catalog page (V1/V2 permissions, direct S3/Firehose delivery, delivery charges), the ALB access logging page (SSE-S3 only, same-Region bucket, August 2022 principal change, `access_logs.s3.*` attributes) and the CloudWatch Logs KMS page (key policy actions and encryption context, symmetric keys only, five-minute propagation, new data only). Removed as unconfirmed: the `delivery.logs.amazonaws.com` bucket and log-group policy details, the `AllowVendedLogDeliveryForResource` permission, resource-policy count limits, the `/aws/vendedlogs/` size-limit advice, the CloudFront legacy-logging remarks, and the vended-log pricing tiers.
Method: documentation only; no commands were run.
