---
id: computing-software.devops-ci-cd.gitlab-ci.cache-fallback-keys
name: cache-fallback-keys
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, fallback-keys, cache-fallback-key, branch-cache-fallback]
level: practitioner
status: docs-checked
description: "Give branch caches a warm start with cache:fallback_keys and CACHE_FALLBACK_KEY, so new branches reuse the default branch cache, and avoid the protected-suffix trap."
sources: ["https://docs.gitlab.com/ci/yaml/#cachefallback_keys", "https://docs.gitlab.com/ci/caching/#use-a-fallback-cache-key", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/caching/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache:fallback_keys

## 1. Per-branch cache with fallback
```yaml
build:
  cache:
    key: $CI_COMMIT_REF_SLUG
    fallback_keys:
      - $CI_DEFAULT_BRANCH
      - deps-default
    paths: [.gradle/caches/]
  script: ./gradlew build
```
Lookup order: `key` → each fallback in order → global `CACHE_FALLBACK_KEY` variable (if set).
Extraction stops at the first cache that is found.

## 2. Global fallback variable
```yaml
variables:
  CACHE_FALLBACK_KEY: main-deps
```
Applies to every cache in the pipeline that misses.

## 3. Protected suffix trap
By default protected and unprotected branches do not share caches: a suffix is added to the key
(`main-protected` for a protected branch; `feature-non_protected` for an unprotected branch when a Developer
runs the pipeline, `feature-protected` when a Maintainer or Owner starts it). Per-cache `fallback_keys` get the
same suffix, so an unprotected branch falling back to `main` looks for `main-non_protected` and finds nothing.
The global `CACHE_FALLBACK_KEY` is the exception: no suffix is added to it.
Fixes: set `cache:unprotect: true` on the jobs that should share (users without access to protected branches
can then read and write the keys protected branches use), or clear *Use separate caches for protected branches*
under Settings > CI/CD > General pipelines. The docs say to disable the separation only where every Developer is highly trusted.

## 4. Gotchas
- Up to 5 fallback keys per cache entry.
- `fallback_keys` takes an array of cache keys.
- After a manual cache clear (Pipelines > Clear runner caches) fallback keys get the index appended like other keys.
- A fallback hit restores files from another key: tools must handle a partially valid cache.

## Verify
- [ ] The first pipeline on a new branch restores a cache from a fallback key (the job log shows which key was used).
- [ ] The second pipeline on that branch hits its own key.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/caching/_index.md and doc/ci/yaml/_index.md: extraction order (`cache:key`, each `fallback_keys` entry, then global `CACHE_FALLBACK_KEY`), up to five fallback keys per cache, `-protected` and `-non_protected` suffixes (also applied to per-cache fallback keys, not to the global fallback key), `cache:unprotect` and its warning, and the settings path for the separation checkbox. Removed the unconfirmed claims about upload target, `cache:key:files` inside fallback keys, variable expansion in fallback keys, and the quoted log lines.

Method: documentation only; no commands were run.
