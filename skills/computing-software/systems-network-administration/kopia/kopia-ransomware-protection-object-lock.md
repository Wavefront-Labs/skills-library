---
id: computing-software.systems-network-administration.kopia.kopia-ransomware-protection-object-lock
name: kopia-ransomware-protection-object-lock
category: computing-software
field: systems-network-administration
product: kopia
tags: [ransomware, object-lock, compliance-mode, restricted-keys, point-in-time, s3]
level: advanced
status: docs-checked
description: "Protect Kopia repositories on S3-compatible storage with restricted keys, object lock in compliance mode and point-in-time recovery."
sources: ["https://kopia.io/docs/advanced/ransomware-protection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kopia can use provider features to make deleted or encrypted backups recoverable. S3 supports both restricted access keys and object locks; Backblaze B2's native engine supports restricted keys but not locks (use the S3 engine for locks); Azure and Google engines support object locks. GCS lacks sufficient S3-compatible access controls.

## Restricted keys

Create a key that cannot delete. On AWS, create an IAM user with a policy that denies `s3:DeleteBucket`, `s3:DeleteBucketPolicy`, `s3:DeleteBucketWebsite` and `s3:DeleteObjectVersion`, create an access key, reconnect Kopia with it, delete the root key, and set a bucket lifecycle expiration to your protection window. On Backblaze create a restricted key with the `b2` CLI limited to one bucket. Enable MFA on the account.

## Object lock

Locks must be enabled when the bucket is created (Backblaze S3 can enable them on an existing bucket with `b2 update bucket`) and can never be disabled. A default retention is not needed.

```console
kopia repo create s3 --bucket BUCKET --access-key=KEY --secret-access-key=SECRET --retention-mode COMPLIANCE --retention-period 30d
kopia maintenance set --extend-object-locks true
```

Compliance mode means even root cannot delete before the date. Kopia does not renew locks unless you enable extension in full maintenance, and `full-interval` must be at least one day shorter than the retention period or Kopia refuses to enable it; run full maintenance at least that often or locks expire.

## Recovery

Disconnect and reconnect with `--point-in-time=2021-11-29T01:10:00.000Z` (S3 repositories only), making sure the retention or lifecycle window has not removed what you need. Ransomware can lurk for weeks encrypting rarely used files first, so keep retention longer than your detection time.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Ransomware Protection page (provider support, IAM deny policy actions, lifecycle expiration, Backblaze b2 key, object-lock caveats, retention flags, extend-object-locks, full-interval rule, --point-in-time for s3 only).
Method: documentation only; no commands were run.
