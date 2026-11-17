---
id: computing-software.systems-network-administration.immich.cli-upload
name: cli-upload
category: computing-software
field: systems-network-administration
product: immich
tags: [upload, recursive, dry-run, album, ignore, concurrency]
level: practitioner
status: docs-checked
description: "Bulk upload to Immich with immich upload: recursion, dry run, auto albums, ignore globs, visibility, watch mode and JSON output."
sources:
  - https://docs.immich.app/features/command-line-interface
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: upload folders of photos and videos from the command line after logging in with `immich login`.

```bash
immich upload file1.jpg file2.jpg
immich upload --recursive directory/
immich upload --dry-run --recursive directory/
```

Subfolders are skipped unless `--recursive` is set. `--dry-run` shows what would happen without acting; use it first.

Key options (each also reads an environment variable):

- `-a, --album`: create albums from folder names.
- `-A, --album-name <name>`: put everything in one album, for example `immich upload --album-name "My summer holiday" --recursive directory/`.
- `-i, --ignore <pattern>`: skip glob matches, for example `immich upload --ignore **/Raw/** **/*.tif --recursive directory/`.
- `-H, --include-hidden`: include hidden folders (skipped by default).
- `--visibility <archive|timeline|hidden|locked>`: set visibility of uploads.
- `-c, --concurrency <number>`: parallel uploads, default 4.
- `-h, --skip-hash`: do not hash before upload. By default files are hashed to avoid re-uploading; the server deduplicates by hash anyway.
- `--delete`: delete local files after upload; `--delete-duplicates`: delete local files already on the server.
- `--watch`: upload automatically as files change.
- `--no-progress`: hide progress bars.
- `-j, --json-output`: JSON with `newFiles`, `duplicates` and `newAssets`.

JSON output is preceded by log lines that must be stripped before parsing (the docs example skips them with `tail -n +6`):

```bash
immich upload --dry-run --json-output . | tail -n +6 | jq .newFiles[]
```

Use `--delete` only after a dry run and a successful trial upload.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/command-line-interface in full: upload options, defaults, environment variables and examples.
Reworded: the JSON log-line stripping note, to match the docs example.
Method: documentation only; no commands were run.
