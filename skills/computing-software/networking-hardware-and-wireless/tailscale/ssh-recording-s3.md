---
id: computing-software.networking-hardware-and-wireless.tailscale.ssh-recording-s3
name: ssh-recording-s3
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [ssh-recording, session-recorder, s3-policy]
level: advanced
status: docs-checked
description: "Configure recorder nodes to write Tailscale SSH recordings to S3-compatible storage."
sources: ["https://tailscale.com/kb/1263"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH session recording to S3

Goal: send Tailscale SSH recordings to object storage.

The feature is described as beta and needs Tailscale v1.40.1 or later. Recorder nodes can write to Amazon S3 or S3-compatible storage such as MinIO, Wasabi, Google Cloud Storage or Cloudflare R2. If a recorder runs with the built-in web UI, users can view recordings stored in S3 there.

**AWS prerequisites.** Permission to create S3 buckets, IAM policies, and either IAM users with access keys or an IAM role.

**IAM policy** (replace `<bucket-name>` on both Resource lines):
```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:PutObject", "s3:GetBucketLocation",
               "s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::<bucket-name>/*",
                 "arn:aws:s3:::<bucket-name>"]
  }]
}
```
`s3:PutObject` and `s3:GetBucketLocation` are always required. If recorders run without the web UI you can omit `s3:GetObject` and `s3:ListBucket`.

Attach the policy to a new IAM user (for access keys) or to a role.

**Checklist**

1. Bucket created.
2. Policy scoped to that bucket.
3. Web UI needs read actions.

## Checked

2026-11-03. Read SSH session recording (kb/1263) and confirmed beta status, v1.40.1, S3-compatible stores, the IAM policy and the required actions. Nothing else was removed.

Method: documentation only; no commands were run.
