---
id: computing-software.devops-ci-cd.ci-pipeline-design.fixture-versioning-and-golden-datasets
name: fixture-versioning-and-golden-datasets
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, fixture-versioning, test-data-management, factories]
level: practitioner
status: draft
description: "Version test fixtures and golden datasets alongside schema changes: fixture migrations, regeneration scripts, Git LFS or object storage for large data, and review practices."
sources: ["https://docs.pytest.org/en/stable/how-to/fixtures.html", "https://git-lfs.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixture versioning and golden datasets

Static fixtures rot when the schema changes; tests then fail for the wrong reasons or silently test
old shapes.

## Practices
- Fixtures live next to the tests in the same repo and change in the same PR as the schema.
- Prefer **generated** fixtures: a script builds them from factories/migrations, committed output
  is reproducible:
  ```bash
  make fixtures   # runs migrations on empty DB, seeds via factories, pg_dump --data-only > testdata/seed.sql
  git diff --exit-code testdata/   # CI: fails if someone changed generators but not outputs
  ```
- Record the schema version in the fixture (`-- schema: 20261015_add_orders`) and assert it in tests.
- Golden datasets for ML/analytics (input + expected output): version with a content hash in the file
  name or a manifest (`data/golden/v3/manifest.json` with sha256 per file).

## Large data
- Git LFS for tens to hundreds of MB; track patterns in `.gitattributes`
  (`testdata/**/*.parquet filter=lfs diff=lfs merge=lfs -text`). CI needs `lfs: true` on checkout.
- Bigger: object storage with versioned keys (`s3://test-data/golden/v3/`) + DVC or a manifest;
  download and verify hashes in CI, cache by version.

## Review
Fixture diffs are data diffs; keep them small and sorted (stable ordering in dumps:
`ORDER BY` primary keys) so reviews are meaningful.

## Verify
- [ ] Changing a migration without regenerating fixtures fails CI.
