---
id: computing-software.systems-network-administration.restic.exclude-patterns
name: exclude-patterns
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, exclude, patterns, exclude-file, exclude-caches, iexclude]
level: practitioner
status: docs-checked
description: "Exclude files from restic backups using --exclude, --iexclude, exclude files, CACHEDIR.TAG, marker files and size limits, with correct quoting."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Excluding files

## Flags

- `--exclude pattern` and case-insensitive `--iexclude`
- `--exclude-file file` and `--iexclude-file`: patterns listed in a file; empty lines and lines starting with `#` are ignored
- `--exclude-caches`: exclude a folder's content if it contains the special `CACHEDIR.TAG` file (the tag file is kept)
- `--exclude-if-present foo`: exclude a folder's content if it contains a file called `foo` (no wildcards for the file name)
- `--exclude-larger-than size`: default unit is bytes; suffixes k/K (KiB), m/M (MiB), g/G (GiB), t/T (TiB)
- `--exclude-cloud-files`: excludes online-only cloud files (OneDrive Files On-Demand, iCloud Drive); Windows and macOS only

## Patterns

Patterns use Go `filepath.Match` syntax plus the `**` wildcard, and are tested against the full path. Ordinary
wildcards do not match across `/`. `**` matches any number of subdirectories and must be a complete path component
(`foo/**/bar`, not `foo**` or `foo/**bar`). A pattern starting with `!` cancels a match from an earlier pattern, as
in gitignore, but once a directory is excluded files inside it cannot be added back.

In an exclude file, environment variables are expanded with os.ExpandEnv (for example `$USER` in a path); write `$$` for a
literal dollar sign. The tilde `~` is not expanded: use `$HOME` or the platform equivalent. Spaces in exclude-file
patterns are written verbatim (leading and trailing spaces are trimmed). For `--exclude` on the command line restic
needs no escaping, but your shell may.

## Sources named explicitly

Excludes do not apply to backup sources passed explicitly: `restic backup ~/work.txt` always backs up that file.
Content inside a directory you pass is still filtered.

## Test before trusting

`backup --dry-run` reports what would be done without writing to the repository; combined with `--verbose` (twice, or
`--verbose=2`) it lists per-file changes.

## Checked
Compared with the "Backing up" page: all exclude options and their descriptions, the size suffixes, `**` rules,
negation, exclude-file expansion, `$$`, tilde handling, spaces and the dry-run/verbose behaviour. Removed: the
"silently does nothing" quoting-trap example and the claim that restic does no glob expansion on source arguments,
neither of which the page states.
Method: docs-only read of cited pages, 2026-11-08
