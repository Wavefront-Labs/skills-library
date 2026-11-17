---
id: computing-software.software-engineering.git.large-repo-performance
name: large-repo-performance
category: computing-software
field: software-engineering
product: git
tags: [git, monorepo, sparse-checkout, partial-clone, git-lfs, commit-graph, performance, shallow-clone, maintenance, fsmonitor, scalar, large-repository]
level: advanced
status: docs-checked
description: "Keep git fast on a huge monorepo: sparse-checkout to avoid materializing the whole tree, partial clone, LFS for binaries, and commit-graph for log/blame speed."
sources:
  - https://git-scm.com/docs/git-sparse-checkout
  - https://git-scm.com/docs/git-clone
  - https://git-scm.com/docs/git-rev-list
  - https://git-scm.com/docs/git-commit-graph
  - https://git-scm.com/docs/git-maintenance
  - https://git-scm.com/docs/git-fsmonitor--daemon
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/scalar
  - https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-migrate.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Large repo performance — why `git status` takes 8 seconds and how to fix it

**Goal:** keep everyday git commands fast (status, checkout, log) in a repo with
hundreds of thousands of files or years of history, without splitting it into many
repos.

## 1. Sparse-checkout: don't materialize files you don't touch
```
git sparse-checkout init --cone
git sparse-checkout set services/billing libs/shared
```
Cone mode (the default) takes a list of directories and checks out only those (plus
files at the top level), so the working tree stays small. It suits "I only work in one
corner of a huge monorepo." The manual does not recommend non-cone mode
(gitignore-style patterns) because of its documented shortcomings; use it only if you
need individual file patterns.

## 2. Partial clone: don't download history/blobs you don't need
```
git clone --filter=blob:none <url>       # fetch trees/commits, blobs on demand
git clone --filter=tree:0 <url>          # omit all trees and blobs until needed
```
A normal clone downloads every blob in every commit of history. `--filter=blob:none`
fetches file *contents* lazily as you check them out or diff them — a CI runner that
only needs the current tree, or a dev who only works in one subdirectory via
sparse-checkout, saves most of the clone time and disk. Combine with
`--depth=1`/shallow for CI that never needs history (a shallow clone has its history
truncated to the given number of commits, so history-based commands only see that much);
don't shallow-clone a dev's working repo.

## 3. commit-graph: speeds up log/blame/merge-base
```
git commit-graph write --reachable --changed-paths
```
The commit-graph file caches commit-graph structure so history walks avoid parsing raw
commit objects; `core.commitGraph` defaults to true, so Git reads it when present.
`--changed-paths` also stores which paths changed between a commit and its first parent,
which the manual says gives significant gains for `git log -- <path>` (writing it can
take a while on large repositories). `git maintenance start` registers the repository and
schedules `git maintenance run --scheduled` hourly through the OS scheduler; prefer it
over a hand-rolled cron of `git gc`.

## 4. Git LFS for binaries, used correctly
Large binaries (assets, datasets, compiled artifacts) committed directly bloat every
clone forever — history keeps every version. Git LFS replaces them with pointer
files, storing actual content in a separate LFS store fetched on demand:
```
git lfs track "*.psd" "*.bin"
git add .gitattributes
```
Gotcha: files added as regular blobs *before* `.gitattributes` tracked them stay
regular blobs in history — LFS migration for existing bloat needs `git lfs migrate
import` (which rewrites history, so it's a coordinated, disruptive operation, not a
casual one).

## 5. FSMonitor for faster status on huge working trees
```
git config core.fsmonitor true
```
`core.fsmonitor true` enables Git's built-in file system monitor daemon
(`git fsmonitor--daemon`), which uses platform filesystem notifications (inotify on
Linux) so `status` need not scan the whole working tree. `core.fsmonitor` can also name
an fsmonitor hook program (for example a Watchman integration). Older Git versions
(2.35.1 and earlier) do not understand the boolean form.

## 6. When these aren't enough
If these per-repo settings are not enough, `scalar` (shipped with Git) wraps them: `scalar clone` enables sparse-checkout (unless `--full-clone`), registers the
repository for background maintenance and applies recommended config. Adopting it is a
larger operational decision than a per-repo config change; evaluate before rolling it out.

## Gotchas
- With a partial clone, objects outside what you have checked out are fetched from the
  remote on demand, so a build script that reads files outside the sparse set triggers
  fetches (or fails offline).
- `git gc --aggressive` trades much more run time for more thorough optimisation; for
  routine upkeep use `git maintenance` tasks instead.
- Partial-clone filters are not applied to submodules unless asked: `git clone`
  has `--also-filter-submodules`.

## Verify
- [ ] `git sparse-checkout list` shows only the directories actually needed for this
      checkout, confirmed by `du -sh .git` and the working tree before/after.
- [ ] Clone time/disk for a fresh CI runner was measured before and after adding
      `--filter=blob:none` (and shallow depth, if history isn't needed).
- [ ] `git config core.fsmonitor` is on and `git maintenance start` has been run for
      anyone reporting slow `status`/`log`.
- [ ] Any binary type added going forward is tracked by `.gitattributes` for LFS
      before the first commit, not after bloat accumulates.

Related: computing-software.software-engineering.git.rebase-and-history-repair

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the git-lfs manual pages on GitHub. Confirmed: cone mode is the default and non-cone is not recommended (git-sparse-checkout); `--filter=blob:none` and `tree:<depth>` semantics (git-clone, git-rev-list); `git commit-graph write --reachable --changed-paths`, `core.commitGraph` default true; `git maintenance start` hourly schedule; `core.fsmonitor` boolean = built-in daemon, hook-path form, inotify on Linux; `git lfs migrate import` rewrites history; `git lfs track` writes `.gitattributes`; `scalar clone` enables sparse-checkout (unless --full-clone) and background maintenance. Removed as unconfirmed: bloom-filter O(1) wording, the `core.commitGraph true` setting advice, per-claim speed statements, and the version number for the fsmonitor daemon.

Method: documentation only; no commands were run.
