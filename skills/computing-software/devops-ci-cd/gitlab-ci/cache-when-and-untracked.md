---
id: computing-software.devops-ci-cd.gitlab-ci.cache-when-and-untracked
name: cache-when-and-untracked
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, cache-when, cache-untracked, cache-on-failure, cache-always]
level: intro
status: docs-checked
description: "Control cache upload timing with cache:when (on_success, on_failure, always) and capture git-untracked files with cache:untracked, and when each is a mistake."
sources: ["https://docs.gitlab.com/ci/yaml/#cachewhen", "https://docs.gitlab.com/ci/yaml/#cacheuntracked", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache:when and cache:untracked

## 1. cache:when
```yaml
test:
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths: [.pytest_cache/, .cache/pip]
    when: always            # on_success (default) | on_failure | always
```
- `on_success` (default): save the cache only when the job succeeds.
- `on_failure`: save the cache only when the job fails.
- `always`: save the cache whether the job fails or succeeds; useful for package download caches, so the run after a red pipeline is still fast.
- Keep the default for build-output caches, so a failed job cannot leave a half-built state in the cache.

## 2. cache:untracked
```yaml
build:
  cache:
    untracked: true          # every file git does not track, ignored files included
    paths: [vendor/]
```
`untracked: true` caches all files untracked in the Git repository: files ignored by `.gitignore` and files
created but not added with `git add`. This can create unexpectedly large caches when the job downloads
dependencies (gems, node modules) or extracts artifacts from another job, because both are untracked.
It can be combined with `cache:paths`. Prefer explicit `paths:`; use `untracked` only for tools that scatter outputs unpredictably.

## 3. Same keys exist for artifacts
`artifacts:when` and `artifacts:untracked` exist as well; check the `artifacts` section of the keyword reference for their exact values.

## Verify
- [ ] After a failing pipeline, the next run restores the cache (with `when: always`).
- [ ] The uploaded cache archive size is what you expect.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md: `cache:when` values and default, `cache:untracked` definition, the large-cache warning, combination with `cache:paths`, and that `cache:paths` includes ignored files. Removed the 50 MB to 2 GB figure, the secrets remark and quoted log text, which no page states.

Method: documentation only; no commands were run.
