---
id: computing-software.systems-network-administration.restic.s3-iam-setup
name: s3-iam-setup
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, s3, iam, bucket-policy, aws, least-privilege]
level: practitioner
status: docs-checked
description: "Create a least-privilege AWS IAM user and policy for a restic S3 bucket, initialise the repository and run a test backup and restore."
sources:
  - https://restic.readthedocs.io/en/stable/080_examples.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restic with Amazon S3: IAM setup

Create the bucket first (the tutorial uses `restic-demo`), then an IAM user with programmatic access and this policy.

## Policy

Two statements:

1. Service S3, actions `DeleteObject`, `GetObject`, `PutObject`, on resource `arn:aws:s3:::restic-demo/*`
2. Service S3, actions `ListBucket`, `GetBucketLocation`, on resource `arn:aws:s3:::restic-demo` (no `/*`)

Save the access key ID and secret key securely.

## Initialise

Generate a long random password (the tutorial uses `apg -a 1 -m 32 -n 1 -M NCL`) and keep secrets out of shell history:

```
unset HISTFILE
export RESTIC_REPOSITORY="s3:s3.eu-west-1.amazonaws.com/restic-demo"
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export RESTIC_PASSWORD=...
restic init
```

## Smoke test

```
dd if=/dev/urandom bs=1M count=10 of=test.bin
restic backup test.bin
restic snapshots
mkdir restore
restic restore <snapshot-id> --target restore
```

Choose a storage class with `-o s3.storage-class=...` on the backup command.

Use your own bucket name: the tutorial notes that the bucket name space is shared among all AWS users, so `restic-demo` may not be available.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing Amazon S3 for restic (Examples): bucket `restic-demo`, programmatic access user, the two policy statements with their actions and resources (no `/*` on the second), the `apg` password command, `unset HISTFILE`, the init, 10 MiB `dd` test, backup, snapshots and restore steps, and the `s3.storage-class` option. Removed: the claim that holders of only the AWS keys cannot read data (the policy grants `GetObject`).

Method: documentation only; no commands were run.
