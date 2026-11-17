---
id: computing-software.cloud-infrastructure-engineering.aws.s3-access-denied-troubleshooting
name: s3-access-denied-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-access-denied, s3-403, policy-evaluation-s3, kms-access-denied, troubleshooting]
level: practitioner
status: docs-checked
description: "Work through an S3 403 Access Denied systematically: identity policy, bucket policy, BPA, Object Ownership/ACLs, KMS key, endpoint policy, SCP/RCP and request details."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting S3 403 Access Denied

## 1. Read the error message first
S3 returns which policy type denied the request for same-account or same-organization
requests:
- `... because no identity-based policy allows the s3:GetObject action` (IAM side).
- `... with an explicit deny in a resource-based policy` (bucket policy).
- `... with an explicit deny in a service control policy` / `resource control policy`.
- `... with an explicit deny in a VPC endpoint policy`.
- `... because no session policy allows` (assumed role with session policy).
- `... because no permissions boundary allows` / `... with an explicit deny in a permissions boundary`.
Cross-account requests outside your organization get less detail. Also note the request ID from the error for support.

## 2. Confirm who is calling and what
```bash
aws sts get-caller-identity
aws s3api get-object --bucket b --key path/file.txt out.bin --debug 2>&1 | grep -E 'Making request|x-amz-request-id|403'
```
A wrong profile, wrong region, or path typo (S3 returns 403, not 404, when you lack
`s3:ListBucket`) explains many cases. With ListBucket permission a missing key returns 404.

## 3. Checklist in evaluation order
1. **SCP/RCP**: org-level denies (region restrictions, data perimeter `aws:PrincipalOrgID`,
   `aws:SourceVpce`).
2. **Bucket policy explicit denies**: TLS-only (`aws:SecureTransport`), encryption
   required headers (`s3:x-amz-server-side-encryption`), VPC endpoint-only, IP restrictions,
   `aws:PrincipalArn` allow-lists.
   `aws s3api get-bucket-policy --bucket b --query Policy --output text | jq .`
3. **Block Public Access**: blocks public policies/ACLs (`get-public-access-block` at
   bucket and account). Only matters for anonymous/public grants.
4. **Identity policy** of the caller allows the action **on the right ARN**: bucket-level
   actions (`s3:ListBucket`) need `arn:aws:s3:::b`; object actions need `arn:aws:s3:::b/*`.
5. **Permission boundary / session policy** on the role.
6. **Cross-account**: both the bucket policy (granting the other account/role) and the
   caller's IAM policy are needed.
7. **Object Ownership / ACLs**: with `BucketOwnerEnforced` ACLs are ignored (good). With
   older settings, objects uploaded by another account are owned by that account and the
   bucket owner cannot read them; fix by switching to `BucketOwnerEnforced`, which
   makes the bucket owner own every object.
8. **KMS**: SSE-KMS objects also need `kms:Decrypt` (and `kms:GenerateDataKey` for
   uploads) on the key, granted by key policy + IAM. S3 surfaces this as 403 AccessDenied.
9. **VPC endpoint policy** on the gateway/interface endpoint the request goes through.
10. **Access points**: requests via an access point need the access point policy and the
    bucket policy delegating to access points.
11. **Requester Pays** buckets need `--request-payer requester`.
12. **Object Lock / legal hold** cause 403 on delete of protected versions.

## 4. Tools
- CloudTrail data events (if enabled) for the request show `errorCode` and the principal.
- IAM policy simulator to test identity-based policies, permissions boundaries, SCPs and resource-based
  policies (its results can differ from the live environment).
- S3 server access logs show `AccessDenied` with the requester ARN.

## Gotchas
- A bucket policy that requires SSE-KMS denies uploads that do not send the encryption header
  (for the CLI, `--sse aws:kms`).
- A presigned URL is authorized with the permissions of the IAM user or role that signed it, so check
  that identity's policies.
- `aws:SourceIp` cannot be used for requests that traverse a VPC endpoint; use
  `aws:SourceVpce`, `aws:SourceVpc` or `aws:VpcSourceIp` for those.

## Verify
- [ ] Root cause identified by the specific denying policy type, fix applied to that policy only.
- [ ] Request succeeds with the intended principal; an unintended principal still fails.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Troubleshoot access denied (403 Forbidden) errors and Amazon S3 policy keys, and the S3 API reference for GetObject.
Confirmed: the access denied message formats (no identity-based, resource-based, SCP, RCP, VPC endpoint, session policy and permissions boundary policy, and the "explicit deny in a ..." forms); the extra context applies to same-account or same-organization requests; a missing ListBucket permission returns 403 and a missing key with ListBucket returns 404; SSE-KMS permission requirements; Requester Pays needs `--request-payer requester`; Object Lock retention blocks deletes; the gateway endpoint page states aws:SourceIp cannot be used for traffic through a VPC endpoint.

Method: documentation only; no commands were run.
