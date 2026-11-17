---
id: computing-software.devops-ci-cd.github-actions.matrix-builds-and-dependency-caching
name: matrix-builds-and-dependency-caching
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, matrix, matrix-build, strategy-matrix, include, exclude, fail-fast, max-parallel, dynamic-matrix, fromjson, test-sharding, sharding, actions-cache, cache-restore, cache-save, restore-keys, hashfiles, setup-node-cache, setup-python-cache, cache-eviction, cache-scope, docker-layer-cache, buildx-gha-cache, ci-speed]
level: practitioner
status: verified
description: "Design GitHub Actions matrices (include/exclude, dynamic fromJSON, sharding) and caches that hit: key design, restore/save split, scope rules, eviction and Docker layer cache."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows", "https://github.com/actions/cache"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matrix builds and dependency caching

**Goal:** cover the versions/platforms you actually ship to, in parallel, with caches
that hit on >90% of runs — without a matrix explosion that eats your minutes.

## 1. Matrix shape
```yaml
strategy:
  fail-fast: false          # see every failing cell, not just the first
  max-parallel: 6           # protect shared resources / concurrency quota
  matrix:
    os: [ubuntu-latest, windows-latest]
    python: ["3.10", "3.12", "3.13"]
    exclude:
      - os: windows-latest
        python: "3.10"
    include:
      - os: ubuntu-latest      # adds a key to an existing cell
        python: "3.12"
        coverage: true
      - os: macos-14           # adds a whole new cell
        python: "3.12"
```
- `include` entries that match an existing cell **extend** it; ones that match nothing **add** a cell.
  The precedence rules are subtle — read the generated job list in the run summary.
- Quote versions: `3.10` unquoted is the float `3.1`.
- Matrix size cap is 256 jobs per workflow run.
- Tests only on the full matrix for `main`/release; PRs run a reduced matrix:
  `python: ${{ github.event_name == 'pull_request' && fromJSON('["3.12"]') || fromJSON('["3.10","3.12","3.13"]') }}`.
- Required status checks name each cell (`test (ubuntu-latest, 3.12)`). Renaming a
  matrix value silently orphans a required check — add a single aggregating job
  (`needs: test`, `if: always()`, fail if `needs.test.result != 'success'`) and require only that.

## 2. Dynamic matrix (changed packages, shards)
```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      pkgs: ${{ steps.p.outputs.pkgs }}
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - id: p
        run: echo "pkgs=$(./scripts/changed-packages.sh | jq -Rcs 'split("\n")|map(select(.!=""))')" >> "$GITHUB_OUTPUT"
  test:
    needs: plan
    if: needs.plan.outputs.pkgs != '[]'     # skip the job when nothing changed
    strategy:
      matrix:
        pkg: ${{ fromJSON(needs.plan.outputs.pkgs) }}
```
Sharding tests: `matrix:` with `shard: [1, 2, 3, 4]`, and pass `--shard=${{ matrix.shard }}/4`
(Jest/Playwright) or `pytest-split --group ${{ matrix.shard }} --splits 4`.

## 3. Cache keys that hit
- Built-in first: `setup-node` `cache: npm|pnpm|yarn`, `setup-python` `cache: pip|poetry`,
  `setup-java` `cache: gradle|maven|sbt`, `setup-go` (`cache` defaults to true). They key on a hash of the
  dependency file (setup-go v6 hashes `go.mod` by default; set `cache-dependency-path: go.sum` to use `go.sum`).
  `setup-node` caches automatically only for npm when `package.json` has `packageManager`/`devEngines.packageManager`
  set to npm; pnpm and yarn need `cache:` set explicitly; `setup-python` accepts `pip`, `pipenv`, `poetry` and is off unless `cache:` is set.
- Manual: key = `os + tool + toolchain version + hash(lockfile)`; restore-keys = the same minus the hash.
```yaml
- uses: actions/cache@v6
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
      target
    key: ${{ runner.os }}-cargo-${{ matrix.rust }}-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: ${{ runner.os }}-cargo-${{ matrix.rust }}-
```
- Include the matrix value in the key, or cells overwrite/poison each other.
- Cache the **download cache** (`~/.npm`, pip cache), not `node_modules`, unless you
  understand native-module/OS coupling.

## 4. Restore/save split
`actions/cache/restore` + `actions/cache/save` let you save only on `main` and only on success:
```yaml
- uses: actions/cache/restore@v6
  id: c
  with:
    path: ~/.cache/tool
    key: tool-${{ hashFiles('tool.lock') }}
# ... build ...
- if: github.ref == 'refs/heads/main' && steps.c.outputs.cache-hit != 'true'
  uses: actions/cache/save@v6
  with:
    path: ~/.cache/tool
    key: ${{ steps.c.outputs.cache-primary-key }}
```
This stops every PR from writing its own entries and evicting the useful `main` ones.

## 5. Scope and eviction (why caches "don't work")
- A run can restore caches from its own branch, its PR base branch and the default branch. It cannot
  restore caches from child or sibling branches. A cache created by a `pull_request` run belongs to the merge ref
  (`refs/pull/.../merge`) and is only restorable by re-runs of that PR, so warm `main` with a `push` workflow.
- Entries are immutable per key; a miss-then-save creates a new key, a hit never updates.
- Repo cache quota: 10 GB by default (owners/admins can raise it; usage beyond 10 GB is billed on GitHub.com);
  entries not accessed for over 7 days are removed, and when the quota is exceeded the eviction policy removes entries
  to make room. Inspect with
  `gh cache list` / *Actions › Caches*, purge with `gh cache delete`.
- Docker: `docker/build-push-action` with `cache-from: type=gha` / `cache-to: type=gha,mode=max`
  uses the same quota (Docker docs); `mode=max` exports all layers (default `min`), so it stores more. Set a `scope=` per image (default scope is `buildkit`).

## Uncertainty
Quota and eviction figures come from the GitHub docs page on dependency caching and the 256-job cap from the
workflow syntax reference (both read 2026-10-20); plans can differ, so check your repository's Actions settings.
The workflow snippets pass actionlint, but no run on GitHub-hosted runners was made (cache hits and eviction are untested).

## Verify
- [ ] Run summary lists exactly the intended cells (no accidental cross-product).
- [ ] Branch protection requires one aggregate check, not per-cell names.
- [ ] Second run shows `Cache restored from key:` with an exact hit; the key includes OS + matrix value + lockfile hash.
- [ ] PRs restore from `main` caches; only `main` saves (restore/save split) if quota is tight.
- [ ] `gh cache list` shows total usage below quota with no thrash of near-identical keys.
