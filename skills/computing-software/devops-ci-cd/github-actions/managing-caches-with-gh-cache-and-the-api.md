---
id: computing-software.devops-ci-cd.github-actions.managing-caches-with-gh-cache-and-the-api
name: managing-caches-with-gh-cache-and-the-api
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, gh-cache, cache-cleanup, cache-api, cache-list, cache-delete, cache-usage, pr-closed-cache-cleanup, cache-size-limit, cache-eviction, actions-cache, branch-cache-scope, cache-key-prefix-delete, actions-cache-management, cache-storage-quota]
level: practitioner
status: docs-checked
description: "List, inspect and delete Actions caches with gh cache and the REST API: find what eats the 10 GB quota, purge caches of closed PRs automatically, and delete by key prefix or ref."
sources: ["https://cli.github.com/manual/gh_cache", "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manage-caches", "https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#usage-limits-and-eviction-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing caches with gh cache and the API

**Goal:** keep the repo under the cache quota so the caches you need are not evicted by
the ones you don't.

## 1. Inspect
```bash
gh cache list --limit 100 --sort size_in_bytes --order desc   # key, size, ref, created, last accessed
gh cache list --ref refs/pull/123/merge                   # a PR's caches
gh cache list --key npm- --json id,key,sizeInBytes,ref    # key prefix filter, JSON fields
```
`--sort` accepts `created_at`, `last_accessed_at` (default) or `size_in_bytes`; `--order` is `asc` or `desc`;
`--limit` defaults to 30. Available JSON fields: createdAt, id, key, lastAccessedAt, ref, sizeInBytes, version.
Usage can also be read through the REST API (see the cache REST reference).
Cache storage is limited per repository: the default is 10 GB (the maximum allowed repository setting is 25 GB;
usage beyond 10 GB is billed on GitHub.com plans), entries not accessed for over 7 days are removed, and when the
limit is reached caches are deleted in order of last access date, oldest first.

## 2. Delete
```bash
gh cache delete <id>                      # one entry by id
gh cache delete <key>                     # by key; add --ref to limit to one ref
gh cache delete --all                     # everything in the repo
gh cache delete --all --ref refs/pull/123/merge   # every cache for one ref
```
`gh cache delete --all` also takes `--succeed-on-no-caches` (exit 0 when nothing matches). Deleting from a workflow
needs `actions: write`; users with write access can also delete in the web UI.

## 3. Purge PR caches on close
```yaml
on:
  pull_request:
    types: [closed]
jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions: { actions: write }
    steps:
      - run: |
          gh cache delete --all --ref "refs/pull/${{ github.event.pull_request.number }}/merge" --succeed-on-no-caches
        env: { GH_TOKEN: "${{ github.token }}", GH_REPO: "${{ github.repository }}" }
```
Pull request caches are restricted to their branch; many of them can fill the quota and cause cache thrashing,
which is why GitHub documents a cleanup workflow on `pull_request` `closed` (using `gh cache list --ref` and
`gh cache delete`, with `GH_TOKEN` and `GH_REPO` set). For fork pull requests the docs mention `pull_request_target`, with its security
considerations.

## 4. Why caches "disappear"
- Scope: caches are restricted by branch, and the default branch cache is available to other branches, so a
  cache written on one feature branch is not visible to another. Warm the default branch so pull requests
  can restore from it.
- Eviction: entries unused for over 7 days are removed, and the oldest-accessed entries go first when the
  repository limit is reached.
- Keys should change with content (for example with `hashFiles`).

## Verify
- [ ] Cache usage is under the repository limit after cleanup.
- [ ] Closed-PR cleanup job deletes entries (log shows ids).
- [ ] Default-branch caches exist for every key prefix pull requests restore from.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and cli/cli source (gh v2.103.2).
- gh cache list flags (--limit default 30, --key prefix filter, --ref, --sort created_at|last_accessed_at|size_in_bytes, --order asc|desc, --json fields): confirmed in cli/cli pkg/cmd/cache/list and shared source (gh v2.103.2 at review). The earlier `--sort size` was wrong.
- gh cache delete forms (id, key, --all, --ref, --succeed-on-no-caches): confirmed in cli/cli pkg/cmd/cache/delete source.
- Cache limits (10 GB default, 25 GB maximum setting, 7-day removal, eviction by last access) and the closed-PR cleanup workflow: confirmed in the dependency-caching reference, cache reusables and manage-caches page.
- Removed unconfirmed REST DELETE query forms, the usage endpoints, the gh minimum-version claim, and the runner-reinstall and mid-run deletion remarks.

Method: documentation only; no commands were run.
