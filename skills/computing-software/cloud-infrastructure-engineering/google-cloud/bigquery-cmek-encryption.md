---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-cmek-encryption
name: bigquery-cmek-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-cmek, cloud-kms, encryption, org-policy]
level: advanced
status: docs-checked
description: "Protect BigQuery data with customer-managed KMS keys: service agent grants, dataset default keys, per-table and query-destination keys, rotation, and enforcing CMEK by org policy."
sources: ["https://cloud.google.com/bigquery/docs/customer-managed-encryption", "https://cloud.google.com/kms/docs/cmek-org-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery CMEK

## 1. Key location and service account
Create the key ring in the location of the dataset: a multi-region dataset needs a multi-region key ring
from a matching location (dataset in `US` with key ring in `us`; `EU` with `europe`), and a regional dataset needs
a matching regional key (for example `asia-northeast1`). The console cannot use the `global` location; bq and
GoogleSQL can. BigQuery uses the key as a key-encryption key (AES-256) over its data-encryption keys.

The BigQuery service account of the project is not created with the project. Trigger it and read its ID:
```bash
bq show --encryption_service_account --project_id=<PROJECT_ID>   # bq-<PROJECT_NUMBER>@bigquery-encryption.iam.gserviceaccount.com
gcloud kms keys add-iam-policy-binding <KEY> --keyring=<KEYRING> --location=<LOCATION> --project=<KMS_PROJECT_ID> \
  --member=serviceAccount:bq-<PROJECT_NUMBER>@bigquery-encryption.iam.gserviceaccount.com \
  --role=roles/cloudkms.cryptoKeyEncrypterDecrypter
```
Service accounts are per project: the project that owns the table (or that runs a job writing an
anonymous table) supplies the service account that needs the role.

## 2. Apply
```bash
bq mk --dataset --default_kms_key projects/<KMS_PROJECT_ID>/locations/<LOCATION>/keyRings/<KEYRING>/cryptoKeys/<KEY> <PROJECT_ID>:<DATASET>
bq cp --destination_kms_key <KEY_RESOURCE_ID> <PROJECT_ID>:<DATASET>.<SRC_TABLE> <PROJECT_ID>:<DATASET>.<DST_TABLE>
bq query --destination_table <DATASET>.<TABLE> --destination_kms_key <KEY_RESOURCE_ID> 'SELECT ...'
```
- A dataset default key applies to newly created tables only; changing it does not modify existing tables. Set or change it on an existing dataset with `bq update --dataset --default_kms_key <KEY_RESOURCE_ID> ...` (set it to `""` to remove it); the SQL forms are `CREATE SCHEMA` / `ALTER SCHEMA` with `default_kms_key_name`.
- A project default key (`ALTER PROJECT SET OPTIONS` with `default_kms_key_name`) applies to query results and new tables for that location, including cached results tables in anonymous datasets.
- By default query results go to a temporary table encrypted with a Google-owned key; use `--destination_kms_key` (or a project default) to protect them.
- A table cannot be switched in place between default encryption and CMEK: copy it with the destination key set, or `SELECT *` into itself with `WRITE_TRUNCATE`. `bq cp` without `--destination_kms_key` copies a CMEK table back to default encryption.
- `bq cp --destination_kms_key` also changes the key of a table already protected by Cloud KMS.

## 3. Enforce
Organization policy `constraints/gcp.restrictNonCmekServices` (deny `bigquery.googleapis.com`) makes resource
creation requests without a Cloud KMS key fail. It applies to new resources only and to resources that contain
data; datasets and project config, which only hold a default key, can still be created or updated without one.
`constraints/gcp.restrictCmekCryptoKeyProjects` limits which projects can supply keys; the KMS page says it does not
by itself guarantee CMEK use, so apply both. A new or changed policy can take up to 15 minutes to take effect
because BigQuery caches policies. Setting an organization policy needs the Organization Policy Administrator role
granted at the organization level.

## Gotchas
- The key must be enabled and the BigQuery service account must be able to encrypt and decrypt. Streaming inserts need it available for at least 24 consecutive hours in the 48 hours after the insert, or data might be lost. If the key is unavailable for 60 consecutive days BigQuery might delete the table (with an email at least 7 days before).
- Rotation: BigQuery does not rotate an existing table's key. Existing data stays on the key version it was created with; update the table with the same Cloud KMS key to move to the latest version. New tables in a dataset with a default key use the latest version after rotation.
- CMEK-protected tables cannot be queried with a wildcard suffix; scripts cannot define destination tables for CMEK operations.
- CMEK support is for BigQuery Enterprise, Enterprise Plus and On-Demand; BigQuery and BigLake tables do not support customer-supplied keys.
- Anyone with access to the table can read it if the service account has the key role, even without direct access to the key.
- Billing: one Cloud KMS encrypt call per table creation or truncation and one decrypt per table in a query; see the Cloud KMS pricing page.

## Verify
- [ ] Created tables are protected by the intended key (check the table's encryption settings in the console or the API `encryptionConfiguration` field); disabling the key version in a test project produces access errors.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the BigQuery customer-managed encryption page and the Cloud KMS CMEK organization policy page:
location matching, service account trigger and role, dataset and project default keys, destination key flags,
no in-place switching, both constraints and the 15-minute caching, rotation behaviour, availability limits
and the listed limitations. Removed: `bq update --destination_kms_key` on tables (the page documents `bq cp` for
tables and `bq update` only for models), the `bq show | jq` check and the claims that disabled or destroyed key
versions are the only failure modes, that old versions must stay enabled, and about cross-region copy.
