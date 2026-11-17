---
id: computing-software.devops-ci-cd.gitlab-ci.cache-keys-from-lockfiles-and-prefixes
name: cache-keys-from-lockfiles-and-prefixes
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, cache-key-files, cache-key-prefix, lockfile-cache-key, protected-branch-caches, clear-runner-caches]
level: practitioner
status: docs-checked
description: "Key GitLab caches on lockfiles with cache:key:files and prefix so dependencies are reused until the lockfile changes, plus protected-branch cache separation and cache clearing."
sources: ["https://docs.gitlab.com/ci/yaml/#cachekeyfiles", "https://docs.gitlab.com/ci/caching/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache:key:files and prefix

## 1. Lockfile-keyed cache
```yaml
.node-cache: &node-cache
  key:
    files: [package-lock.json]        # up to 2 files (10 with the increase_ci_cache_key_files_limit flag, GitLab 19.5)
    prefix: $CI_JOB_NAME              # optional; the key looks like rspec-<sha>
  paths: [vendor/ruby]

test:
  cache: *node-cache
  script: echo "install dependencies and run tests here"
```
`cache:key:files` computes the key as a SHA of the **content** of the listed files, so every branch with the
same lockfile content shares one cache and a dependency bump creates a new one. Files that do not exist are
ignored; if none exist the key falls back to `default` (the prefix is added to it, for example `rspec-default`).
To key on the latest commit that touched the files instead, use `cache:key:files_commits` (up to two files; it
cannot be combined with `cache:key:files` in the same cache).

## 2. Cache only what is reusable
- Cache dependency directories under the project (for example `vendor/ruby`), listed in `cache:paths`.
- Paths must be inside the local working copy (relative to `$CI_PROJECT_DIR`); configure tools to write inside it.

## 3. Protected vs unprotected branches
By default a suffix is added to every cache key: `-protected` for protected branches and tags (and for pipelines
started by a Maintainer or Owner), `-non_protected` otherwise. Consequence: unprotected branches do not reuse
main's cache. Options: accept it (the safer default), or set `cache:unprotect: true` on a job, or clear
*Use separate caches for protected branches* in Settings > CI/CD > General pipelines (the docs say to do that only
where all Developers are highly trusted).

## 4. Clearing
Build > Pipelines > **Clear runner caches** (Developer role or higher) updates the internal cache name
(`cache-<index>`, index incremented by one); the old cache is not deleted and can be removed from runner storage manually.
Changing `cache:key` also starts a fresh cache. Pin dependency versions: after a clear, the next pipeline,
including on a protected branch, fetches dependencies again.

## Gotchas
- Multiple standalone runners (or autoscale runners) without a distributed cache each have their own local cache, so hits look random; the docs recommend one runner or a distributed cache.
- Cache is best-effort; never rely on it for correctness (use artifacts to pass build outputs).

## Verify
- [ ] The second pipeline's job log reports a cache hit for the key.
- [ ] Changing the lockfile produces a new key.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md: `cache:key:files` is a SHA of file content (not the last commit), missing files are ignored, `default` fallback and the `<prefix>-default` form, the file-count limit history (10 files in 19.5 behind the `increase_ci_cache_key_files_limit` flag, disabled by default), `cache:key:files_commits` (up to two files, not combinable with `files`), `cache:unprotect`; and in doc/ci/caching/_index.md: suffix rules, the Clear runner caches behaviour and the cache-mismatch causes. Removed the unconfirmed `Shared = true`, cleanup tooling and log-line claims. The earlier statement that the key comes from the most recent commit was wrong for `cache:key:files`.

Method: documentation only; no commands were run.
