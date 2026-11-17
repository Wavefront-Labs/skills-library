---
id: computing-software.software-engineering.git.removing-sensitive-data-from-history
name: removing-sensitive-data-from-history
category: computing-software
field: software-engineering
product: git
tags: [git, git-internals, git-filter-repo, remove-secrets-from-history, leaked-credentials, bfg, history-rewrite, secret-rotation, purge-file]
level: advanced
status: docs-checked
description: "Respond to a secret or large file committed to Git: rotate first, purge with git filter-repo, force-push, clean forks/caches and stop recurrence."
sources:
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
  - https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt
  - https://github.com/newren/git-filter-repo/blob/main/INSTALL.md
  - https://git-scm.com/docs/git-filter-branch
  - https://github.com/rtyley/bfg-repo-cleaner/blob/main/README.md
  - https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing sensitive data from history

**Goal:** neutralise a leaked secret and remove it (or a huge file) from every commit,
knowing that rewriting history is the second step, not the first.

## 1. Rotate first
Once pushed to any remote, assume the secret is compromised (other clones, CI caches and
backups may hold it). Revoke and reissue the key, check access logs. Rewriting history
without rotating fixes nothing.

## 2. Rewrite with git filter-repo
Git's own manual says `git filter-branch` is not recommended and points to alternatives.
Install `git-filter-repo` (its INSTALL.md covers package managers, and pipx:
`pipx install git-filter-repo`). Work in a FRESH clone (`--mirror` is allowed):
```bash
git clone --mirror git@host:org/repo.git && cd repo.git
git filter-repo --sensitive-data-removal --invert-paths --path config/prod.env    # drop a file everywhere
git filter-repo --sensitive-data-removal --replace-text ../replacements.txt       # redact strings
git filter-repo --strip-blobs-bigger-than 50M                                     # purge big blobs
```
`replacements.txt` lines look like `AKIA...XYZ==>REDACTED` or `regex:password=\S+==>password=REDACTED`.
`--sensitive-data-removal` (`--sdr`, needs git-filter-repo 2.47 or later) also fetches all
refs (which can discard unpushed local-only changes, hence the fresh clone), reports the
first changed commit(s) and tells you about orphaned LFS objects. filter-repo removes the
`origin` remote to stop accidental pushes; re-add it. It also removes signatures on
commits and tags it rewrites, so expect signed history to lose its signatures.

## 3. Force-push and clean up downstream
```bash
git push --force --mirror origin
```
- Branch protection may need temporary relaxing; tags are rewritten too.
- Pull request refs on GitHub (`refs/pull/*`) can keep the old commits reachable:
  contact GitHub Support to purge cached views and references in pull requests, as the
  GitHub docs describe (Support only assists where rotating the credential cannot
  mitigate the risk).
- Every collaborator must re-clone (or hard-reset every branch); a single old clone
  pushing back reintroduces the data.
- Forks keep the old history; they must be deleted or cleaned.

## 4. Prevent recurrence
- Pre-commit secret scanning and server-side push protection on your Git host (see your
  host's documentation for what it offers).
- Ignore env files (`.env*`), commit `.env.example`.

## BFG alternative
BFG Repo-Cleaner is an alternative; its README shows `bfg --strip-blobs-bigger-than 1M
--replace-text banned.txt repo.git`. Read its usage documentation before relying on it.

## Verify
- [ ] `git log --all -S '<secret fragment>'` in a fresh clone returns nothing.
- [ ] The secret is revoked (old key fails authentication).
- [ ] Secret scanning hook blocks a test commit containing a fake key.

## Checked

Checked 2026-10-25 against the git-filter-repo manual (repository last updated 2026-07-09), the GitHub docs page on removing sensitive data (github/docs main), the git-filter-branch manual and the BFG README. Confirmed: `--sensitive-data-removal` / `--sdr` behaviour (fetches all refs, reports first changed commits and LFS orphaning) and the 2.47 minimum version; `--invert-paths --path`, `--replace-text` with `==>` and `regex:` / `literal:` / `glob:` prefixes, `--strip-blobs-bigger-than` with K/M/G suffixes; origin removal; signature removal on rewritten commits; `git push --force --mirror origin`; GitHub Support purge of cached pull request views and fork behaviour; filter-branch is not recommended; BFG `--strip-blobs-bigger-than` and `--replace-text`. Removed as unconfirmed: the claim that bots scan pushes in seconds, `pip install` as the install route, BFG `--delete-files` and its HEAD protection, named scanner tools and the claim that `refs/pull/*` are read-only.

Method: documentation only; no commands were run.
