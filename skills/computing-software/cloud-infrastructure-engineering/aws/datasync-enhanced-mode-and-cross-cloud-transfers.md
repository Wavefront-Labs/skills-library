---
id: computing-software.cloud-infrastructure-engineering.aws.datasync-enhanced-mode-and-cross-cloud-transfers
name: datasync-enhanced-mode-and-cross-cloud-transfers
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, datasync, datasync-enhanced-mode, cross-cloud-transfer, s3-migration, object-storage]
level: advanced
status: docs-checked
description: "Use DataSync Enhanced mode for large S3 transfers and move data from other clouds' object storage (Azure Blob, Google Cloud Storage, S3-compatible) into AWS."
sources: ["https://docs.aws.amazon.com/datasync/latest/userguide/choosing-task-mode.html", "https://docs.aws.amazon.com/datasync/latest/userguide/creating-azure-blob-location.html", "https://docs.aws.amazon.com/datasync/latest/userguide/tutorial_transfer-google-cloud-storage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DataSync Enhanced mode and cross-cloud transfers

## 1. Task modes
| | Basic | Enhanced |
|---|---|---|
| Object count | limited per task | virtually unlimited |
| Performance | good | higher, parallel listing/prep/transfer |
| Metrics | task-level | detailed per-stage, CloudWatch |
| Supported locations | all | S3, EFS, FSx for Lustre, FSx for OpenZFS, NFS, SMB, HDFS, Azure Blob and object storage, only for supported pairs (some need an Enhanced mode agent; FSx for Windows needs Basic) |
```bash
aws datasync create-task --source-location-arn <S3_SRC> --destination-location-arn <S3_DST> \
  --task-mode ENHANCED --name s3-consolidation \
  --options VerifyMode=ONLY_FILES_TRANSFERRED,ObjectTags=PRESERVE,TransferMode=CHANGED
```

## 2. Other clouds
- **Google Cloud Storage** (S3-compatible XML API with HMAC keys):
```bash
aws datasync create-location-object-storage --server-hostname storage.googleapis.com --server-protocol HTTPS \
  --bucket-name gcs-src --access-key <HMAC_ACCESS_ID> --secret-key <HMAC_SECRET> --agent-arns <AGENT_ARN>
```
- **Azure Blob**: `create-location-azure-blob --container-url https://acct.blob.core.windows.net/container
  --authentication-type SAS --sas-configuration Token=<SAS> --agent-arns <AGENT_ARN>`.
- Agents can run as EC2 instances in your VPC or as VMs in the other cloud near the data. Transfers between
  Google Cloud Storage or Azure Blob and S3 using Enhanced mode do not need an agent; private connectivity does.
- Egress fees from the source cloud apply; estimate bytes before the run.

## 3. Large migrations
- Manifests (`--manifest-config`) to transfer exact object lists; include/exclude filters by prefix.
- Run incrementals until cutover; `TransferMode=CHANGED`.
- Watch `FilesTransferred`, `BytesTransferred` and per-stage metrics; failures listed in task reports.

## Verify
- [ ] Task report shows zero failed objects; object counts and total size match source inventory.

## Checked

2026-10-28. Confirmed against the choosing-task-mode, Google Cloud Storage tutorial and Azure Blob location pages: Enhanced mode unlimited objects and parallel listing/prepare/transfer/verify, supported location list, GCS via XML API with HMAC keys, agent placement, source-cloud transfer charges. Removed the unconfirmed "without an agent between object stores" wording and made the location row specific. CLI commands checked against the botocore model. Read end to end.

Method: documentation only; no commands were run.
