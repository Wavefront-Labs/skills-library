---
id: computing-software.devops-ci-cd.ci-pipeline-design.build-caching-strategies
name: build-caching-strategies
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, ci-cache, build-cache, cache-key, restore-keys, cache-eviction, cache-scope, cache-poisoning, actions-cache, gitlab-cache, cache-vs-artifacts, docker-layer-cache, buildx, github-actions, gitlab-ci]
level: practitioner
status: docs-checked
description: "Design CI caches that actually save time: key and fallback design, scope and poisoning, cache vs artifacts, Docker layer caches, and measuring hit rate vs restore cost."
sources: ["https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows", "https://docs.gitlab.com/ee/ci/caching/", "https://docs.docker.com/build/cache/backends/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI build caching strategies

**Goal:** caches that cut wall-clock time measurably, never make a build wrong, and can't
be poisoned by an untrusted branch.

(Making the build itself cacheable — declared inputs, remote task caches — is
`computing-software.devops-ci-cd.build-systems.fast-reproducible-cacheable-builds`. This
skill is about the CI platform's cache layer.)

## 1. Decide what is worth caching
Cache things that are **expensive to produce and cheap to restore**: package-manager
download caches and dependency directories are the usual candidates. Test results and
coverage reports are not caches; they are **artifacts**.

**Cache vs artifact:** a cache is an optimisation that may be missing at any time;
an artifact is an output a later job *depends on*. GitLab's docs say the same: use
artifacts to pass intermediate build results between stages. If a path is both cached and
an artifact, the cache can be overwritten because caches are restored before artifacts.

## 2. Key design (GitHub Actions)
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-build-cache-node-modules-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-build-cache-node-modules-
      ${{ runner.os }}-build-
```
- On an exact `key` match the action reports a hit (`cache-hit` output); on a miss it
  creates a new cache at the end of a successful job. An existing cache cannot be changed:
  create a new one under a new key. Keys are at most 512 characters.
- Put a hash of the lockfile in the key so a dependency change creates a new cache; the
  docs also use `runner.os`.
- `restore-keys` are tried in order, most specific first, as prefix matches; if several
  caches match one prefix the most recently created is restored. They give a *partial*
  hit, so the restored cache may not match the current lockfile; only use them when the
  tool tolerates stale content.
- The search order is the current branch first, then the default branch.
- For common package managers the `setup-*` actions (setup-node for npm/Yarn/pnpm,
  setup-python for pip/pipenv/Poetry, setup-java for Gradle/Maven, setup-ruby, setup-go,
  setup-dotnet) create and restore dependency caches with minimal configuration.
- GitLab: `cache:key`, `cache:key:files` and `cache:fallback_keys` (up to five fallback
  keys per cache entry) are the equivalents. To start from a fresh cache, change
  `cache:key` or clear the cache manually.

## 3. Scope, limits and poisoning
- GitHub Actions: runs restore caches from the current branch or the default branch; a
  pull request run can also restore from its base branch. Caches cannot be restored from
  child or sibling branches or from other tag names. A cache created by a `pull_request`
  run is scoped to the merge ref and cannot be restored by the base branch or by other pull
  requests.
- Default limits: entries not accessed for over 7 days are removed; the total is capped at
  10 GB per repository by default (adjustable, extra usage is billed); when full, caches
  are evicted oldest-last-access first. The docs warn this can cause cache thrashing.
- Cache contents are not signed or verified, and anyone who can open a pull request can
  read caches on the base branch. Never store tokens or credentials in a cached path.
- Low-trust triggers (for example `pull_request_target`, `issue_comment`, `workflow_run`)
  get read-only access to the default branch's caches by default; only triggers such as
  `push` and `schedule` can write there. Use `actions/cache/restore` in low-trust workflows
  and let a trusted `push` workflow keep the cache updated. The `cache-mode` workflow/job
  key (`read`, `write`, `write-only`, `none`) grants the least access a job needs.
  Declaring a write-capable mode on a low-trust trigger reintroduces poisoning risk.
- GitLab: the cache is stored where GitLab Runner is installed and uploaded to S3 if a
  distributed cache is enabled. Autoscaled runners without a distributed cache, or several
  standalone runners without a shared cache, cause misses. Set the `cache:policy` to `pull`
  on jobs that only read and `pull-push` where the cache is built. By
  default protected and non-protected branches do not share a cache (keys get a
  `-protected` or `-non_protected` suffix); keep it that way.

## 4. Docker layer cache in CI
Use BuildKit cache backends. The default `docker` driver supports `inline`, `local`,
`registry` and `gha` only with the containerd image store enabled; other backends need a
different driver. `gha` uploads to the GitHub Actions cache (listed as beta in the docs).
```
docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:main .
```
The second `--cache-from` is the docs' pattern for scoped per-branch caches that fall back
to main. `mode=min` (the default) caches only layers exported into the final image;
`mode=max` caches all layers, so it is bigger but more likely to hit, which suits
multi-stage builds. Compression (for example `compression=zstd`) is supported by the
`local` and `registry` backends.

## 5. Measure, don't assume
Record for each cache: hit or miss, restore time, size and save time. A large cache that
takes longer to restore than the downloads it saves is a net loss. Saving also costs time
on every miss.

## Verify
- [ ] Each cache has a recorded hit rate and restore time; every one is a net win.
- [ ] Deleting all caches gives a slower but **identical-result** build.
- [ ] Untrusted (PR/fork/low-trust) jobs cannot write caches consumed by main or release jobs.
- [ ] Nothing a later job requires is passed via cache instead of an artifact.
- [ ] Keys include the lockfile hash (and OS where it matters); a runtime upgrade causes a clean miss.

## Checked
Confirmed 2026-11-09 against the three cited pages, read in full: GitHub Actions dependency caching reference (key matching, restore-keys order, branch scope, merge-ref scoping, 7-day and 10 GB limits, eviction, low-trust triggers, cache-mode, setup-* actions, security notes), GitLab caching docs (cache vs artifacts, distributed cache, protected branch separation, fallback_keys up to five, policy pull and pull-push, restore before artifacts), Docker cache backends (supported backends, registry branch example, mode min/max, compression).
Removed: the cache-type table (ccache, sccache, Gradle, Bazel, node_modules, "typical win" ratings), `scope=` on the gha backend, `docker save` advice, the `cache: npm` input name, the "warm persistent runners" section, the "historically" limits wording, and the sample pip key.
Method: docs-checked 2026-11-09 against docs.github.com caching reference, docs.gitlab.com/ee/ci/caching and docs.docker.com/build/cache/backends
