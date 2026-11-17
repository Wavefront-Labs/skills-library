---
id: computing-software.devops-ci-cd.gitlab-ci.cache-policy-pull-push
name: cache-policy-pull-push
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, cache-policy, cache-pull-push, cache-pull-only, cache-warm-job]
level: practitioner
status: docs-checked
description: "Use cache:policy pull, push and pull-push so one job populates a cache and many parallel jobs only download it, cutting upload time and load on the cache server."
sources: ["https://docs.gitlab.com/ci/yaml/#cachepolicy", "https://docs.gitlab.com/ci/caching/examples/#use-a-variable-to-control-a-jobs-cache-policy", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache:policy

| policy | Download at start | Upload at end |
|---|---|---|
| `pull-push` (default) | yes | yes |
| `pull` | yes | no |
| `push` | no | yes |

## 1. Warm once, read many
```yaml
.deps-cache: &deps
  key: { files: [poetry.lock] }
  paths: [.cache/pypoetry]

install:
  stage: .pre
  cache: { <<: *deps, policy: pull-push }
  script: poetry install

test:
  parallel: 8
  cache: { <<: *deps, policy: pull }       # 8 jobs, zero uploads
  script: poetry run pytest
```
The docs recommend `pull` for many parallel jobs sharing a cache: it speeds up jobs and reduces load on the cache
server, and one `push` job builds the cache.

## 2. Policy from a variable
```yaml
variables:
  CACHE_POLICY: pull
build:
  cache:
    key: gradle
    paths: [.gradle/caches]
    policy: $CACHE_POLICY
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables: { CACHE_POLICY: push }       # nightly job rebuilds the cache from scratch
    - when: on_success
```
The `push` policy on a schedule rebuilds the cache from the job's own output each night.

## 3. Gotchas
- `pull` jobs never fix a stale or missing cache: something must push for each key (protected and unprotected keys carry different suffixes and are separate).
- The cache is saved only when the job succeeds unless `cache:when` says otherwise.
- `policy: push` jobs do not download: tools must work from an empty cache dir.
- `policy` accepts a CI/CD variable.

## Verify
- [ ] The parallel `test` jobs do not upload a cache.
- [ ] Only the install or scheduled job uploads one.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md: `pull`, `push`, `pull-push` (default) semantics, the recommendation to use `pull` for parallel jobs and a `push` job to build the cache, `cache:when` values with `on_success` default, and that `policy` accepts CI/CD variables. Removed the last-writer-wins claim, the minutes figure, the nightly clean-cache claim and quoted log lines, which no page states. The `rules:variables` pattern for a policy variable matches the example in doc/ci/caching/examples.md.

Method: documentation only; no commands were run.
