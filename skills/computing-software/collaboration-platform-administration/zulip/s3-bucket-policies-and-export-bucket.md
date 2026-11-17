---
id: computing-software.collaboration-platform-administration.zulip.s3-bucket-policies-and-export-bucket
name: s3-bucket-policies-and-export-bucket
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [s3-bucket-policy, s3-export-bucket, iam-user, avatars-bucket]
level: advanced
status: docs-checked
description: "Write the IAM and bucket policies for Zulip's S3 uploads, avatar and data export buckets, and set S3_EXPORT_BUCKET with one-week download links."
sources: ["https://zulip.readthedocs.io/en/latest/production/upload-backends.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3 bucket policies and the export bucket

Use a dedicated IAM user with limited permissions. Each bucket needs a policy, built with the AWS policy generator.

Uploads bucket (not world-readable): two statements. First, Allow for `ARN_PRINCIPAL_HERE` on actions `s3:GetObject`, `s3:DeleteObject` and `s3:PutObject` with resource `arn:aws:s3:::BUCKET_NAME_HERE/*`. Second, Allow the same principal `s3:ListBucket` on `arn:aws:s3:::BUCKET_NAME_HERE`.

Avatars bucket: the same two statements plus a third that Allows principal `*` the action `s3:GetObject` on `arn:aws:s3:::BUCKET_NAME_HERE/*`, which makes avatars world-readable.

Data exports: when an export finishes (from the organization settings UI, or the command line with `--upload`) it is uploaded for download. With S3 enabled it lands in the avatars bucket by default, because that bucket is world-readable and download links are easy to produce.

For a dedicated bucket, set `S3_EXPORT_BUCKET` in `/etc/zulip/settings.py`. Give it the uploads-style policy, with write access only for the Zulip account. Zulip generates links valid for one week.

Copy existing exports across, for instance:

```
aws s3 sync s3://example-zulip-avatars/exports/ s3://example-zulip-exports/
```

Keep the uploads bucket private; only the avatars bucket is meant to be world-readable.

## Checked

2026-11-08. Checked: read against the Zulip upload-backends page (docs/production/upload-backends.md, read in full). Removed: a claim that Zulip itself checks file access and a public bucket would bypass it, which the page does not state.

Method: documentation only; no commands were run.
