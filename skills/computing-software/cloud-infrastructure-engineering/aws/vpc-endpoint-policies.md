---
id: computing-software.cloud-infrastructure-engineering.aws.vpc-endpoint-policies
name: vpc-endpoint-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vpc-endpoints, endpoint-policy, endpoint-policies, vpce-condition, data-perimeter, aws-principalorgid, s3]
level: practitioner
status: docs-checked
description: "Write VPC endpoint policies and matching resource-side conditions (aws:SourceVpce, aws:PrincipalOrgID, aws:ResourceOrgID) to build a data perimeter against exfiltration."
sources: ["https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies-vpc-endpoint.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://github.com/aws-samples/data-perimeter-policy-examples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC endpoint policies (data perimeter)

Two directions, two policies:
- **Endpoint policy** (on the endpoint): which principals may reach which resources *through
  this endpoint* → stops insiders copying data to a personal bucket.
- **Resource policy condition** (on the bucket/queue/key): only accept requests *from these
  endpoints/VPCs* → stops stolen credentials being used from outside.

## 1. Endpoint policy: only our org's principals and resources
```json
{"Version": "2012-10-17", "Statement": [
 {"Sid": "OrgOnly", "Effect": "Allow", "Principal": "*", "Action": "*", "Resource": "*",
  "Condition": {"StringEquals": {"aws:PrincipalOrgID": "o-abc123", "aws:ResourceOrgID": "o-abc123"}}},
 {"Sid": "AwsOwnedBuckets", "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject",
  "Resource": ["arn:aws:s3:::prod-<REGION>-starport-layer-bucket/*"]}]}
```
```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id vpce-s3gw --policy-document file://s3-endpoint-policy.json
```
The second statement keeps ECR image layers (served from an AWS-owned bucket, as in the ECR endpoint policy example) working. Other AWS-owned buckets your workloads use (for example OS package repositories) may need similar statements; check each service's documentation.

## 2. Resource side: bucket accepts only via our endpoints
```json
{"Sid": "DenyOutsideVpce", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::payroll-data", "arn:aws:s3:::payroll-data/*"],
 "Condition": {"StringNotEquals": {"aws:SourceVpce": ["vpce-0aaa", "vpce-0bbb"]},
               "BoolIfExists": {"aws:ViaAWSService": "false"},
               "ArnNotLike": {"aws:PrincipalArn": "arn:aws:iam::<ACCOUNT_ID>:role/break-glass"}}}
```
`aws:SourceVpce` / `aws:SourceVpc` apply to requests made through a VPC endpoint. For S3 requests that traverse a VPC endpoint you cannot use `aws:SourceIp` in identity or bucket policies; use `aws:VpcSourceIp` instead.

## 3. Checklist
- An endpoint policy does not override or replace identity-based or resource-based policies; IAM must still allow the request.
- An endpoint policy is JSON in the IAM language, must contain a `Principal` element, and is limited to 20,480 characters. The default policy allows full access. For gateway endpoints `Principal` must be `*`; use `aws:PrincipalArn` to name a principal. After an update, allow a few minutes.
- Not all services support endpoint policies; for a service that does not, any endpoint allows full access.
- You cannot use wildcards with global context keys that hold system-generated identifiers (for example `aws:PrincipalAccount` or `aws:SourceVpc`).
- Apply perimeter conditions org-wide with SCPs or resource control policies rather than bucket by bucket when possible.

## Gotchas
- A bucket policy that limits access to a VPC endpoint can block all other connections to the bucket, including your own console and laptop access (the S3 guide warns about this) — include an
  admin/break-glass exception and `aws:ViaAWSService` for AWS services acting on your behalf.
- Gateway endpoint policies apply to all route tables using that endpoint — test in a non-prod VPC.

## Verify
- [ ] From inside the VPC, `aws s3 cp s3://payroll-data/x .` works; from a laptop with the same role it is denied.
- [ ] Copy to a bucket in another org via the endpoint fails with AccessDenied (explicit deny in VPC endpoint policy / not allowed).
- [ ] `dnf update` and ECR pulls still succeed after the endpoint policy change.

## Checked

Checked 2026-10-27 against the VPC PrivateLink guide (endpoint policies, gateway endpoints for S3, ECR interface endpoints), the S3 guide (bucket policies for VPC endpoints) and the IAM global condition keys page.
- Endpoint policy rules (size limit, `Principal` required, default policy, gateway endpoint `Principal` must be `*`, `aws:PrincipalArn`, wildcard restriction, services without support allow full access) confirmed on the endpoint policies page.
- `aws:SourceIp` unusable and `aws:VpcSourceIp` for S3 requests through endpoints confirmed on the S3 gateway endpoint page; the lock-out warning confirmed on the S3 bucket policy page.
- The condition keys `aws:PrincipalOrgID`, `aws:ResourceOrgID`, `aws:SourceVpce`, `aws:ViaAWSService` and the ECR layer bucket `prod-<REGION>-starport-layer-bucket` appear in the AWS pages read. `modify-vpc-endpoint --policy-document` (the `PolicyDocument` member) confirmed in the service model.
- Removed the Amazon Linux repository bucket names, which no page read lists.

Method: documentation only; no commands were run.
