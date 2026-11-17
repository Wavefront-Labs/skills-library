---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-storage-bucket-relocation
name: cloud-storage-bucket-relocation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, bucket-relocation, gcloud-storage-buckets-relocate, data-residency, storage-transfer]
level: practitioner
status: docs-checked
description: "Move a Cloud Storage bucket to a new location without renaming it: relocation dry run, write-downtime vs no-downtime moves, finalisation, and the copy alternative."
sources: ["https://cloud.google.com/storage/docs/bucket-relocation/overview", "https://cloud.google.com/storage/docs/bucket-relocation/relocate-buckets", "https://cloud.google.com/sdk/gcloud/reference/storage/buckets/relocate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Storage bucket relocation

Historically a bucket's location was immutable: you created a new bucket and copied. **Bucket
relocation** moves data to a new location while keeping the bucket name, metadata and IAM.

## Run
```bash
# 1. dry run: reports incompatibilities (e.g. unsupported features)
gcloud storage buckets relocate gs://media-assets --location=europe-west2 --dry-run
# 2. start (from multi-region/dual-region to region etc.)
gcloud storage buckets relocate gs://media-assets --location=europe-west2
# 3. track the long-running operation
gcloud storage operations list projects/_/buckets/media-assets
gcloud storage operations describe projects/_/buckets/media-assets/operations/<OP>
# 4. the write-downtime form needs a finalize step
gcloud storage buckets relocate gs://media-assets --finalize --operation=projects/_/buckets/media-assets/operations/<OP>
```
- Relocation comes in a no-write-downtime form and a write-downtime form; the dry run and the relocation docs tell you which applies.
- Reads stay available during relocation (no downtime for reads, minimal for writes).

## When to copy instead
Storage Transfer Service or `gcloud storage cp -r` to a new bucket if relocation is unsupported for
your source/target pair, if you also want to rename, or to change features (for example hierarchical namespace) at the same time.
Plan: new bucket, sync, cut over clients, final incremental sync, delete old.

## Gotchas
- Relocation incurs charges; see the Cloud Storage pricing page.
- Some bucket restrictions can block relocation (the docs suggest Storage Transfer Service as a workaround); with CMEK, supply `--destination-kms-key-name` for the destination.
- Storage class settings, including Autoclass, are preserved.

## Verify
- [ ] `gcloud storage buckets describe gs://media-assets --format='value(location)'` shows the new location; object counts match.

## Checked

2026-10-28. Confirmed against: gcloud storage buckets relocate reference (--location, --dry-run, --operation, --finalize, --destination-kms-key-name) and the bucket relocation overview (write-downtime vs minimal-downtime, reads stay available, Autoclass preserved, Storage Transfer Service workaround).

Removed or rewritten: per-GiB pricing wording, the claim that retention locks and Pub/Sub or inventory settings need re-checking, and the location-type rule for no-downtime moves.

Method: documentation only; no commands were run.
