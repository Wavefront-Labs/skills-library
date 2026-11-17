---
id: computing-software.systems-network-administration.restic.environment-variables
name: environment-variables
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, environment-variables, configuration, cache-dir, host, scripting]
level: practitioner
status: docs-checked
description: "Configure restic through RESTIC_* environment variables for repository, password, cache, compression, pack size and concurrency, plus backend credentials."
sources:
  - https://restic.readthedocs.io/en/stable/075_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables

Restic also accepts these settings as command-line options; several variables replace a specific option, for example `RESTIC_REPOSITORY` replaces `-r`.

## Repository and access

- `RESTIC_REPOSITORY`, `RESTIC_REPOSITORY_FILE`
- `RESTIC_PASSWORD`, `RESTIC_PASSWORD_FILE`, `RESTIC_PASSWORD_COMMAND`
- `RESTIC_KEY_HINT`
- `RESTIC_CACERT`, `RESTIC_TLS_CLIENT_CERT`

## Behaviour

- `RESTIC_CACHE_DIR`: where the local cache lives
- `RESTIC_COMPRESSION`: `off`, `fastest`, `auto`, `better`, `max` (format version 2 only)
- `RESTIC_HOST`: override the hostname recorded in snapshots
- `RESTIC_PROGRESS_FPS`: frames per second for the progress bar
- `RESTIC_PACK_SIZE`: target pack size, an integer in MiB (default 16 MiB)
- `RESTIC_READ_CONCURRENCY`: file read concurrency
- `RESTIC_FEATURES`: comma-separated feature flags (`key[=value]`)
- `TMPDIR` (Windows: `TMP`): location for temporary files, including temporary pack files

## Copy source

`RESTIC_FROM_REPOSITORY`, `RESTIC_FROM_REPOSITORY_FILE`, `RESTIC_FROM_PASSWORD`, `RESTIC_FROM_PASSWORD_FILE`, `RESTIC_FROM_PASSWORD_COMMAND`, `RESTIC_FROM_KEY_HINT`.

## Backends

S3 uses `AWS_*`, Azure `AZURE_*`, B2 `B2_*`, Google `GOOGLE_*`, Swift `OS_*` and `ST_*`, REST `RESTIC_REST_USERNAME` and `RESTIC_REST_PASSWORD`, rclone `RCLONE_BWLIMIT`.

`RESTIC_HOST` also limits which snapshots are considered to that host.

## Checked

2026-11-03. Confirmed in the restic docs pages Scripting (variable list) and Tuning parameters (compression modes, pack size default and unit, `RESTIC_FEATURES` format, temp directory). Removed: the claim that flags override variables, `RESTIC_IGNORE_CTIME` and `RESTIC_IGNORE_INODE` (not listed in the variable table), and the advice paragraphs about stable host names and password visibility (the FAQ passage is covered in repository-password-sources).

Method: documentation only; no commands were run.
