---
id: computing-software.cloud-infrastructure-engineering.minio.tier-targets
name: tier-targets
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, tier-targets, mc-ilm-tier-add-s3, mc-ilm-tier-add-gcs, mc-ilm-tier-add-azure, credentials-file, storage-class, remote-prefix]
level: practitioner
status: docs-checked
description: "Register MinIO, S3, GCS or Azure remote tiers with mc ilm tier add: endpoint, credentials-file, account-key and storage-class options for each target type."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/transition-objects-to-minio.rst", "https://github.com/minio/docs/blob/main/source/administration/object-management/transition-objects-to-s3.rst", "https://github.com/minio/docs/blob/main/source/administration/object-management/transition-objects-to-gcs.rst", "https://github.com/minio/docs/blob/main/source/administration/object-management/transition-objects-to-azure.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO remote tier targets

`mc ilm tier add TYPE TARGET TIER_NAME ...` registers a remote tier. `TARGET` is the alias of the MinIO deployment, and the tier name (the docs suggest all caps, e.g. `S3_TIER`) is needed in the next step, the lifecycle rule.

## MinIO and Amazon S3
```
mc ilm tier add minio TARGET TIER_NAME \
   --endpoint https://HOSTNAME --access-key ACCESS_KEY --secret-key SECRET_KEY \
   --bucket BUCKET --prefix PREFIX --storage-class STORAGE_CLASS --region REGION
mc ilm tier add s3 TARGET TIER_NAME   (same flags)
```

## Google Cloud Storage
```
mc ilm tier add gcs TARGET TIER_NAME \
   --bucket BUCKET --prefix PREFIX --credentials-file CREDENTIALS --storage-class STORAGE_CLASS
```
If the GCS bucket has a default storage class, MinIO uses it when `--storage-class` is omitted.

## Azure Blob Storage
```
mc ilm tier add azure TARGET TIER_NAME \
   --account-name ACCOUNT --account-key KEY --bucket CONTAINER --endpoint ENDPOINT \
   --prefix PREFIX --storage-class STORAGE_CLASS
```
`--endpoint` is optional and defaults to `https://ACCOUNT.blob.core.windows.net`; the account name cannot be changed after the tier is created. A storage account default access tier is used when `--storage-class` is omitted.

## Notes
- The remote bucket (or container) must exist beforehand.
- Use `--prefix` to separate MinIO's objects from other data in the bucket.
- Pair with `computing-software.cloud-infrastructure-engineering.minio.tiering` for the transition rule and its warnings.

## Checked

2026-11-03. Confirmed against the MinIO docs source: the four transition-objects-to-* pages: flags per target type, Azure endpoint default, GCS and Azure default storage-class behaviour, remote bucket must exist, prefix advice. Removed or fixed: the invented `--transition-tier` reference and the truncated-output note.

Method: documentation only; no commands were run.
