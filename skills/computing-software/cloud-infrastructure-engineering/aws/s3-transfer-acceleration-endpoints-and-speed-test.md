---
id: computing-software.cloud-infrastructure-engineering.aws.s3-transfer-acceleration-endpoints-and-speed-test
name: s3-transfer-acceleration-endpoints-and-speed-test
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, accelerate-endpoint, transfer-acceleration, upload-performance]
level: practitioner
status: docs-checked
description: "Enable S3 Transfer Acceleration, point the CLI and SDKs at the accelerate endpoint, and measure the benefit with the speed comparison tool before paying for it."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration-examples.html", "https://docs.aws.amazon.com/cli/latest/topic/s3-config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transfer Acceleration endpoints and speed comparison

## 1. Enable
```bash
aws s3api put-bucket-accelerate-configuration --bucket uploads-prod --accelerate-configuration Status=Enabled
aws s3api get-bucket-accelerate-configuration --bucket uploads-prod
```
Requirements: virtual-hosted-style requests only, a DNS-compliant bucket name without periods, and a bucket in a Region that supports acceleration (check the current Region list on the Transfer Acceleration page). Speed can take up to 20 minutes to improve after enabling. ListBuckets, CreateBucket and DeleteBucket are not sent to the accelerate endpoint.

## 2. Use the endpoint
- Endpoint: `https://<bucket>.s3-accelerate.amazonaws.com` (dual-stack: `s3-accelerate.dualstack.amazonaws.com`).
- CLI:
```bash
aws configure set default.s3.use_accelerate_endpoint true
aws s3 cp big.bin s3://uploads-prod/        # or per command:
aws s3 cp big.bin s3://uploads-prod/ --endpoint-url https://s3-accelerate.amazonaws.com
```
- SDKs: boto3 `Config(s3={'use_accelerate_endpoint': True})`; for other SDKs check their S3 client option.

## 3. Measure first
Run the Amazon S3 Transfer Acceleration Speed Comparison tool from the clients' locations; it compares
direct vs accelerated uploads per Region. Gains are largest for long-distance, high-latency uploads of
large objects; nearby clients see little or none.
Additional data transfer charges can apply when you use Transfer Acceleration (see S3 pricing), so test first.

## 4. Combine with multipart
Parallel multipart parts (`multipart_chunksize`, `max_concurrent_requests`) plus acceleration for big files.

## Verify
- [ ] Timed upload from a distant client: accelerated vs standard, recorded before rollout.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Transfer Acceleration and Enabling and using S3 Transfer Acceleration, the AWS CLI S3 configuration topic, and the botocore config source.
Confirmed: PutBucketAccelerateConfiguration Status Enabled or Suspended; endpoint https://<bucket>.s3-accelerate.amazonaws.com and the dualstack form; use_accelerate_endpoint profile setting and --endpoint-url https://s3-accelerate.amazonaws.com; requirements (virtual-hosted style, DNS-compliant name without periods, up to 20 minutes before speed improves, limited Region list); Speed Comparison tool uses multipart upload to compare direct and accelerated uploads; multipart_chunksize and max_concurrent_requests are AWS CLI S3 settings; botocore Config s3 use_accelerate_endpoint. Removed the unconfirmed conditional-charge statement and unverified SDK options.

Method: documentation only; no commands were run.
