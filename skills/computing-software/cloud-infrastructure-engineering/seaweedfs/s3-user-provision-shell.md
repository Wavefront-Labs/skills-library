---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-user-provision-shell
name: s3-user-provision-shell
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [iam, weed-shell, s3-user-provision, readwrite-role, access-key]
level: intro
status: docs-checked
description: "Create a bucket, an IAM user with generated keys and a bucket-scoped policy in weed shell using s3.bucket.create and s3.user.provision."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Simplest-S3-Bucket-and-User-Setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 user provision shell

Goal: least-privilege S3 access for one user on one bucket.

```
weed shell
> s3.bucket.create -name my-bucket
> s3.user.provision -name alice -bucket my-bucket -role readwrite
```

`s3.user.provision` does three things: creates a policy scoped to the bucket, creates the user with a fresh access/secret key (printed in the shell; also visible in the Admin UI on port 12535), and attaches the policy.

Roles:
- `readonly`: s3:GetObject plus s3:ListBucket
- `readwrite`: GetObject, PutObject, DeleteObject plus ListBucket
- `admin`: s3:* on the bucket

Only the named bucket is granted. Re-running for an existing user attaches the new bucket policy to that user instead of creating a duplicate.

Gotcha: once any credential exists, the gateway leaves "Allow All" mode and rejects unauthenticated requests.

Use the keys:
```bash
export AWS_ACCESS_KEY_ID=<printed> AWS_SECRET_ACCESS_KEY=<printed>
aws --endpoint-url http://localhost:8333 s3 cp ./file.txt s3://my-bucket/
```

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page Simplest S3 Bucket and User Setup: commands, the three steps, role table, Admin UI port 12535, Allow-All to authenticated switch. Reworded the existing-user sentence to match the page; removed the Verify line.
Method: documentation only; no commands were run.
