---
id: computing-software.data-engineering.databricks.unity-catalog-volumes
name: unity-catalog-volumes
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, unity-catalog, uc-volumes, managed-volume, external-volume, dbfs-mounts-migration, file-governance, read-volume, write-volume]
level: practitioner
status: docs-checked
description: "Govern non-tabular files with Unity Catalog volumes: managed vs external, /Volumes paths, privileges, access methods, replacing DBFS mounts."
sources:
  - https://docs.databricks.com/aws/en/volumes/
  - https://docs.databricks.com/aws/en/volumes/volume-files
  - https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-volume
  - https://docs.databricks.com/aws/en/dbfs/unity-catalog
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity Catalog volumes

**Goal:** landing files, exports, ML artefacts, libraries and init scripts governed by Unity Catalog grants instead of DBFS mounts that anyone on a cluster can read.

## 1. Create
```sql
CREATE VOLUME prod.landing.partner_files COMMENT 'raw partner drops';             -- managed: UC owns storage
CREATE EXTERNAL VOLUME prod.landing.legacy_drop
  LOCATION 's3://company-landing/legacy/';                                          -- under an external location
GRANT READ VOLUME, WRITE VOLUME ON VOLUME prod.landing.partner_files TO `ingest_sp`;
GRANT READ VOLUME ON VOLUME prod.landing.partner_files TO `data_engineers`;
```
- Managed volumes: UC manages layout and deletion (7-day retention on delete). External volumes: dropping removes only the UC object.
- External volume locations cannot overlap tables or other volumes.

## 2. Paths and access
Path form: `/Volumes/<catalog>/<schema>/<volume>/<path>`.
```python
df = spark.read.format("csv").option("header", True).load("/Volumes/prod/landing/partner_files/2026/10/")
dbutils.fs.ls("/Volumes/prod/landing/partner_files/")
with open("/Volumes/prod/landing/partner_files/readme.txt") as f: print(f.read())    # POSIX-style access
```
```bash
databricks fs cp ./local.csv dbfs:/Volumes/prod/landing/partner_files/local.csv
databricks fs ls dbfs:/Volumes/prod/landing/partner_files/
```
```sql
SELECT * FROM read_files('/Volumes/prod/landing/partner_files/2026/10/', format => 'csv', header => true);
LIST '/Volumes/prod/landing/partner_files/';
```
Use the Files API (REST) or the SDKs for apps outside Databricks.

## 3. What to put in volumes (and what not)
- Yes: landing zones for Auto Loader/COPY INTO, exports for partners, model artefacts, images/PDFs for unstructured pipelines, wheel files, JARs, init scripts.
- No: tabular data you query repeatedly — make it a table (governed per column/row, optimised, lineage).
- Auto Loader checkpoints/schema locations work well in a dedicated `_meta` volume.

## 4. Migrating off DBFS mounts
- Map each `/mnt/<x>` to an external location + external volume (or the table it really is).
- Replace paths in code: `/mnt/landing/...` → `/Volumes/prod/landing/legacy_drop/...`; grep notebooks and jobs for `/mnt/` and `dbfs:/mnt/`.
- DBFS mounts bypass Unity Catalog entirely and are deprecated; do not reuse the same storage between mounts and external volumes. Remove mounts once code is migrated.

## Verify
- [ ] Users without `READ VOLUME` get permission denied on the path.
- [ ] No production code references `/mnt/` paths.
- [ ] Ingestion service principal has `WRITE VOLUME` only on the landing volume.

## Checked

2026-11-09. Confirmed on the volumes overview, CREATE VOLUME, DBFS-with-Unity-Catalog and privileges pages: managed vs external volumes, 7-day retention on managed delete, /Volumes/<catalog>/<schema>/<volume>/<path> and the optional dbfs:/ prefix, external location must not overlap other volumes or tables, READ VOLUME and WRITE VOLUME privileges, mounts bypass Unity Catalog and are deprecated, LIST SQL command and databricks fs commands for volume files, Files API. Runtime 13.3 LTS or above is required. Removed: init-script allowlist claim and the SDK method name (not on the pages read). The volume-files page was read for its summary lines only.

Method: documentation only; no commands were run.

