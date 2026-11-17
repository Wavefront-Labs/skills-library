---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-synthetics-canaries-in-vpc-artifacts-and-alarms
name: cloudwatch-synthetics-canaries-in-vpc-artifacts-and-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-synthetics, canary-vpc, canary-artifacts, canaries, synthetic-monitoring, successpercent]
level: practitioner
status: docs-checked
description: "Run CloudWatch Synthetics canaries against private endpoints in a VPC, manage canary artifacts and retention in S3, and alarm on SuccessPercent and Duration."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_artifact_encryption.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetics canaries in a VPC, artifacts and alarms

## VPC canaries
```bash
aws synthetics create-canary --name internal-api --runtime-version <RUNTIME_VERSION> \
  --artifact-s3-location s3://<ARTIFACT_BUCKET>/internal-api/ \
  --execution-role-arn "$ROLE" --schedule Expression="rate(5 minutes)" \
  --code Handler=index.handler,S3Bucket=<CODE_BUCKET>,S3Key=internal-api.zip \
  --vpc-config SubnetIds=subnet-a,subnet-b,SecurityGroupIds=sg-canary
```
Take `<RUNTIME_VERSION>` from the AWS "Synthetics runtime versions" page.
- Canaries can run against endpoints in a VPC and public endpoints. The VPC needs both DNS resolution and DNS
  hostnames enabled.
- A canary in a VPC must still send metrics to CloudWatch and artifacts to S3. If the VPC already has internet
  access, nothing more is needed. Otherwise either:
  - give IPv4 internet access: NAT gateway in a public subnet plus a `0.0.0.0/0` route to it in the private subnet's
    route table (a deleted NAT gateway leaves the route in `blackhole` status), or
  - keep the VPC private: create a CloudWatch interface endpoint (`com.amazonaws.<REGION>.monitoring`) and an S3
    gateway endpoint.
- IPv6: dual-stack subnets, an egress-only internet gateway, route and security group updates, and
  `Ipv6AllowedForDualStack` in the canary VPC configuration (`CreateCanary` or `UpdateCanary`).
- `VpcConfig` accepts up to 16 subnet ids and 5 security group ids (botocore model).

## Artifacts
- Screenshots, HAR files and reports are stored in your S3 bucket, encrypted at rest with an AWS managed key by
  default (no extra permissions).
- Encryption options: SSE-S3 (`SSE_S3`, no extra permissions) or SSE-KMS with a customer managed key ARN (a
  cross-account key is allowed). For a customer managed key the canary's IAM role needs `kms:GenerateDataKey` and
  `kms:Decrypt` (decrypt is needed for visual monitoring), either in the role policy or by adding the role to the key
  policy. Anyone viewing artifacts needs decrypt permission on the key.
- `--success-retention-period-in-days` and `--failure-retention-period-in-days` accept 1 to 1024 days (botocore
  model; it controls run metadata retention).
- If you change the artifact location or encryption with visual monitoring, either keep the role's permissions for
  both old and new locations and keys, or select the next run as a new baseline (the AWS recommendation).
- Store credentials in Secrets Manager, not in the script.

## Alarms
Namespace `CloudWatchSynthetics`, dimension `CanaryName` (SuccessPercent and Duration also support `Browser` and
`Location`). `SuccessPercent` is the percentage of runs that succeed with no failures (statistic Average, percent);
`Duration` is run time in milliseconds (statistic Average).
```bash
aws cloudwatch put-metric-alarm --alarm-name internal-api-canary \
  --namespace CloudWatchSynthetics --metric-name SuccessPercent \
  --dimensions Name=CanaryName,Value=internal-api --statistic Average \
  --period 300 --evaluation-periods 3 --datapoints-to-alarm 2 \
  --threshold 90 --comparison-operator LessThanThreshold \
  --treat-missing-data breaching --alarm-actions "$TOPIC"
```
- Thresholds, period and `breaching` for missing data are design choices, not AWS defaults.
- Canaries that use `executeStep()` or `executeHttpStep()` also publish `SuccessPercent` and `Duration` per step with
  dimensions `CanaryName` and `StepName`.
- Other metrics: `Failed` (runs that failed to execute), `SuccessPercentWithRetries`, `RetryCount`, and
  `2xx`/`4xx`/`5xx` counts.

## Verify
- [ ] Canary succeeds against the private endpoint; artifacts appear in S3.
- [ ] Break the target: `SuccessPercent` drops and the alarm fires.

## Checked
2026-11-08. Confirmed against the CloudWatch User Guide pages on running a canary on a VPC, encrypting canary
artifacts and canary metrics; request fields checked against the botocore model. Corrected: retention range is 1 to
1024 days (the draft said 1-455). Removed: the specific runtime version, Lambda ENI permission list, S3 lifecycle and
screenshot-config advice, and the "1-455" and 15-minute alarm claims, which the pages do not state.
Method: docs-only read of cited pages, 2026-11-08
