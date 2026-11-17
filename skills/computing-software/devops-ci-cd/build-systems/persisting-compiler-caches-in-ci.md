---
id: computing-software.devops-ci-cd.build-systems.persisting-compiler-caches-in-ci
name: persisting-compiler-caches-in-ci
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, ccache-ci, ccache, sccache, compiler-cache, actions-cache, cache-hit-rate]
level: practitioner
status: docs-checked
description: "Persist ccache or sccache between CI runs: cache directories and keys, size limits, path normalisation for hits across runners, cloud storage backends, and measuring hit rate."
sources: ["https://ccache.dev/manual/latest.html", "https://github.com/hendrikmuhs/ccache-action", "https://github.com/mozilla/sccache/tree/main/docs", "https://github.com/Mozilla-Actions/sccache-action", "https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Persisting compiler caches in CI

## ccache with the CI cache
```yaml
# GitHub Actions
- uses: hendrikmuhs/ccache-action@v1.2
  with:
    key: ${{ runner.os }}-${{ matrix.compiler }}-${{ matrix.build_type }}
    max-size: 2G
- run: |
    cmake -B build -G Ninja -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
    cmake --build build
    ccache --show-stats -v
```
Manual equivalent: `actions/cache` on the ccache directory (`$CCACHE_DIR`) with a key that includes `github.sha` and a `restore-keys` prefix, so every run restores the newest cache and saves a new one.
GitLab: `cache: { key: ccache-$CI_JOB_NAME, paths: [.ccache/] }` with `CCACHE_DIR=$CI_PROJECT_DIR/.ccache` (cache paths must be inside the project directory).

## Settings that make hits happen
```bash
export CCACHE_DIR=$PWD/.ccache
export CCACHE_BASEDIR=$PWD          # rewrite absolute paths under the checkout to relative -> hits across different checkout dirs
export CCACHE_NOHASHDIR=true        # do not hash the current directory (relevant for -g debug info)
export CCACHE_COMPILERCHECK=content # hash the compiler binary content instead of mtime and size
export CCACHE_MAXSIZE=2G
export CCACHE_SLOPPINESS=pch_defines,time_macros,include_file_mtime,include_file_ctime
ccache -z                           # zero stats at job start, then --show-stats at end
```
`__DATE__`/`__TIME__` macros and absolute paths in the command line are classic hit-rate killers (see the ccache manual's troubleshooting section).

## sccache with cloud storage (no restore/save step)
```yaml
- uses: mozilla-actions/sccache-action@v0.0.11
- env:
    SCCACHE_GHA_ENABLED: "true"      # GitHub Actions cache backend
    RUSTC_WRAPPER: sccache
    CARGO_INCREMENTAL: "0"
  run: cargo build --release && sccache --show-stats
```
Or S3: `SCCACHE_BUCKET`, `SCCACHE_REGION`, optional `SCCACHE_ENDPOINT`, and `SCCACHE_S3_KEY_PREFIX` to scope keys per project; GCS and Azure backends are also documented. Objects are fetched per compilation, so cache size does not slow job start. The S3 and GitHub Actions backends accept `SCCACHE_S3_RW_MODE=READ_ONLY` / `SCCACHE_GHA_RW_MODE=READ_ONLY`; use read-only access for PR jobs to avoid poisoning the shared cache.

## Size and eviction
- GitHub Actions cache: 10 GB per repository by default (configurable); entries not accessed for 7 days are removed; caches per matrix leg multiply quickly. Share caches across similar legs.
- `ccache --evict-older-than 7d` removes entries not used for 7 days; run it before saving to keep the cache lean.
- Only save from main-branch builds; PRs restore main's cache.

## Measure
`ccache -s`: cacheable calls, hits (direct/preprocessed) and misses. A drop to near zero after a toolchain change is expected once.

## Verify
- [ ] A second run of the same commit shows hits for (almost) every compilation and a shorter compile time.
- [ ] PR builds restore main's cache and show high hit rates.

## Checked
Date: 2026-10-25. Documentation: ccache manual (`doc/manual.adoc`), hendrikmuhs/ccache-action and Mozilla-Actions/sccache-action READMEs, mozilla/sccache docs (`GHA.md`, `S3.md`, `Configuration.md`), GitHub's dependency-caching reference (github/docs).
Confirmed: ccache variable names and meanings (`CCACHE_BASEDIR`, `CCACHE_NOHASHDIR`, `CCACHE_COMPILERCHECK`, `CCACHE_MAXSIZE`, `CCACHE_SLOPPINESS` values); `--evict-older-than` with `d` suffix; sccache-action `v0.0.11` and `SCCACHE_GHA_ENABLED` / `RUSTC_WRAPPER` usage; `SCCACHE_BUCKET`, `SCCACHE_REGION`, `SCCACHE_ENDPOINT`, `SCCACHE_S3_KEY_PREFIX`, `SCCACHE_S3_RW_MODE`, `SCCACHE_GHA_RW_MODE`; GitHub cache limits and eviction; `actions/cache` key and `restore-keys` semantics.
Removed: the `SCCACHE_S3_NO_CREDENTIALS` variable (not documented as an environment variable; read-only mode is `*_RW_MODE=READ_ONLY`), the ">80% / >95% hit" targets, the "(4.4+)" gate on `--evict-older-than`.
Method: documentation only; no commands were run.
