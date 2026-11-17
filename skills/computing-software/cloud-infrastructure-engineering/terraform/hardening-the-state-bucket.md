---
id: computing-software.cloud-infrastructure-engineering.terraform.hardening-the-state-bucket
name: hardening-the-state-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-bucket-hardening, bucket-policy-state, s3-backend, kms, state-security]
level: practitioner
status: docs-checked
description: "Harden an S3 state bucket: KMS encryption through the backend, versioning with noncurrent expiry, Block Public Access, ACLs off, TLS-only policy, logging and per-object access."
sources:
  - "https://developer.hashicorp.com/terraform/language/backend/s3"
  - "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html"
  - "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening the state bucket (S3)

State can contain secrets; treat the bucket like a secrets store.

## Controls
| Control | Setting (source) |
|---|---|
| Encryption | Backend `encrypt = true` enables server-side encryption of the state and lock files; `kms_key_id` takes a KMS key ARN, and Terraform then needs `kms:Encrypt`, `kms:Decrypt` and `kms:GenerateDataKey` on that key (S3 backend page). Every S3 bucket already encrypts new objects by default with SSE-S3 (S3 best practices). |
| Versioning | Enable it. The backend page warns it is highly recommended, for state recovery after accidental deletions and human error. Versioning is off by default on a bucket and, once enabled, can only be suspended, not returned to unversioned (Versioning page). |
| Old versions | Versions are stored in full and billed per object version, so pair versioning with an S3 Lifecycle noncurrent-expiration rule if you want old versions (and any secrets in them) to age out. Choose the retention period yourself; the pages give no figure. |
| Public access | Use S3 Block Public Access; the best-practices page says to make sure a bucket is not public unless anyone on the internet must read or write it. |
| Object ownership | The bucket owner enforced setting disables ACLs and is the default for new buckets; AWS recommends it. Access is then governed by IAM, bucket, VPC endpoint, SCP and RCP policies. |
| Transport | Allow only HTTPS with the `aws:SecureTransport` condition in the bucket policy. |
| Least privilege | Grant only what a task needs. The backend page lists the minimum: `s3:ListBucket` on the bucket, `s3:GetObject` and `s3:PutObject` on the state key; with `use_lockfile` also `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on `<key>.tflock`. `s3:DeleteObject` is not needed on the state file. |
| Credentials | Use IAM roles, not long-lived keys stored in applications or instances. The backend page recommends environment variables for credentials, since `-backend-config` or hardcoded values land in `.terraform` and plan files. |
| Logging | Enable S3 server access logging, and consider CloudTrail data events (`GetObject`, `PutObject`, `DeleteObject`) for object-level audit. |
| Replication | Cross-Region Replication is optional and needs versioning on both buckets. |

## Bucket policy core (TLS only)
```json
{
  "Statement": [
    { "Sid": "DenyInsecureTransport", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
      "Resource": ["arn:aws:s3:::<STATE_BUCKET>", "arn:aws:s3:::<STATE_BUCKET>/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } } }
  ]
}
```
The `aws:SecureTransport` condition is named by the S3 best-practices page; the exact policy
text above is an illustration, so validate it (for example with IAM Access Analyzer) before use.

## Per-workspace and per-state access
The backend page notes that by default every user can read and write all workspaces'
state, and shows an IAM policy scoped to a single state object. If locking is on, include
the `<key>.tflock` object in the same access controls. Non-default workspaces live under
`<workspace_key_prefix>/<workspace_name>/<key>` (prefix defaults to `env:`).

## Object Lock
S3 Object Lock stores objects write-once-read-many and helps prevent accidental or
inappropriate deletion. Weigh that against your need to remove old versions that
contain leaked secrets; the pages do not settle this trade-off, so decide it deliberately.

## Detective controls
The best-practices page names AWS Config managed rules for several of these controls,
including `s3-bucket-ssl-requests-only`, `s3-bucket-versioning-enabled`,
`s3-bucket-logging-enabled` and `s3-bucket-public-read-prohibited`.

## Verify
- [ ] The bucket shows encryption, versioning and Block Public Access on in the console or CLI.
- [ ] A role without the state-key permissions (and without KMS access, if you set `kms_key_id`) is denied.

## Checked
Checked 2026-11-08 against the Terraform S3 backend page, the Amazon S3 security best
practices page and the S3 Versioning page. Removed: the 90-day expiry example, the
`s3:x-amz-server-side-encryption` deny statement, the claim that MFA delete or compliance-mode
Object Lock behave in specific ways, the GCS and Azure equivalents, and the `aws s3api`
verification commands, because those pages do not state them.
Method: docs-only read of cited pages, 2026-11-08
