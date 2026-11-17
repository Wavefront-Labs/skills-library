---
id: computing-software.devops-ci-cd.gitea.packages-storage
name: packages-storage
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-package-cleanup, gitea, package-cleanup-rules, blob-deduplication, cleanup-packages-cron, keep-versions-regex, older-than-days]
level: advanced
status: docs-checked
description: "Manage Gitea package storage: blob deduplication, the cleanup_packages job and OLDER_THAN, cleanup rule settings, anchored case-insensitive regexes and evaluation order."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/packages/storage.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea package storage and cleanup

## Deduplication
Identical uploaded blobs are stored once. Two packages with identical files each show the full size but together use half on disk. Deleting a package removes only references; the blobs stay and may be re-referenced by a later upload. Unreferenced blobs are removed by the cleanup job (`cron.cleanup_packages` in the config cheat sheet); its `OLDER_THAN` setting says how long unreferenced blobs are kept first. So deleting packages does not free disk immediately.

## Cleanup rules
Each package owner (user or organization) manages rules for their own packages. Fields:
- **Enabled**
- **Type**: each rule manages one package type
- **Apply pattern to full package name**: patterns match `package/version` instead of just `version`
- **Keep the most recent**: versions always kept per package
- **Keep versions matching**: regex; empty keeps nothing, `.+` keeps all. The container registry always keeps `latest`
- **Remove versions older than**: days
- **Remove versions matching**: regex; empty or `.+` removes everything unless another setting excludes it
A preview shows the affected packages; use it before enabling.

## Regex rules
Patterns are automatically wrapped in `\A` and `\z`; do not add `^`, `$`, `\A` or `\z`. Case-insensitive. Examples: `.*` all; `v.+` starts with v; `release` exactly that; `.+-temp-.+` contains `-temp-`; `v.+|release`; with full-name matching, `package/v.+|other/release`.

## Order of evaluation (run periodically in the cleanup job)
1. Collect all packages of the type for the owner.
2. Collect all versions of each.
3. Drop the N most recent from the list.
4. Drop versions matching "keep".
5. Drop versions newer than "older than".
6. Drop versions not matching "remove".
7. Delete what is left.
Because only the leftover is deleted, a rule with an empty remove pattern is dangerous when the other filters leave versions in the list; always preview.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
