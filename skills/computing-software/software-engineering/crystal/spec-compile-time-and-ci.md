---
id: computing-software.software-engineering.crystal.spec-compile-time-and-ci
name: spec-compile-time-and-ci
category: computing-software
field: software-engineering
product: crystal
tags: [spec-compile-time-and-ci, spec-framework, ci, junit, tap, coverage, spec-ci, compile-error-test, github-actions, kcov, crystal]
level: advanced
status: docs-checked
description: "Run specs in CI with random order and JUnit/TAP output as runner options, install shards with --production, and use install-crystal or Docker images."
sources:
  - https://crystal-lang.org/reference/latest/man/crystal/
  - https://crystal-lang.org/reference/latest/man/shards/
  - https://github.com/crystal-lang/install-crystal
  - https://hub.docker.com/r/crystallang/crystal
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spec in CI, JUnit output and compile-error tests

Goal: reliable CI.

- Command: `shards install --production && crystal spec -- --order random --junit_output ./out`. Runner options (`--order`, `--junit_output`, `--tap`, `--fail-fast`, `--verbose`, `--profile`) go after a `--` separator because they are given to the compiled spec binary; `--junit_output <output_dir>` writes JUnit XML, `--tap` writes TAP, and `--order <mode>` is `default`, `random` or a numeric seed (default `default`).
- `shards install --production` installs no development dependencies, installs only locked versions, and fails if `shard.yml` and `shard.lock` are out of sync. For an application, check in both `shard.yml` and `shard.lock`; for a library, only `shard.yml`. `shards check` exits 0 if dependencies are satisfied and 1 if not.
- Other checks for the same job: `crystal tool format` (synopsis `crystal tool format [--check] [<path>...]`), `crystal docs`; the install-crystal README itself uses `crystal tool format && git diff --exit-code` for the format check.
- Matrix over Crystal versions with the `crystal-lang/install-crystal@v1` action (`crystal: latest`, `nightly`, `1.11` and so on; `shards: true` is the default and uses the Shards bundled with Crystal) or the Docker image `crystallang/crystal`, whose tags are `x`, `x.y`, `x.y.z` (Ubuntu), the same with `-alpine`, and `nightly`; no ARM images are built.

Gotchas:
- `crystal spec` builds with the default optimisation level (`-O0`); `--release` is `-O3 --single-module`, so it is slower to compile.
- Use `crystal spec file:line` to run a single example, or `--tag`, `--example` and `--location` runner options to filter.

Verify: the CI job fails when a spec is broken on purpose.

## Checked

Checked 2026-11-08 against the `crystal` man page (spec runner options, optimisation levels, tool format), the `shards` man page (`--production`, check, lockfile advice), the install-crystal README and the crystallang/crystal Docker Hub page. Fixed: `--order` and `--junit_output` are runner options and belong after `--`. Removed: `crystal build --no-codegen`, the kcov coverage note, the compile-error test recipe and the cache-path advice, none of which the pages cover.

Method: docs-only read of cited pages, 2026-11-08
