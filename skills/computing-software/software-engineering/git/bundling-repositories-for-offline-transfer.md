---
id: computing-software.software-engineering.git.bundling-repositories-for-offline-transfer
name: bundling-repositories-for-offline-transfer
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, git-bundle, offline-transfer, air-gapped, backup, incremental-bundle]
level: practitioner
status: verified
description: "Move repositories or incremental history across air-gapped networks with git bundle: create, verify, fetch from, and chain incremental bundles."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Bundling
  - https://git-scm.com/docs/git-bundle
  - https://git-scm.com/docs/bundle-uri
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundling repositories for offline transfer

**Goal:** transfer Git history as a single file (USB, email, artifact store) when there is no network path between machines.

## 1. Full bundle
```bash
git bundle create repo.bundle --all          # all refs
git bundle create main.bundle main v1.0.0    # only some refs
git bundle verify repo.bundle                # checks prerequisites against the current repo
```
A bundle is a packfile plus a header listing refs and prerequisite commits.

## 2. Use it like a remote
```bash
git clone repo.bundle project                 # bundle acts as the origin URL
git -C project remote set-url origin https://git.example.com/org/project.git   # repoint later
git fetch ../repo.bundle 'refs/heads/*:refs/remotes/bundle/*'
git bundle list-heads repo.bundle
```

## 3. Incremental bundles
On the sending side, bundle only what the receiver lacks:
```bash
git bundle create update-0612.bundle v1.0.0..main         # receiver must already have v1.0.0
git bundle create update.bundle --since=10.days main
# track last transfer with a tag
git bundle create delta.bundle lastsent..main && git tag -f lastsent main
```
On the receiving side `git bundle verify update.bundle` lists "The bundle requires this ref" ("these N refs" when several) and ends "is okay"; if the prerequisite commit is missing it prints "Repository lacks these prerequisite commits" and fails.

## 4. Backup use
`git bundle create backup-$(date +%F).bundle --all` produces one file that is easy to checksum and store; restore with `git clone`.

## Gotchas
- A range like `main~10..main` must reference commits the receiver has; otherwise verify fails. Prefer tags agreed by both sides.
- Bundles do not carry config, hooks, reflogs, stashes (unless `refs/stash` included) or LFS objects; transfer LFS files separately (`git lfs fetch --all` then copy `.git/lfs/objects`).
- Bundles are not encrypted or signed; checksum them, and encrypt for untrusted transport.
- A bundle made as `create x.bundle main v1.0.0` has no `HEAD` entry, so `git clone x.bundle` warns "remote HEAD refers to nonexistent ref, unable to checkout" and leaves no branch checked out; use `--all`, or add `HEAD` to the ref list.

## Verify
- `git bundle verify` reports "is okay" on the receiving repo, and after fetch `git rev-parse main` matches the sender's.
