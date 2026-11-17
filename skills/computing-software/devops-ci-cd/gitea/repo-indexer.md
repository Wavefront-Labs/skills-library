---
id: computing-software.devops-ci-cd.gitea.repo-indexer
name: repo-indexer
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-repo-indexer, gitea, repo-indexer-enabled, bleve, git-grep-search, repo-indexer-exclude, gobwas-glob]
level: practitioner
status: docs-checked
description: "Enable Gitea code search with the repo indexer: [indexer] keys, MAX_FILE_SIZE, include/exclude glob patterns and precedence, plus the default git grep fallback."
sources: ["https://docs.gitea.com/administration/repo-indexer/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repository indexer (code search)

Without an indexer, repository-level code search uses `git grep` (fine for small repos). Enable the indexer for better search:
```ini
[indexer]
REPO_INDEXER_ENABLED = true
REPO_INDEXER_PATH = indexers/repos.bleve
MAX_FILE_SIZE = 1048576
REPO_INDEXER_INCLUDE =
REPO_INDEXER_EXCLUDE = resources/bin/**
```
First-time and global re-indexing (for example after an upgrade) can use a lot of resources.

- `MAX_FILE_SIZE`: files larger than this many bytes are skipped.
- `REPO_INDEXER_EXCLUDE_VENDORED` (default true) skips vendored files.
- `REPO_INDEXER_INCLUDE` (comma-separated globs, default empty means all files) and `REPO_INDEXER_EXCLUDE` (default empty). **Exclude wins over include.** Use them to keep derived files (lss, sym, map ...) out and the index small.

## Glob semantics (gobwas/glob)
- `**.txt` all `.txt` in any directory; `*.txt` only at the repository root.
- `resources/bin/**` everything below; `resources/bin/*` only directly inside.
- `**Makefile` any file named Makefile.
- A bare directory pattern (`resources/bin`) matches nothing; you need `/**`.
- Files and patterns are lower-cased, so `**Makefile`, `**makefile`, `**MAKEFILE` are equal.

Related: the dump flag `--skip-index` skips Bleve data in backups (see `gitea-dump-restore`).

## Checked

2026-11-03: read https://docs.gitea.com/administration/repo-indexer/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
