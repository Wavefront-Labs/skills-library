---
id: computing-software.cloud-infrastructure-engineering.google-cloud.sensitive-data-protection-dlp
name: sensitive-data-protection-dlp
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sensitive-data-protection, cloud-dlp, dlp, de-identification, infotypes, inspection-templates, deidentify-templates, discovery-scans, data-profiles, pii-detection, tokenization, format-preserving-encryption, fpe-ffx, crypto-hashing, redaction, bigquery-dlp, gcs-dlp, dlp-jobs, data-classification]
level: practitioner
status: docs-checked
description: "Find and neutralise PII with Sensitive Data Protection: data profiles, inspection jobs and templates, de-identification (masking, hashing, AES-SIV, FPE)."
sources: ["https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles", "https://docs.cloud.google.com/sensitive-data-protection/docs/inspecting-storage", "https://docs.cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data", "https://docs.cloud.google.com/sensitive-data-protection/docs/creating-templates-inspect", "https://docs.cloud.google.com/sensitive-data-protection/docs/pseudonymization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive Data Protection (Cloud DLP)

**Goal:** know where sensitive data lives, and feed de-identified copies to analytics and lower environments instead of the real thing.

## 1. Three modes
| Mode | What |
|---|---|
| **Discovery (data profiler)** | continuous monitoring of an organization, folder or project; classifies data into infoTypes and produces profiles with sensitivity and risk levels |
| **Inspection jobs** | scan a specific Cloud Storage location, Datastore kind or BigQuery table and report findings |
| **Content methods** (`content.inspect`, `content.deidentify`, reidentify) | synchronous calls from your code |
For pricing of each mode see Google's Sensitive Data Protection pricing page; no figures are kept here.

## 2. Discovery (data profiles)
- **Coverage:** BigQuery and BigLake (table, column and project profiles; not BigQuery Omni, non-BigLake external tables such as Sheets, or tables with rows over 128 MB serialized), Cloud SQL (you must give connection details per instance first), Cloud Storage (bucket-level file store profiles with file clusters), Vertex AI, and S3 and Azure Blob Storage. Cloud Run environment variables are checked for secrets and reported to Security Command Center without profiles.
- **Actions:** publish findings to Security Command Center and Knowledge Catalog; Pub/Sub notification when a profile's sensitivity level changes; save profile copies to BigQuery (you control the dataset expiry).
- **Frequency:** an initial scan when the configuration is created, new or modified data profiled shortly after; default reprofiling waits 30 days and only reprofiles if there are changes. Options are do not reprofile, daily, weekly or monthly, or on a fixed schedule. Reprofiling can take up to 24 hours. A forced reprofile is available manually.
- **Service agent:** organization and folder scans use a service agent container project (billing tracking) with agent `service-<PROJECT_NUMBER>@dlp-api.iam.gserviceaccount.com`; project-level scans need no container. Roles: DLP Administrator (`roles/dlp.admin`) to create and view configurations; DLP Data Profiles Reader (`roles/dlp.dataProfilesReader`) and DLP Reader (`roles/dlp.reader`) for read-only access.
- **Regions:** data stays in place. A regional inspection template only profiles data in its region; a `global` template covers regions without a dedicated one, otherwise profiling fails there. Unsupported regions are skipped with an error. Only one configuration per scope and discovery type; the closest organization or folder configuration to the project applies.
- The latest profile version is kept indefinitely; each reprofile replaces the previous one.

## 3. Inspection templates
An inspection template wraps an `InspectConfig`: `infoTypes` (do not leave blank, or a default set is used), `minLikelihood` (five levels, default Possible), `includeQuote` (matched text in findings; leave off if findings must not contain the data) and `limits.maxFindingsPerRequest` (0 means server maximum). Rulesets support hotword rules (a regular expression before or after an infoType within a character distance, fixed or adjusted likelihood), exclusion rules (regex, phrase, hotword, context infoType; full, partial or inverse matching) and adjustment rules. You can create up to 1000 templates, in a region or Global, via console, `projects.inspectTemplates` / `organizations.inspectTemplates` `create`, or a client library. Reference one by name in `content.inspect`, `content.deidentify` or `dlpJobs.create`; updates apply to job triggers that use it.

## 4. Inspection jobs on storage
Request body `inspectJob` with `storageConfig`, `inspectConfig` and `actions`; REST `POST https://dlp.googleapis.com/v2/projects/<PROJECT_ID>/dlpJobs` (samples use parent `projects/<PROJECT_ID>/locations/global`).
- Cloud Storage: `cloudStorageOptions.fileSet.url` such as `gs://<BUCKET>/*` (one `*` is that directory only, `**` is recursive); the sample also sets `bytesLimitPerFile`. Datastore: `datastoreOptions` with `kind.name` and `partitionId`.
- Sampling is recommended to reduce latency; for CSV, TSV and Avro the sample must cover the full header and at least one data row.
- Actions: `saveFindings` to a BigQuery table; `pubSub` completion notification (match jobs with the `DlpJobName` attribute).
- Job triggers run scans daily, weekly or quarterly and can inspect only data changed since the last scan.
- Cancelling a job midway still charges for the completed portion.

## 5. De-identification
Config names on the de-identification and pseudonymization pages: `replaceConfig`, `redactConfig`, `characterMaskConfig`, `cryptoHashConfig`, `dateShiftConfig`, plus the pseudonymization methods below.
| Method | Config | Reversible | Notes |
|---|---|---|---|
| Deterministic encryption (AES-SIV) | `CryptoDeterministicConfig` | yes | min input 1 character; base64 output with optional surrogate prefix |
| Format-preserving (FPE-FFX) | `CryptoReplaceFfxFpeConfig` | yes | min input 2 characters, ASCII only; output same length in a defined alphabet |
| Cryptographic hashing (HMAC-SHA-256) | `cryptoHashConfig` | no | string or integer input; base64 output |
- Keys: a Cloud KMS wrapped key (128, 192 or 256-bit key wrapped by a KMS key) is the preferred option and is needed to re-identify; a transient key is generated and discarded per request so cannot re-identify; an unwrapped raw key is not recommended outside testing. The `cryptoHashConfig` key must be 32 or 64 bytes.
- FPE alphabets: `NUMERIC`, `HEXADECIMAL`, `UPPER_CASE_ALPHA_NUMERIC`, `ALPHA_NUMERIC`, a radix from 2 to 95, or a custom character list. Small input or alphabet spaces can be reverse-engineered: increase the radix or use a context tweak.
- Re-identifying free text needs a surrogate infoType; for structured data in a `RecordTransformation` the surrogate annotation is optional.
- `InfoTypeTransformations` apply to matching values in text; `RecordTransformations` apply to matching values or whole columns in tabular data.

## Gotchas
- Profiles and templates are regional: a missing regional or `global` template makes profiling fail in that region.
- Unsupported data (Omni tables, Sheets-backed tables) is silently outside profiles.
- Detection thresholds and rules are yours to tune per infoType; test on seeded data first.

## Verify
- [ ] A seeded table appears in a data profile with the expected infoTypes.
- [ ] An inspection job on a sample prefix reports the planted infoTypes and, with `includeQuote` off, no quoted text.
- [ ] `deidentify` with FPE then reidentify round-trips a value of the same length and alphabet.

## Checked
Checked 2026-11-08 against the Sensitive Data Protection pages on data profiles, inspecting storage, de-identification, inspection templates and pseudonymization. Removed (not stated in those pages): cost-model column and "five-figure invoice", Terraform resource names, the `gcloud dlp` remark, discovery fields `sensitivityScore` and `dataRiskLevel` with LOW/MODERATE/HIGH, specific IAM roles for BigQuery/GCS/Cloud SQL scanning, custom infoType JSON and `filesLimitPercent`/`RANDOM_START` sampling parameters, `publishSummaryToCscc`, `bucketingConfig`/`timePartConfig`, Dataflow templates and remote functions, PDF and image-redaction remarks, the KMS service agent role for FPE, and the 95 percent profiling target. The pages were read through a page-summarising fetch tool, which truncated the longest pages; claims kept are those the summaries quoted.
Method: documentation only; no commands were run.
