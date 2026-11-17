---
id: computing-software.database-administration.dragonfly.s3-credentials-and-flags
name: s3-credentials-and-flags
category: computing-software
field: database-administration
product: dragonfly
tags: [s3-credentials, s3-endpoint, minio, s3-flags, dragonfly]
level: practitioner
status: docs-checked
description: "Supply AWS credentials and region to Dragonfly for S3 snapshots, use S3-compatible services like MinIO, and the s3_* flags."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly infers AWS credentials from the environment using standard AWS credential providers:

- Environment variables such as `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`.
- The shared credentials file `~/.aws/credentials` (override with `AWS_SHARED_CREDENTIALS_FILE`; default profile via `AWS_PROFILE`).
- EC2 instance metadata, only when started with `--s3_ec2_metadata`.

Also set the bucket region via `AWS_REGION`, the shared config file or EC2 metadata.

S3 flags:

| Flag | Meaning | Default |
| --- | --- | --- |
| `s3_endpoint` | override endpoint for S3-compatible services | empty (AWS regional endpoint) |
| `s3_ec2_metadata` | load credentials from EC2 metadata | false |
| `s3_sign_payload` | sign upload payloads (has a performance cost) | true |
| `s3_use_https` | use HTTPS | true |

For MinIO on `localhost:9000`:

```shell
./dragonfly --logtostderr --dir s3://acme-backups --s3_endpoint localhost:9000
```

The backups page marks Dragonfly S3 cloud storage as a preview feature.

## Checked

2026-11-04. Confirmed against the Dragonfly Saving Backups page and flags page: credential providers and variables, region sources, the four s3 flags and their defaults, the MinIO example, the preview note. Nothing removed.

Method: documentation only; no commands were run.
