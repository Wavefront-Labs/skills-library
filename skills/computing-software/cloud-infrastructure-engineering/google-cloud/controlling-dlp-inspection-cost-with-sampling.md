---
id: computing-software.cloud-infrastructure-engineering.google-cloud.controlling-dlp-inspection-cost-with-sampling
name: controlling-dlp-inspection-cost-with-sampling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sensitive-data-protection, dlp-cost-control, dlp-sampling, rows-limit, bytes-limit-per-file, discovery-pricing]
level: practitioner
status: docs-checked
description: "Keep Sensitive Data Protection costs predictable: BigQuery and Cloud Storage sampling fields, changed-data-only scans, and discovery pricing modes."
sources: ["https://cloud.google.com/sensitive-data-protection/docs/inspecting-storage#sampling", "https://cloud.google.com/sensitive-data-protection/pricing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling DLP inspection cost with sampling

Prices are not kept here: see the Sensitive Data Protection pricing page.

Storage inspection jobs (`projects.dlpJobs.create`) are billed on bytes inspected, so scanning less data costs less. Sampling returns a sample of results without scanning the whole dataset.

## BigQuery jobs (fields in `BigQueryOptions`)
- `rowsLimit`: maximum rows to scan; unset or 0 scans all rows.
- `rowsLimitPercent`: 0 to 100; 0 or 100 means no limit; only one of `rowsLimit` and `rowsLimitPercent` may be set. The page cautions that a known issue makes `rowsLimitPercent` behave unexpectedly and recommends `rowsLimit` instead.
- `sampleMethod`: `TOP` (from the top, the default) or `RANDOM_START` (from a randomly selected row).
- `excludedFields`: columns to leave unread, which reduces data scanned and cost.
- `includedFields`: the page describes these as fields identifying specific rows to scan.
- `TimespanConfig` filters rows by a start and end timestamp, useful for partitioned tables; only rows with a timestamp in the span are scanned.
- When sampling a structured file such as CSV, TSV or Avro, make the sample big enough to cover the full header and a row of data.

## Cloud Storage jobs (fields in `CloudStorageOptions`)
- `bytesLimitPerFile`: maximum bytes read per file; the rest is omitted. It has no effect on certain file types.
- `filesLimitPercent`: share of the input file set to scan; 0 or 100 means no limit.
- `fileTypes[]`: file types to include.
- `sampleMethod`: `TOP` or `RANDOM_START`; meaningful only together with `bytesLimitPerFile`. `RANDOM_START` picks a random offset in each file larger than the limit and scans contiguous bytes.
- Images cannot be sampled: the whole image is scanned and billed at the file size.

## Scope and schedule
- Start with one table, one bucket or a few files plus sampling, to tune detectors and exclusion rules before scaling up.
- Avoid enabling infoTypes you do not need; broad ones such as DATE, TIME, DOMAIN_NAME and URL match widely and may not help on large scans. PERSON_NAME and FEMALE_NAME among others can make requests run much more slowly.
- Job triggers run scans daily, weekly or quarterly and can inspect only data changed since the last scan, saving time and cost.

## Discovery (data profiles)
- Two pricing modes: consumption (charged on bytes profiled, the default) and subscription (reserved capacity in units, billed continuously while deployed, no charge for bytes profiled; costs stay predictable as data grows).
- The page describes an estimate feature for BigQuery and BigLake discovery, at organisation, folder or project level.

## Gotchas
- Sampling can miss rare sensitive values; scan high-risk data in full.
- Hybrid jobs and content methods are billed on bytes inspected too, and hybrid requests have a 1 KB minimum.

## Checked
Confirmed 2026-11-08 against the inspecting-storage (sampling) and pricing pages. Removed claims the pages do not state: the `bytesLimitPerFilePercent` field, the `enableAutoPopulationOfTimespanConfig` setting, the reprofile-frequency advice, the `maxFindingsPerRequest` and `content:inspect` notes, and the billing-export check. The estimate-inspection-cost source returned 404 and was dropped.
Method: docs-only read of cited pages, 2026-11-08
