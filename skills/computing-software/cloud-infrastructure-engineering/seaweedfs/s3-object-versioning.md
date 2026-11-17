---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-object-versioning
name: s3-object-versioning
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [version-id, delete-marker, list-object-versions, versioning]
level: practitioner
status: docs-checked
description: "Enable, suspend and use S3 object versioning on SeaweedFS with the AWS CLI: list versions, get or copy a specific version and delete markers."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Object-Versioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 object versioning

```bash
export S3_ENDPOINT=http://localhost:8333
aws --endpoint-url $S3_ENDPOINT s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled
aws --endpoint-url $S3_ENDPOINT s3api get-bucket-versioning --bucket my-bucket
aws --endpoint-url $S3_ENDPOINT s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Suspended
```
Suspending does not disable versioning completely.

Inspect and use versions:
```bash
aws --endpoint-url $S3_ENDPOINT s3api list-object-versions --bucket my-bucket
aws --endpoint-url $S3_ENDPOINT s3api get-object --bucket my-bucket --key example.txt --version-id <id> out.txt
aws --endpoint-url $S3_ENDPOINT s3api copy-object --copy-source "my-bucket/example.txt?versionId=<id>" --bucket my-bucket --key copy.txt
aws --endpoint-url $S3_ENDPOINT s3api delete-object --bucket my-bucket --key example.txt --version-id <id>
```
The listing returns `Versions` (with `IsLatest`) and `DeleteMarkers`. A plain delete adds a delete marker; deleting a specific version id removes only that version.

Object Lock requires versioning. The page notes that version-specific lifecycle rules are not fully implemented.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Object Versioning: Enabled and Suspended status, listing with Versions, IsLatest and DeleteMarkers, copy with `?versionId=`, delete marker behaviour. Removed the claim that noncurrent versions can be expired with lifecycle rules (the page says version-specific lifecycle rules are not fully implemented) and the Verify line.
Method: documentation only; no commands were run.
