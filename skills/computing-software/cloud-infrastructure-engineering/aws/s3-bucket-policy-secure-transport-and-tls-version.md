---
id: computing-software.cloud-infrastructure-engineering.aws.s3-bucket-policy-secure-transport-and-tls-version
name: s3-bucket-policy-secure-transport-and-tls-version
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, secure-transport, tls-version-condition, bucket-policy, encryption-in-transit, data-perimeter]
level: practitioner
status: docs-checked
description: "Enforce encryption in transit on S3 with aws:SecureTransport and s3:TlsVersion bucket policy denies, add perimeter conditions safely, and avoid locking out services."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/s3-controls.html", "https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-ssl-requests-only.html", "https://aws.amazon.com/blogs/security/tls-1-2-required-for-aws-endpoints/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 bucket policy: SecureTransport and TLS version

## 1. Deny plain HTTP
```json
{"Sid": "DenyInsecureTransport", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::data-bucket", "arn:aws:s3:::data-bucket/*"],
 "Condition": {"Bool": {"aws:SecureTransport": "false", "aws:PrincipalIsAWSService": "false"}}}
```
Setting `aws:PrincipalIsAWSService` to false keeps AWS service principals out of the deny: network-specific
context (`aws:SecureTransport`, `s3:TlsVersion`, `aws:SourceIp`, `aws:VpcSourceIp`) is redacted on
service-to-service calls, so an unqualified deny can block them (S3 policy keys page).
Targets Security Hub `S3.5` and Config rule `s3-bucket-ssl-requests-only` (re-run both after adding the
service-principal condition). This blocks clients using `http://` endpoints and S3 website
endpoints (which are HTTP only: use CloudFront in front instead).

## 2. Require a minimum TLS version
```json
{"Sid": "DenyOldTLS", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::data-bucket", "arn:aws:s3:::data-bucket/*"],
 "Condition": {"NumericLessThan": {"s3:TlsVersion": "1.2"}}}
```
AWS API endpoints, including S3, ended TLS 1.0 and 1.1 support (AWS Security Blog reports the
global rollout complete on 27 February 2024), so this is mostly defence in depth and documentation for auditors; set `1.3` only
if every client supports it. Find client TLS versions in CloudTrail data events
(`tlsDetails.tlsVersion`) or server access logs (`TLS version` field) before tightening.

## 3. Common companions (all as Deny statements)
- To require encryption at rest, prefer default encryption (with a bucket key for SSE-KMS)
  over a `s3:x-amz-server-side-encryption` header condition, which forces every client to send the header.
- Enforce a specific KMS key with a condition on the `x-amz-server-side-encryption-aws-kms-key-id`
  request header (confirm the exact condition key name in the S3 condition keys reference).
- Network perimeter: deny unless `aws:SourceVpce` is one of yours, and exclude AWS service
  principals (such as CloudTrail or Config writing logs) with `aws:PrincipalIsAWSService` false.
- Identity perimeter: deny unless `aws:PrincipalOrgID` is your org (exempt AWS service
  principals with `aws:PrincipalIsAWSService` false in the same deny).

## 4. Avoid lockouts
- A Deny on `s3:*` with conditions that your own admin role fails (e.g. a VPC endpoint
  condition while you work from a laptop) locks you out of fixing the policy. Exempt a
  break-glass role with `ArnNotLike aws:PrincipalArn`, or rely on the root user /
  `AssumeRoot` task `S3UnlockBucketPolicy` to delete the policy.
- Test changes on a copy bucket with the same policy first.
- Log delivery and other AWS service callers: AWS documents that network-specific condition keys
  are redacted on service-to-service calls, so every Deny that uses `aws:SecureTransport`,
  `s3:TlsVersion`, `aws:SourceIp` or `aws:VpcSourceIp` should carry the `aws:PrincipalIsAWSService`
  false exclusion.

## 5. Apply
```bash
aws s3api put-bucket-policy --bucket data-bucket --policy file://policy.json
aws s3api get-bucket-policy-status --bucket data-bucket   # IsPublic should be false
```
Validate with Access Analyzer (`aws accessanalyzer validate-policy --policy-type
RESOURCE_POLICY --validate-policy-resource-type AWS::S3::Bucket --policy-document file://policy.json`).

## Verify
- [ ] `curl -I http://data-bucket.s3.eu-west-1.amazonaws.com/x` (HTTP) returns 403; HTTPS works for authorised callers.
- [ ] Security Hub S3.5 passes for the bucket.
- [ ] Break-glass access path tested before rolling the policy to production buckets.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Amazon S3 condition keys (policy keys) and Security best practices, the Security Hub S3 controls page, the AWS Config rule page for s3-bucket-ssl-requests-only, the S3 server access log format page, the CloudTrail record contents page, the AWS Security Blog post on TLS 1.2 and the botocore s3 model.
Confirmed: s3:TlsVersion exists with numeric conditions and the NumericLessThan 1.2 example; the S3 policy keys note about redacted context on service-to-service calls and the aws:PrincipalIsAWSService false exclusion; Security Hub control S3.5 (S3 general purpose buckets should require requests to use TLS); Config rule s3-bucket-ssl-requests-only (S3_BUCKET_SSL_REQUESTS_ONLY); server access log field TLS version (TLSv1.1 to TLSv1.3) and CloudTrail tlsDetails.tlsVersion; GetBucketPolicyStatus returns IsPublic; TLS 1.0 and 1.1 deprecation completed 27 February 2024. Website endpoints do not support HTTPS (WebsiteEndpoints page). Removed the unconfirmed KMS condition key spelling.

Method: documentation only; no commands were run.
