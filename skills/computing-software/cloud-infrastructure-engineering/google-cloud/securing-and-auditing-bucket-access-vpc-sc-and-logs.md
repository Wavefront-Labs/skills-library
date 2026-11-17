---
id: computing-software.cloud-infrastructure-engineering.google-cloud.securing-and-auditing-bucket-access-vpc-sc-and-logs
name: securing-and-auditing-bucket-access-vpc-sc-and-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, gcs-vpc-service-controls, bucket-vpc-sc, gcs-audit-logs, bucket-usage-logs, data-access-logs, exfiltration]
level: advanced
status: docs-checked
description: "Fence sensitive buckets inside a VPC Service Controls perimeter and record who read or wrote what, using Data Access audit logs or legacy usage and storage logs."
sources: ["https://docs.cloud.google.com/vpc-service-controls/docs/supported-products", "https://docs.cloud.google.com/storage/docs/audit-logging", "https://docs.cloud.google.com/storage/docs/access-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing and auditing bucket access: VPC-SC and logs

## 1. Buckets inside a perimeter
IAM answers *who*; VPC Service Controls answers *from where* and *to where*. With
`storage.googleapis.com` restricted in a perimeter around the data project, requests from outside the perimeter are blocked and copying to a bucket outside it fails (the exfiltration control).
```bash
gcloud access-context-manager perimeters update data-perim --policy=<POLICY> \
  --add-resources=projects/<DATA_PROJECT_NUMBER> --add-restricted-services=storage.googleapis.com
```
Allow known external flows with ingress/egress rules (e.g. a partner SA reading one bucket), not by
removing the restriction. Run new perimeters in dry-run first (see VPC-SC skills).

## 2. Who touched objects: Data Access audit logs
```bash
gcloud projects get-iam-policy <P> --format=json > p.json
# add to p.json:
# "auditConfigs":[{"service":"storage.googleapis.com","auditLogConfigs":[{"logType":"DATA_READ"},{"logType":"DATA_WRITE"}]}]
gcloud projects set-iam-policy <P> p.json
```
Query: `resource.type="gcs_bucket" resource.labels.bucket_name="<B>"`. Cloud Storage audit logs use the resource type `gcs_bucket`; DATA_READ covers getting object data and metadata and listing objects.
Volume can be large on busy buckets: enable on sensitive projects, and use exemptions only for principals whose access is logged elsewhere. Audit logs do not track access to public objects.

## 3. Legacy usage and storage logs
Hourly CSV usage logs (requests, bytes, caller IP) and daily storage-size logs written to a bucket:
```bash
gcloud storage buckets create gs://<org>-gcs-usage-logs --location=<R> --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding gs://<org>-gcs-usage-logs \
  --member=group:cloud-storage-analytics@google.com --role=roles/storage.objectCreator
gcloud storage buckets update gs://<B> --log-bucket=gs://<org>-gcs-usage-logs --log-object-prefix=<B>
```
Cloud Audit Logs is the recommended method for tracking who accesses Cloud Storage; usage logs suit access through `allUsers` / `allAuthenticatedUsers` and per-request detail.

## Gotchas
- Run a new perimeter in dry-run first so cross-project flows that silently worked show up as violations.
- Usage logs are generated hourly (typically about 15 minutes after the hour) and their timeliness and completeness are not guaranteed.

## Verify
- [ ] From outside the perimeter and access level, `gcloud storage ls gs://<B>` is denied with a VPC-SC violation.
- [ ] A test object read appears in Logs Explorer with the caller's principal.

## Checked
2026-10-31. Confirmed on Cloud Storage "Audit logging" and "Usage logs and storage logs" pages: DATA_READ, `gcs_bucket` resource type, exemptions, no audit logs for public objects, audit logs recommended over usage logs, hourly CSV usage logs and daily storage logs, delivery not guaranteed, `cloud-storage-analytics@google.com` with `roles/storage.objectCreator`, `--log-bucket` and `--log-object-prefix`. Removed: the literal 403 text, `allUsers` behaviour under VPC-SC, `storage.objects.get` method name, signed-URL and Cloud Build gotchas (not confirmed). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
