---
id: computing-software.systems-network-administration.restic.s3-backend
name: s3-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, s3, amazon-s3, aws, backend, credentials]
level: practitioner
status: docs-checked
description: "Configure restic against Amazon S3 with path-style URLs and AWS credential environment variables, including session tokens and storage class."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
  - https://restic.readthedocs.io/en/stable/080_examples.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon S3 backend

Credentials come from the environment:

```
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...      # only for temporary credentials
```

Restic also honours `AWS_DEFAULT_REGION`, `AWS_PROFILE` and `AWS_SHARED_CREDENTIALS_FILE`, and can assume a role through the `RESTIC_AWS_ASSUME_ROLE_*` variables (ARN, session name, external ID, policy, region, STS endpoint).

## Repository URL

Only path-style addressing is supported:

```
restic -r s3:s3.us-east-1.amazonaws.com/bucket_name init
```

Virtual-hosted-style URLs are not supported. Until restic 0.8.0 the default prefix was `restic`; a repository created by an older version is addressed as `.../bucket_name/restic`.

## Storage class

Default is `STANDARD`. Other accepted values: `STANDARD_IA`, `ONEZONE_IA`, `INTELLIGENT_TIERING`, `REDUCED_REDUNDANCY`. Set per command:

```
restic backup -o s3.storage-class=REDUCED_REDUNDANCY /path/to/data
```

See the s3-iam-setup skill for an IAM policy example. If the bucket does not exist, `init` creates it in the region of the endpoint used.

## Checked

2026-11-03. Confirmed in the restic docs pages Preparing a new repository (Amazon S3 section), Scripting (AWS and `RESTIC_AWS_ASSUME_ROLE_*` variables) and Examples (storage classes and `s3.storage-class`): credential variables incl. session token, path-style only, the pre-0.8.0 prefix, default `STANDARD` and the other four class names. Removed: the snapshots smoke-test paragraph and unsupported advice about credentials and shell history.

Method: documentation only; no commands were run.
