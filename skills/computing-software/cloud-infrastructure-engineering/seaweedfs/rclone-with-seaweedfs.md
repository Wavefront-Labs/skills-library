---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.rclone-with-seaweedfs
name: rclone-with-seaweedfs
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [rclone, restic, s3-client]
level: intro
status: docs-checked
description: "Configure rclone and restic with SeaweedFS S3: rclone.conf (provider Other, force_path_style) and restic needing non-anonymous keys."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/rclone-with-SeaweedFS
  - https://github.com/seaweedfs/seaweedfs/wiki/restic-with-SeaweedFS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rclone with seaweedfs

rclone remote in `rclone.conf`:
```
[swfs]
type = s3
provider = Other
access_key_id = any-key-id
secret_access_key = any-access-key
endpoint = http://localhost:8333
upload_cutoff = 50Mi
chunk_size = 50Mi
force_path_style = true
```
```bash
rclone --log-level INFO copy --checksum --fast-list /path/to/files swfs:/bucket-name/files
```
Sub-path proxies need the `X-Forwarded-Prefix` header, as for the AWS CLI.

restic needs non-anonymous access. Create an identity (any key values) and use the same keys on both sides:
```bash
export AWS_ACCESS_KEY_ID=any-key-id AWS_SECRET_ACCESS_KEY=any-access-key
echo "s3.configure -access_key $AWS_ACCESS_KEY_ID -secret_key $AWS_SECRET_ACCESS_KEY -user iam -actions Admin -apply" | weed shell
s3cmd mb s3://resticbucket
restic -r s3:http://localhost:8333/resticbucket init
restic -r s3:http://localhost:8333/resticbucket backup /path/to/data
```
## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages rclone with SeaweedFS (rclone.conf fields, copy command, X-Forwarded-Prefix) and restic with SeaweedFS (non-anonymous keys, s3.configure, s3cmd mb, restic init and backup). Removed the Verify line.
Method: documentation only; no commands were run.
