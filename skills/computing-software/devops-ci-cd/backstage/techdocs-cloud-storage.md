---
id: computing-software.devops-ci-cd.backstage.techdocs-cloud-storage
name: techdocs-cloud-storage
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-publisher, aws-s3, google-gcs, backstage]
level: advanced
status: docs-checked
description: "Store generated TechDocs sites in S3 or Google Cloud Storage with the techdocs.publisher config."
sources:
  - https://backstage.io/docs/features/techdocs/using-cloud-storage
  - https://backstage.io/docs/features/techdocs/architecture
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The publisher decides where generated sites live. By default TechDocs stores generated files on the backend's local file system, while the docs recommend external storage such as AWS S3, GCS or Azure Blob Storage.

```yaml
techdocs:
  builder: 'external'
  publisher:
    type: 'googleGcs'
    googleGcs:
      bucketName: 'name-of-techdocs-storage-bucket'
      projectId: 'name-of-project'
```

```yaml
techdocs:
  publisher:
    type: 'awsS3'
    awsS3:
      bucketName: 'name-of-techdocs-storage-bucket'
      region: 'us-east-1'
```

- GCS credentials can come from `$file` pointing at a JSON key, from `${GOOGLE_APPLICATION_CREDENTIALS}`, or from default application credentials.
- S3 credentials can come from the AWS environment variables or `~/.aws/credentials`, from `aws.accounts` entries (with `accountId` set under `techdocs.publisher.awsS3`), or from an `integrations.awsS3` integration. On EC2, ECS or EKS an IAM role avoids separate access keys.
- Azure Blob Storage is a supported option too.

The docs give example IAM policies: the Backstage backend needs read access to the bucket, and the CI publisher needs write access.

## Checked

2026-11-03. Confirmed on the Using Cloud Storage page: `techdocs.publisher.type` values, the GCS keys `bucketName`, `projectId` and `credentials` (a `$file` JSON key, `${GOOGLE_APPLICATION_CREDENTIALS}` or default credentials), S3 `bucketName` and `region`, the S3 authentication options and IAM role note, example IAM policies with separate read and write access, and Azure Blob Storage. On the Architecture page: the local file system is the default store and external storage is recommended. Removed: `bucketRootPath`, `endpoint`, proxy and static key YAML, and the publisher extension point sentence, none of which this page states (the CLI has separate flags for some).

Method: documentation only; no commands were run.
