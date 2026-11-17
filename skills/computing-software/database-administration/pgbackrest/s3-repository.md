---
id: computing-software.database-administration.pgbackrest.s3-repository
name: s3-repository
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, s3, object-store, repo-s3, iam-role]
level: practitioner
status: docs-checked
description: "Configure an S3-compatible repository, key types, and a restrictive bucket policy."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store the repository in S3.

The bucket must exist before use; pgBackRest does not create it. The repository can sit in the bucket root, but a subpath is usually better so logs or other data can share the bucket.

```
[global]
repo3-type=s3
repo3-path=/demo-repo
repo3-s3-bucket=demo-bucket
repo3-s3-endpoint=s3.us-east-1.amazonaws.com
repo3-s3-region=us-east-1
repo3-s3-key=<access key>
repo3-s3-key-secret=<secret key>
repo3-retention-full=4
```

Region and endpoint must match where the bucket lives (the endpoint should be valid for the region).

`repo-s3-key-type` (default `shared`): `shared`, `auto` (temporary credentials from the instance role, so no keys in the file), `web-id`, `pod-id` (EKS pod identity) or `process` (run `repo-s3-process-cmd`). `repo-s3-role` is the role name, not the full ARN, used with `auto`. `repo-s3-uri-style` is `host` (default) or `path`.

Create a dedicated role and set bucket permissions as restrictively as possible. The guide's policy allows `s3:ListBucket` on the bucket for the repository prefix, and `s3:PutObject`, `s3:PutObjectTagging`, `s3:GetObject`, `s3:GetObjectVersion` and `s3:DeleteObject` only on the repository path.

File creation is slow on S3, so enable bundling.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (S3-Compatible Object Store Support, sample bucket policy). Nothing needed removing. 

Method: documentation only; no commands were run.
