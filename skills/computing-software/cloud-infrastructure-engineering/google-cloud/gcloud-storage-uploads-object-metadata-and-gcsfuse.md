---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcloud-storage-uploads-object-metadata-and-gcsfuse
name: gcloud-storage-uploads-object-metadata-and-gcsfuse
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, gcloud-storage-cp, parallel-composite-upload, object-metadata, content-type-cache-control, gcsfuse, cloud-storage-fuse, gke-gcsfuse-csi]
level: practitioner
status: docs-checked
description: "Move data with gcloud storage cp/rsync and parallel composite uploads, set Content-Type, Cache-Control and custom metadata, and mount buckets with Cloud Storage FUSE."
sources: ["https://cloud.google.com/storage/docs/parallel-composite-uploads", "https://cloud.google.com/sdk/gcloud/reference/storage/cp", "https://cloud.google.com/storage/docs/metadata", "https://cloud.google.com/storage/docs/gcs-fuse", "https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gcloud storage uploads, object metadata and Cloud Storage FUSE

## 1. Copy and sync
```bash
gcloud storage cp -r ./build gs://<B>/site/
gcloud storage rsync -r --delete-unmatched-destination-objects ./build gs://<B>/site
gcloud config set storage/parallel_composite_upload_enabled False    # disable parallel composite uploads
```
`storage/parallel_composite_upload_enabled` defaults to None, which enables parallel composite uploads (large files split into parts and composed) for objects that meet the criteria, with bucket compatibility checks; False disables them. `storage/parallel_composite_upload_threshold` is the minimum file size, default 150 MiB.
Composite objects carry a **crc32c hash only (no MD5)**, so clients that need MD5 cannot use them. Temporary part objects in storage classes other than Standard can incur early deletion fees; disable parallel composite uploads for such buckets.

## 2. Metadata that matters
```bash
gcloud storage cp index.html gs://<B>/site/ --content-type=text/html --cache-control="public, max-age=300"
gcloud storage objects update gs://<B>/site/app.*.js --cache-control="public, max-age=31536000, immutable"
gcloud storage objects update gs://<B>/reports/q3.pdf --content-disposition='attachment; filename="q3.pdf"' \
  --custom-metadata=owner=finance,retention=7y
gcloud storage cp -Z app.js gs://<B>/site/       # gzip-compress on upload (see the cp reference)
gcloud storage objects describe gs://<B>/site/index.html --format='yaml(contentType,cacheControl,contentEncoding,metadata)'
```
Without an explicit `Cache-Control`, publicly readable objects are served with `public, max-age=3600` (unless encrypted with a customer-managed key or inside a VPC Service Controls perimeter), so caches may keep the old file for up to an hour. Use hashed filenames for assets and short
TTLs for HTML.

## 3. Cloud Storage FUSE
Cloud Storage FUSE turns `/` in object names into directory separators. On flat-namespace buckets it cannot infer implicitly defined directories (simulated or managed folders) by default; on hierarchical namespace buckets it infers explicit folders, and Google recommends HNS buckets if you need a file system.
```bash
gcsfuse --implicit-dirs <B> /mnt/models
```
GKE: the CSI driver pod annotation is `gke-gcsfuse/volumes: "true"`, with a `csi` volume using `driver: gcsfuse.csi.storage.gke.io`; the driver page shows `mountOptions: "implicit-dirs"` for flat buckets.

## Gotchas
- rsync without `--delete-unmatched-destination-objects` never removes stale files; with it, a wrong source path deletes everything — dry-run first (`--dry-run`).

## Verify
- [ ] `curl -I https://storage.googleapis.com/<B>/site/index.html` shows the intended Content-Type and Cache-Control.

## Checked

2026-10-28. Confirmed against: Cloud Storage parallel composite uploads page (property defaults, 150 MiB threshold, crc32c only, early deletion fees), object metadata page (default Cache-Control for public objects), Cloud Storage FUSE overview (directory inference and HNS), the GKE Cloud Storage FUSE CSI driver page (annotation, driver name, `implicit-dirs`), and gcloud storage reference pages (commands checked with the command checker).

Removed or corrected: the claim that setting the enabled property to True turns the feature on (default None already enables it), the fstab line and file-mode options, the file-cache config values, the `--addons` flag name, and the POSIX, rename and list-cost gotchas.

Method: documentation only; no commands were run.
