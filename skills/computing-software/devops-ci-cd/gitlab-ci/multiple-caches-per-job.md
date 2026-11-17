---
id: computing-software.devops-ci-cd.gitlab-ci.multiple-caches-per-job
name: multiple-caches-per-job
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, multiple-caches, cache-list, per-tool-caches]
level: practitioner
status: docs-checked
description: "Give one job several independent caches (up to four) with a cache list, each with its own key, paths and policy, e.g. language deps vs tool caches."
sources: ["https://docs.gitlab.com/ci/caching/#use-multiple-caches", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/caching/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple caches per job

One combined cache means any change (a new lockfile, a linter upgrade) invalidates everything.
Split by change rate.

## 1. Example
```yaml
test:
  cache:
    - key: { files: [Gemfile.lock] }
      paths: [vendor/ruby]
    - key: { files: [yarn.lock] }
      paths: [.yarn-cache/]
      policy: pull
    - key: lint-$CI_COMMIT_REF_SLUG
      fallback_keys: [lint-$CI_DEFAULT_BRANCH]
      paths: [.lint-cache/]
      when: always
  script:
    - echo "install dependencies and run checks here"
```

## 2. Rules
- Max **4** caches per job.
- Use distinct keys: caches with the same key but different paths overwrite each other.
- Each cache entry supports its own `key`, `paths`, `policy`, `when`, `untracked`, `fallback_keys`, `unprotect`.
- Job configuration and `default:cache` do not merge: a job's `cache` replaces the default entirely; reuse with YAML anchors.
- If multiple caches are combined with `CACHE_FALLBACK_KEY`, the global fallback cache is fetched every time a cache is not found.

## 3. Sizing
All caches defined for a job are archived in a single `cache.zip`, so splitting caches changes how often a key
is invalidated, not the number of archives. Group paths that change together.

## Verify
- [ ] Bumping one lockfile changes only that cache's key.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/caching/_index.md and doc/ci/yaml/_index.md: maximum of four caches per job, the global fallback behaviour with multiple caches, that job `cache` and `default:cache` do not merge, that all caches of a job are stored in one `cache.zip`, and that identical keys with different paths overwrite each other. Removed the separate-zip claim, `!reference` advice and the compression variables (runner docs, not checked here).

Method: documentation only; no commands were run.
