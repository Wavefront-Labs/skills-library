---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.reuse-migrating-legacy-repos
name: reuse-migrating-legacy-repos
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [reuse-migrating-legacy-repos, reuse-specification, legacy repo, bulk annotate, scancode, git blame, headers migration, relicense audit, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Bulk-annotate a legacy repo using licence detection, ownership analysis and per-directory rules."
sources:
  - https://reuse.software/spec-3.3/
  - https://reuse.software/tutorial/
  - https://reuse.software/dev/
  - https://github.com/fsfe/reuse-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating a legacy repository to REUSE

Goal: reach compliance without hand-editing thousands of files.

Method:
1. Inventory existing licences and copyrights; reuse lint lists the files that lack information.
2. Determine ownership from your records (for example version control history) and company policy.
3. Use reuse annotate with --recursive and --skip-unrecognised to insert headers where licence is uniform.
4. Use REUSE.toml path globs for generated and binary assets.
5. Resolve conflicts: files with mixed or unknown licences need manual review.
6. Commit in one dedicated change to ease review.

Gotchas:
- Do not guess licences; unknown stays flagged.
- Corporate copyright notices should follow legal guidance.

Verify: reuse lint passes and diff review confirms no code changes.

## Checked

2026-11-02. Checked against the reuse-tool man pages (reuse annotate --recursive and --skip-unrecognised, REUSE.toml) and the REUSE 3.3 specification (REUSE.toml annotations). Removed: ScanCode and the git log command (not in the REUSE pages).

Method: documentation only; no commands were run.
