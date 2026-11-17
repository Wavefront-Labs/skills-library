---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-storage-access-control-and-signed-urls
name: cloud-storage-access-control-and-signed-urls
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, gcs, gcs-security, signed-urls, signed-policy-documents, uniform-bucket-level-access, bucket-iam, public-access-prevention, iam-conditions, object-acl, allusers, cmek-gcs, hmac-keys, requester-pays, cors, bucket-hardening, data-exfiltration]
level: practitioner
status: docs-checked
description: "Lock down Cloud Storage: uniform bucket-level access and public access prevention, IAM conditions on prefixes, signed URLs and policy documents for uploads, CMEK, HMAC keys, CORS and requester pays."
sources: ["https://docs.cloud.google.com/storage/docs/uniform-bucket-level-access", "https://docs.cloud.google.com/storage/docs/public-access-prevention", "https://docs.cloud.google.com/storage/docs/access-control/signed-urls", "https://docs.cloud.google.com/storage/docs/access-control/iam-roles", "https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions", "https://docs.cloud.google.com/storage/docs/encryption/using-customer-managed-keys", "https://docs.cloud.google.com/sdk/gcloud/reference/storage/sign-url"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Storage access control and signed URLs

**Goal:** no bucket is accidentally public, access is IAM-only and scoped to prefixes where
needed, and untrusted clients upload/download via short-lived signed URLs rather than credentials.

## 1. Bucket baseline (enforce by org policy)
```bash
gcloud storage buckets create gs://prj-p-payments-docs --location=europe-west1 \
  --uniform-bucket-level-access --public-access-prevention \
  --default-storage-class=STANDARD --soft-delete-duration=7d
```
- **Uniform bucket-level access (UBLA)**: object and bucket ACLs stop working; IAM is the only control. An organization-level "enforce uniform bucket-level access" constraint can require it. It cannot be disabled once active for 90 consecutive days.
- **Public access prevention**: blocks `allUsers`/`allAuthenticatedUsers` grants (new grants fail with `412 Precondition Failed`). A bucket's state is `enforced` or `inherited`; the organization policy constraint is `storage.publicAccessPrevention`.
- Single region, or a custom dual-region with `--placement=<region>,<region>`, per residency requirements.

## 2. IAM scoping
- Bucket-level: `gcloud storage buckets add-iam-policy-binding gs://B --member=group:x --role=roles/storage.objectViewer`.
- Prefix-level with an **IAM condition** (UBLA must be enabled first):
  ```
  --condition='expression=resource.name.startsWith("projects/_/buckets/B/objects/tenant-42/"),title=tenant42'
  ```
- Roles: `objectViewer` (get and list objects), `objectCreator` (create only; no view, delete or overwrite — good for drop boxes), `objectUser` (create, read, update and delete objects), `objectAdmin` (full object control), `admin` (objects and buckets). The legacy `storage.legacy*` roles can be granted only on individual buckets and are reflected in ACLs; avoid them.
- `roles/storage.objectCreator` without `objectViewer` is a write-only sink; combine with retention for immutable ingest.

## 3. Signed URLs (download or upload without Google credentials)
```bash
gcloud storage sign-url gs://B/report.pdf --duration=15m \
  --private-key-file=key.json            # or --impersonate-service-account=signer@P.iam.gserviceaccount.com
```
By default `--duration` is 3600 seconds and at most 12 hours; signing with `--private-key-file` or a service account activated with `gcloud auth activate-service-account` allows up to 7 days. With `--impersonate-service-account` the impersonated service account signs; otherwise a service account key is required. Use `--http-verb=PUT` and `--headers=KEY=VALUE` for uploads: headers included in the signature must be sent with any request that uses the URL.
- V4 signed URLs last at most 604800 seconds (7 days); the signer is normally a service account.
- A signed URL can be used for the initial POST that starts a resumable upload; the server can instead start the upload and hand the session URI to the client.
- **Signed policy documents** (HTML form POST) let a browser upload directly with constraints; see the post-object forms documentation for the supported conditions.

## 4. Keys, encryption, other switches
- **CMEK**: `gcloud storage buckets update gs://B --default-encryption-key=projects/P/locations/europe-west1/keyRings/kr/cryptoKeys/gcs` — the key ring must be in the same location as the data (it may be in another project); grant the Cloud Storage service agent `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key (for example with `gcloud storage service-agent --authorize-cmek`). `--default-encryption-key` also exists on `buckets create`.
- **HMAC keys** for S3-compatible clients: `gcloud storage hmac create signer@P.iam.gserviceaccount.com` — the secret is only shown at creation; treat HMAC keys like service account keys and manage them with `gcloud storage hmac list`, `update` and `delete`.
- **Requester pays** (`--requester-pays` on `buckets update`) for shared datasets.
- **CORS**: `gcloud storage buckets update gs://B --cors-file=cors.json` for browser uploads/downloads.
- **Soft delete** (default 7 days) and object versioning for recovery; **retention policy / bucket lock** for WORM (see `gcs-lifecycle-management`).

## Gotchas
- `roles/storage.objectViewer` on a *project* grants read on every bucket in it; grant at bucket level.
- Signed URLs are normally signed by a service account; without a key file, use `--impersonate-service-account`.
- Check the system clock of the machine that signs: a skewed clock can make a signed URL expire early or not yet be valid.
- `allAuthenticatedUsers` means *any Google account on earth*, not your org — public access prevention rightly blocks it.

## Verify
- [ ] `gcloud storage buckets describe gs://B` shows uniform bucket-level access enabled and public access prevention enforced; granting `allUsers` is refused.
- [ ] A tenant-42 condition lets the test user `cat gs://B/tenant-42/x` and denies `gs://B/tenant-43/x`.
- [ ] A 15-minute signed URL downloads with `curl` and stops working after expiry.
- [ ] A request that omits or changes a header included in the signature is rejected.

## Checked
Checked 2026-10-24 against the Cloud Storage uniform bucket-level access, public access prevention, signed URLs, IAM roles, IAM conditions and customer-managed keys pages and the gcloud `storage sign-url`, `buckets create`, `buckets update` and `hmac create` references (docs.cloud.google.com). Confirmed the 90-day UBLA window, PAP behaviour and the `storage.publicAccessPrevention` constraint, the IAM condition expression and UBLA prerequisite, role capabilities, the 7-day V4 maximum and the `sign-url` duration rules, CMEK key-ring location and service-agent role, and the HMAC create command. Removed the `storage.uniformBucketLevelAccess` and `storage.restrictAuthTypes` constraint names, the VPC Service Controls remark, the audit-log verification and the `x-goog-content-sha256` and `signBlob` specifics, none of which the pages state. `--requester-pays` is documented on `buckets update` but not on `buckets create`.
Method: documentation only; no commands were run.
