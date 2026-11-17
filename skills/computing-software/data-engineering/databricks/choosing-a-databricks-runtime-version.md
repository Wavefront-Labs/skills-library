---
id: computing-software.data-engineering.databricks.choosing-a-databricks-runtime-version
name: choosing-a-databricks-runtime-version
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-runtime, lts, photon, upgrade-planning]
level: practitioner
status: docs-checked
description: "Pick and upgrade Databricks Runtime versions: LTS vs latest, ML and Photon variants, Spark version per DBR, end-of-support dates, upgrade testing."
sources:
  - https://docs.databricks.com/aws/en/release-notes/runtime/
  - https://docs.databricks.com/aws/en/release-notes/runtime/databricks-runtime-ver
  - https://docs.databricks.com/aws/en/compute/photon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a Databricks Runtime version

**Goal:** stable, supported runtimes for production with a planned upgrade path.

## Rules of thumb
- Production jobs: newest **LTS** (long-term support) that your libraries support. Databricks recommends an LTS runtime for job compute running operational workloads and the most current version for all-purpose compute.
- LTS end-of-support dates on the release page sit three years after release (for example 15.4 LTS released Aug 19, 2024, supported to Aug 19, 2027; 17.3 LTS to Oct 22, 2028). A non-LTS release such as 19 shows its end-of-support date as determined at LTS transition.
- ML workloads: the matching **ML** runtime (each listed version has a "for Machine Learning" variant).
- Photon: enabled by default on classic all-purpose, jobs compute and classic Lakeflow pipelines; Photon instances consume DBUs at a different rate than non-Photon ones, so measure. Via the Clusters or Jobs API you must set `runtime_engine` to `PHOTON` explicitly. It does not help UDFs, RDD/Dataset APIs, stateful streaming or queries under about two seconds.

## Find versions
```bash
databricks clusters spark-versions -o json | jq -r '.versions[].key' | grep -i lts
```
The release page lists each supported runtime with its Apache Spark version (for example 15.4 LTS uses Spark 3.5.0, 17.3 LTS uses 4.0.0), release date and end-of-support date.

## Pin, do not float
Use explicit versions in job definitions/bundles. Cluster policies can restrict allowed runtimes (`spark_version` allowlist) so teams do not drift onto unsupported ones.

## Upgrade procedure
1. Read the release notes and the Apache Spark migration guide for the Spark version in the target runtime (`https://spark.apache.org/docs/<version>/migration-guide.html`).
2. Run the job on the new runtime in staging with production-like data (bundle target override of `spark_version`).
3. Compare outputs (row counts, checksums) and runtime/cost.
4. Upgrade in waves; keep the old version pinned for rollback until the next run succeeds.

## Gotchas
- Python minor version changes break pinned wheels compiled for the old version.
- Libraries pre-installed in the runtime may change version under you; pin critical ones explicitly.
- Serverless compute manages versions for you (environment versions instead of DBR).

## Verify
An inventory of cluster and job settings shows no production jobs on runtimes past their end-of-support date.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: the supported-runtime table (Spark versions, release and end-of-support dates, ML variants, 19 end of support determined at LTS transition), the LTS and all-purpose recommendations, Photon defaults, `runtime_engine` PHOTON via API, Photon limitations, DBU-rate wording, the Spark migration guide URL pattern, and the `spark_version` policy attribute (release notes, compute configuration, Photon and policy pages).

Removed or corrected: the "short support window" claim for non-LTS, the 15.4.x-scala2.12 string format, the specific migration-note examples (ANSI defaults, Python version), the system.compute.clusters verify step, and the "costs a higher DBU rate" wording (the page says a different rate).

Method: documentation only; no commands were run.
