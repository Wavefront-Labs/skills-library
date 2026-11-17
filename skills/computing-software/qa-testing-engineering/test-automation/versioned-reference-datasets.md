---
id: computing-software.qa-testing-engineering.test-automation.versioned-reference-datasets
name: versioned-reference-datasets
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [reference-datasets, test-data-management, golden-datasets, dvc, data-versioning]
level: practitioner
status: draft
description: "Maintain versioned reference datasets for tests: what to include, storage with Git LFS or DVC, checksums, regeneration scripts and change review."
sources:
  - https://dvc.org/doc
  - https://git-lfs.com/
  - https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Versioned reference datasets

**Goal:** stable, known input datasets (and expected outputs) that tests, benchmarks and demos rely on, with every change deliberate and traceable.

## What belongs in a reference dataset
- Representative records covering partitions and edge cases (one customer per segment, unusual names, max-length fields).
- Known-answer records for calculations (with expected results alongside).
- Size tiers: `small` for unit/CI, `medium` for integration, `large` for performance (generated, not hand-made).
- A README: purpose, schema version, how generated, owner, and privacy statement (synthetic or masked).

## Storage
| Size | Store |
|---|---|
| < ~10 MB text | plain Git next to tests |
| Large binaries | Git LFS (`git lfs track "*.parquet"`) |
| Large or many versions, ML data | DVC (`dvc add data/ref_v3`, `dvc push` to S3/GCS; `.dvc` pointer files in Git) |

## Versioning
- Version datasets explicitly (`ref-customers/v3/`), tests pin a version.
- Record a checksum manifest (`sha256sum * > MANIFEST.sha256`) and verify it at test start to detect accidental edits or partial downloads.
- Regeneration is a script in the repo (seeded Faker generators, export queries plus masking), never manual edits.
- Schema changes: migrate the dataset with the same migration scripts as production, bump the version, keep the old one until tests move.

## Change review
Dataset diffs in PRs (row counts, schema, sample diff); for big files, CI posts a summary (rows added/removed per partition). Owners approve changes.

## Gotchas
- Production extracts used as reference data must be masked and approved; synthetic is safer.
- Shared mutable copies drift; load fresh from the versioned source per run.
- LFS bandwidth quotas on hosted Git; cache in CI.

## Verify
Tests reference a dataset version, the checksum check passes in CI, and the dataset can be rebuilt from its script to the same checksum.
