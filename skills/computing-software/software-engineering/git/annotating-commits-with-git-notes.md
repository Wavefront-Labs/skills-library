---
id: computing-software.software-engineering.git.annotating-commits-with-git-notes
name: annotating-commits-with-git-notes
category: computing-software
field: software-engineering
product: git
tags: [git, git-notes, commit-metadata, refs-notes, review-metadata, ci-annotations]
level: advanced
status: verified
description: "Attach metadata to commits without rewriting them using git notes: namespaces, pushing refs/notes, merging notes and keeping them across rebases."
sources: ["https://git-scm.com/docs/git-notes", "https://git-scm.com/docs/git-config#Documentation/git-config.txt-notesrewriteRef", "https://git-scm.com/book/en/v2/Git-Internals-Git-References"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotating commits with git notes

**Goal:** add information to existing commits (review results, CI status, benchmark
numbers, "Reviewed-by" after the fact) without changing their hashes.

## Basics
```bash
git notes add -m "Benchmarked: p99 41ms -> 37ms" a1b2c3d
git notes append -m "Deployed to prod 2026-10-18" a1b2c3d
git notes show a1b2c3d
git notes edit a1b2c3d
git notes remove a1b2c3d
git log --notes            # notes shown under the message (default ref only)
```
Notes are stored as a commit history under `refs/notes/commits`, mapping commit id to a
blob. They never alter the annotated commit.

## Namespaces
```bash
git notes --ref=ci add -m "build #812 green" HEAD      # refs/notes/ci
git log --notes=ci --notes=review
git config --add notes.displayRef "refs/notes/*"       # show all namespaces in log
```
Keep machine-written data (CI, perf) in its own ref so humans and bots do not conflict.

## Sharing (not automatic)
Notes are not pushed or fetched by default.
```bash
git push origin 'refs/notes/*'
git fetch origin 'refs/notes/*:refs/notes/*'
# permanent: git config --add remote.origin.fetch '+refs/notes/*:refs/notes/*'
```
Concurrent writers cause non-fast-forward rejections: fetch into a temp ref and
`git notes --ref=ci merge -s cat_sort_uniq refs/notes/remote-ci` (strategies:
manual (the default), ours, theirs, union, cat_sort_uniq).

## Surviving rebase / amend
Notes attach to a commit id; a rewritten commit loses them unless configured:
```bash
git config notes.rewriteRef refs/notes/commits      # copy notes on amend/rebase
```
`notes.rewriteRef` is the setting that matters: it names the ref(s) (glob allowed) whose notes
are copied. `notes.rewrite.amend` and `notes.rewrite.rebase` already default to true; set one to
false to opt a command out. Verified: with `notes.rewriteRef` set, a `git commit --amend` kept the
note on the new commit.

## When not to use
- Hosting web UIs generally do not display notes (check yours); anything reviewers must see
  belongs in the commit message, PR or a tag.
- Not for secrets or large data: they replicate to everyone who fetches the ref.

## Verify
- [ ] `git ls-remote origin 'refs/notes/*'` shows the namespace after pushing.
- [ ] `notes.rewriteRef` set wherever history is routinely rebased.
