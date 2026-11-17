---
id: computing-software.software-engineering.pnpm.ci-store-caching
name: ci-store-caching
category: computing-software
field: software-engineering
product: pnpm
tags: [ci-cache, store-dir-ci, pnpm-cache-path, gitlab-ci, circleci, azure-pipelines, bitbucket-pipelines, jenkins]
level: practitioner
status: docs-checked
description: "Cache pnpm in CI safely: put store-dir inside the workspace, key the cache on pnpm-lock.yaml, cache the pnpm cache path metadata, and never share caches with untrusted jobs."
sources:
  - https://pnpm.io/continuous-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Caching the store is optional and may not speed installs up. Pattern used by the provider examples:

```sh
pnpm config set store-dir .pnpm-store   # point the store at the cached path
pnpm install
```

with the CI cache keyed on `pnpm-lock.yaml` (GitLab `cache.key.files`, CircleCI `checksum "pnpm-lock.yaml"`, Azure `Cache@2` key `pnpm | "$(Agent.OS)" | pnpm-lock.yaml`, Semaphore `cache store node-$(checksum pnpm-lock.yaml) $(pnpm store path)`).

Per provider details:
- Bitbucket: image `ghcr.io/pnpm/pnpm:12`, cache `pnpm: $BITBUCKET_CLONE_DIR/.pnpm-store`.
- CircleCI: append `export PATH="$PNPM_HOME/bin:$PATH"` to `$BASH_ENV`, which CircleCI sources before each step.
- Azure: `echo "##vso[task.prependpath]$PNPM_HOME/bin"`; use a Linux or macOS agent.
- Jenkins: each `sh` step is its own shell, so set `PATH` in the pipeline `environment` block.
- AppVeyor: `PNPM_HOME` plus the PowerShell installer; `Install-Product node` is no longer needed.

Metadata cache: `pnpm cache path` prints its directory. It also holds the lockfile verification log, which lets a job skip re-checking an unchanged lockfile against supply-chain policies (the main install cost once the store is warm).

Important: only cache store and cache directories in locations writable by trusted jobs; never let untrusted jobs write what trusted jobs restore.

## Checked

2026-11-04. Confirmed against pnpm.io/continuous-integration: store caching is optional, provider cache keys and paths (GitLab, CircleCI, Azure, Semaphore, Bitbucket), per-provider PATH handling, AppVeyor note, pnpm cache path and verification log, trusted-cache warning. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
