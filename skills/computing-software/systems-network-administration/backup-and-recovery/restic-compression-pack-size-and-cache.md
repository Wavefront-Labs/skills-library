---
id: computing-software.systems-network-administration.backup-and-recovery.restic-compression-pack-size-and-cache
name: restic-compression-pack-size-and-cache
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-compression, restic-pack-size, restic, restic-cache, backup-performance, repository-v2]
level: advanced
status: docs-checked
description: "Tune restic compression levels, pack size, cache location, backend connections and read concurrency, with the temporary-space cost of larger packs."
sources:
  - https://restic.readthedocs.io/en/stable/047_tuning_parameters.html
  - https://restic.readthedocs.io/en/stable/manual_rest.html#caching
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# restic compression, pack size and cache tuning

**Goal:** faster backups and lower storage/request costs without surprises at restore time.

## Compression (repository format v2, restic 0.14+)
```sh
restic backup --compression auto /data     # default
restic backup --compression max /data      # modes: off, fastest, auto, better, max
restic backup --compression off /media     # already-compressed data (video, jpg, zip)
export RESTIC_COMPRESSION=max
```
v1 repositories cannot compress; upgrade with `restic migrate upgrade_repo_v2` first.

## Pack size
Default target pack size is 16 MiB (created packs may be larger). Raise it for very large repositories (TiB range), very fast uploads, or backends with hard limits on object count:
```sh
restic backup --pack-size 64 /data         # target size in MiB
export RESTIC_PACK_SIZE=64
```
Bigger packs mean fewer objects, but need temporary space of pack size x (backend connections + 1) in the temp directory (`TMPDIR`; `TMP` on Windows), more memory on some backends, and more SSD wear if packs reach disk. Specify the setting on every command that modifies the repository.

## Parallelism
- `-o <backend>.connections=N` sets backend concurrency (for example `-o s3.connections=10`, `-o rest.connections=5`); the default is 5 per backend and 2 for the local backend. Too many connections degrade performance.
- `--read-concurrency N` (or `RESTIC_READ_CONCURRENCY`; default 2) reads more files in parallel, useful on fast storage such as NVMe.
- `GOMAXPROCS=1` limits CPU use; `--limit-upload` and `--limit-download` take KiB/s.
- `backup --no-extra-verify` skips the pre-upload decode check to save CPU; if used, run `restic check --read-data` or `--read-data-subset` more often.

## Cache
- Default on Linux is `$XDG_CACHE_HOME/restic`, else `~/.cache/restic`; macOS `~/Library/Caches/restic`; Windows `%LOCALAPPDATA%/restic`. The cache is ephemeral: anything missing is reloaded from the repository.
- Override with `--cache-dir` or `RESTIC_CACHE_DIR`: `--cache-dir /var/cache/restic`.
- `restic cache --cleanup` removes cache directories older than `--max-age` (default 30 days); the `--cleanup-cache` flag does it as part of another command.
- `--no-cache` disables the cache, so all data is loaded from the repository.

## Gotchas
- If the environment variables that locate the cache directory are not set (for example some service managers), restic exits with an error; set `--cache-dir` or `RESTIC_CACHE_DIR` explicitly.
- The compression level of data already stored cannot be changed later; the setting applies per run.

## Verify
Compare `restic stats --mode raw-data` and backup duration before and after a change.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: compression modes and default auto, v2-only compression, 16 MiB default pack size and temp-space formula, connection defaults (5, local 2), read-concurrency default 2, GOMAXPROCS, KiB/s limits, cache locations, --cleanup-cache and cache --cleanup --max-age=30. Removed unconfirmed claims (zstd level, 128 MiB maximum, GB-per-TB cache sizing, request-cost effects).

Method: documentation only; no commands were run.
