---
id: computing-software.software-engineering.git.refspecs-and-arbitrary-refs
name: refspecs-and-arbitrary-refs
category: computing-software
field: software-engineering
product: git
tags: [git, git-internals, refspec, git-refspec, fetch, push, refs, merge-request-refs, notes]
level: practitioner
status: verified
description: "Read and write refspecs to fetch and push arbitrary refs: MR heads, notes, tags, mirrors, deleting remote refs, and narrowing what a remote fetches."
sources:
  - https://git-scm.com/book/en/v2/Git-Internals-The-Refspec
  - https://git-scm.com/docs/git-fetch
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/git-ls-remote
  - https://git-scm.com/docs/git-for-each-ref
  - https://github.com/gitlabhq/gitlabhq/blob/master/doc/user/project/merge_requests/merge_request_troubleshooting.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Refspecs and fetching or pushing arbitrary refs

**Goal:** control exactly which refs move between repositories, beyond the default branch tracking.

## 1. Syntax
`[+]<src>:<dst>` - for fetch, src is on the remote and dst local; for push, the reverse. `+` allows non-fast-forward updates. Globs `*` must appear in both sides.
Default written by `git clone`:
```ini
[remote "origin"]
    url = git@github.com:org/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

## 2. Fetch recipes
```bash
git fetch origin 'refs/merge-requests/*/head:refs/remotes/origin/mr/*'   # GitLab merge request heads
git fetch origin main:refs/remotes/origin/main             # only main
git fetch origin 'refs/notes/*:refs/notes/*'                 # fetch the notes refs
git fetch origin '+refs/tags/*:refs/tags/*'                # force-update moved tags
```
Narrow a remote permanently (huge repos with many branches):
```bash
git config --replace-all remote.origin.fetch '+refs/heads/main:refs/remotes/origin/main'
git config --add remote.origin.fetch '+refs/heads/release/*:refs/remotes/origin/release/*'
```
Negative refspecs exclude: `git fetch origin 'refs/heads/*:refs/remotes/origin/*' '^refs/heads/dependabot/*'`.

## 3. Push recipes
```bash
git push origin HEAD:refs/heads/feature-x      # push current commit to a new remote branch
git push origin local-name:remote-name
git push origin :old-branch                     # delete (same as --delete old-branch)
git push origin 'refs/notes/*'
git push --mirror backup                        # all refs, deletes extras on the target
```
Default push config: `remote.origin.push = refs/heads/*:refs/heads/*` or `push.default=current|simple`.

## 4. Inspect refs
```bash
git ls-remote origin 'refs/heads/release/*'
git for-each-ref --format='%(refname) %(objectname:short)' refs/remotes/origin
git show-ref --tags
```

## Gotchas
- `git fetch origin main` writes `FETCH_HEAD`; with a configured remote-tracking refspec it also updates `origin/main` (see CONFIGURED REMOTE-TRACKING BRANCHES in git-fetch), but never your local `main`.
- `--mirror` push deletes remote refs that do not exist locally; use it only for true mirrors.
- Without `+`, fetching rewritten history fails with "(non-fast-forward)" for that ref.

## Verify
- `git ls-remote . 'refs/remotes/*'` shows exactly the refs your refspecs intend, and a test fetch of a single ref lands where expected.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the GitLab docs mirror. Confirmed: refspec syntax `[+]<src>:<dst>`, one `*` on each side of a pattern refspec, leading `+` to force, negative refspecs starting with `^` (git-fetch, git-push), empty source deletes the remote ref, `--mirror` push semantics, FETCH_HEAD and configured remote-tracking branches, `remote.<name>.fetch`/`push`; GitLab publishes merge request heads under `refs/merge-requests/<iid>/head`. Removed as unconfirmed: GitHub `pull/<n>/head` and `refs/pull/*` read-only remarks, the Gerrit `refs/for/` push, and the claim that notes are not fetched by default.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: the default `+refs/heads/*:refs/remotes/origin/*`; a fetch refspec that remaps into `refs/remotes/origin/mr/*`; `main:refs/remotes/origin/main`; a negative refspec `^refs/heads/feature`; fetching and pushing `refs/notes/*`; `+refs/tags/*:refs/tags/*`; `push origin HEAD:refs/heads/x`, `local:remote`, and `:old-branch` deletion; `ls-remote` with a glob; `for-each-ref` on remotes; `show-ref --tags`; `config --replace-all` then `--add` on `remote.origin.fetch`; `push --mirror` and `fetch` of a missing ref (`couldn't find remote ref`). Not run: GitLab `refs/merge-requests/*/head` (no GitLab server; docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
