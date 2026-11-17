---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.aws-cli-with-seaweedfs
name: aws-cli-with-seaweedfs
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [endpoint-url, signature-v4, presigned-url, aws-cli, presigned]
level: intro
status: docs-checked
description: "Use the AWS CLI against SeaweedFS S3: dummy keys, s3v4 signatures, --endpoint-url, common commands and the X-Forwarded-Prefix sub-path caveat."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/AWS-CLI-with-SeaweedFS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# aws cli with seaweedfs

Setup:
```bash
aws configure                       # region us-east-1
aws configure set default.s3.signature_version s3v4
export S3_ENDPOINT=http://localhost:8333
```
Commands (always pass the endpoint):
```bash
aws --endpoint-url $S3_ENDPOINT s3 ls
aws --endpoint-url $S3_ENDPOINT s3 mb s3://newbucket3
aws --endpoint-url $S3_ENDPOINT s3 cp /path/to/file s3://newbucket3
aws --endpoint-url $S3_ENDPOINT s3 cp s3://newbucket3/file s3://newbucket3/file.txt
aws --endpoint-url $S3_ENDPOINT s3 rm s3://newbucket3/file
aws --endpoint-url $S3_ENDPOINT s3 rb s3://newbucket3
```
When authentication is enabled, the URL is not accessible without credentials; `aws --endpoint-url $S3_ENDPOINT s3 presign s3://newbucket/t.txt` produces a URL you can use (default 1 hour).

Reverse-proxy sub-path (for example `/s3`) is undefined behavior for S3; if unavoidable, have the proxy send `X-Forwarded-Prefix: /s3` because the CLI prepends the sub-path.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page AWS CLI with SeaweedFS: region, s3v4 signature setting, command examples, presign, X-Forwarded-Prefix sub-path note. Removed the claim that keys can be anything and the Verify line.
Method: documentation only; no commands were run.
