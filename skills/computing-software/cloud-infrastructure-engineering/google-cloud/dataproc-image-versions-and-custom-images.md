---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dataproc-image-versions-and-custom-images
name: dataproc-image-versions-and-custom-images
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, dataproc, dataproc-image-versions, custom-dataproc-images, initialization-actions, upgrades]
level: advanced
status: docs-checked
description: "Choose and pin Dataproc image versions, build custom images with generate_custom_image.py instead of slow init actions, and plan upgrades across Spark and OS versions."
sources: ["https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions", "https://cloud.google.com/dataproc/docs/guides/dataproc-images", "https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/init-actions", "https://github.com/GoogleCloudDataproc/custom-images"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataproc image versions and custom images

## 1. Versions
`--image-version=2.2-debian12` pins the **minor** track (you get the latest sub-minor at creation).
Pin the full sub-minor (`2.2.<SUB>-debian12`) for reproducibility in prod, and bump deliberately.
Each image fixes Spark/Hadoop/Python versions; check the release notes table before bumping. Images
reach end of support; clusters keep running but stop getting fixes.

## 2. Init actions vs custom images
Init actions run on every node at boot (slow, can fail scale-up). Pre-bake instead:
```bash
git clone https://github.com/GoogleCloudDataproc/custom-images && cd custom-images
python generate_custom_image.py --image-name=dp-2-2-acme-v3 --dataproc-version=2.2.35-debian12 \
  --customization-script=install.sh --zone=<ZONE> --gcs-bucket=gs://<B>/custom-image-logs \
  --no-smoke-test --service-account=image-builder@<P>.iam.gserviceaccount.com
gcloud dataproc clusters create etl --region=<R> --image=projects/<P>/global/images/dp-2-2-acme-v3
```
The customization script installs Python packages/agents/certs. Custom images expire for cluster creation after
365 days (label `goog-dataproc-version`); rebuild on a schedule.

## 3. Upgrading
- There's no in-place image upgrade: create new clusters on the new image, run jobs side-by-side, compare outputs.
- Check Python and Scala binary changes (Spark 3.5, Scala 2.12/2.13) and connector JAR versions.
- Serverless batches use `--version=2.2` runtime versions the same way.

## Gotchas
- Init actions must be idempotent and fast; scale-up waits for them. Use `--initialization-action-timeout`.
- Custom image build needs a VPC with egress for package installs, or a mirror.
- Mixing a custom image with `--image-version` is an error: the image already defines it.

## Verify
- [ ] `gcloud dataproc clusters describe etl --region=<R> --format='value(config.softwareConfig.imageVersion,config.masterConfig.imageUri)'` shows the intended image; cluster boots without init actions.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the pinned sub-minor version (now a placeholder) and the install.sh file name.

Method: documentation only; no commands were run.
