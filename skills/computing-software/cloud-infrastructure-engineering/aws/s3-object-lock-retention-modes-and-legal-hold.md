---
id: computing-software.cloud-infrastructure-engineering.aws.s3-object-lock-retention-modes-and-legal-hold
name: s3-object-lock-retention-modes-and-legal-hold
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, object-lock, governance-mode, compliance-mode, legal-hold, worm, ransomware-protection, default-retention, object-lock-existing-bucket]
level: practitioner
status: docs-checked
description: "Make S3 data immutable with Object Lock: governance vs compliance mode, default retention, legal holds, bypass permissions, enabling on existing buckets, and test-before-commit."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# S3 Object Lock: governance, compliance and legal hold

## 1. Modes
| | Governance | Compliance |
|---|---|---|
| Delete/overwrite version before retain-until | only with `s3:BypassGovernanceRetention` + `x-amz-bypass-governance-retention:true` | **no user**, including root (only deleting the AWS account removes it) |
| Shorten retention | with bypass permission | no (mode cannot change, period cannot be shortened) |
| Use | internal protection, testing retention settings | WORM storage for regulated data, ransomware vault |
**Legal hold**: independent on/off flag, no expiry, blocks deletion of that version until
removed by a user with `s3:PutObjectLegalHold`; it is independent of retention, and bypassing governance mode does not remove it.
Object Lock was assessed by Cohasset Associates for SEC 17a-4, CFTC and FINRA environments; whether it satisfies a specific regulation for your data is for your compliance advisers to decide.

## 2. Enable
New bucket: `aws s3api create-bucket --bucket vault --object-lock-enabled-for-bucket` (plus a `--region`/`--create-bucket-configuration` where needed).
Existing bucket (Object Lock works only on versioned buckets): `aws s3api put-object-lock-configuration` with
`ObjectLockEnabled: Enabled` — after enabling you can't disable Object Lock or suspend versioning.
Default retention:
```bash
aws s3api put-object-lock-configuration --bucket vault --object-lock-configuration \
  '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":{"Mode":"GOVERNANCE","Days":30}}}'
```
Per object:
```bash
aws s3api put-object-retention --bucket vault --key db/2026-10-16.dump --version-id v1 \
  --retention '{"Mode":"COMPLIANCE","RetainUntilDate":"2033-10-16T00:00:00Z"}'
aws s3api put-object-legal-hold --bucket vault --key case-4411/mail.pst --legal-hold Status=ON
```

## 3. Test before compliance
Start with **governance** mode and short periods; verify that apps, lifecycle and replication
behave; then switch default retention to compliance. A compliance-mode mistake (e.g. 10 years
on terabytes of temp data) cannot be undone — you pay for storage until it expires or the
account is closed.

## 4. Bypass governance (admins only)
```bash
aws s3api delete-object --bucket vault --key x --version-id v1 --bypass-governance-retention
```
Restrict `s3:BypassGovernanceRetention` to a break-glass role; deny it org-wide otherwise.

## Gotchas
- Lock protects **versions**: a plain DELETE still adds a delete marker (object "disappears"
  from listings) but the locked version remains recoverable.
- Lifecycle keeps working on locked objects (including delete markers) but cannot delete a locked version until the lock ends. Delete markers are not WORM-protected.
- Replication of locked objects requires Object Lock on the destination too, and the replication role needs `s3:GetObjectRetention` and `s3:GetObjectLegalHold` on the source.
- Batch Operations can apply retention (`S3PutObjectRetention`) and legal holds (`S3PutObjectLegalHold`) to existing objects in bulk.
- An upload with a retention period set needs a `Content-MD5` or `x-amz-sdk-checksum-algorithm` header.
- A bucket with Object Lock cannot be the destination for server access logs. Object Lock does not protect against loss or deletion of KMS keys.

## Verify
- [ ] `aws s3api get-object-retention` shows mode/date on new objects (default retention).
- [ ] Deleting a version under compliance mode fails with `403` (AccessDenied) even as admin.
- [ ] Legal hold on → deletion denied; off → allowed (after retention).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: governance vs compliance semantics (root cannot override compliance; only deleting the account removes it), `s3:BypassGovernanceRetention` plus header, legal hold independence, versioning requirement and irreversibility, create-bucket and put-object-lock-configuration CLI forms, default retention JSON (botocore), replication permissions and destination requirement, lifecycle and delete-marker behaviour, checksum header requirement, Cohasset assessment wording. Retention decisions for regulated data remain the owner's and their compliance advisers'.

Method: documentation only; no commands were run.
