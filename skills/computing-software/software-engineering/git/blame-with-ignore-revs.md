---
id: computing-software.software-engineering.git.blame-with-ignore-revs
name: blame-with-ignore-revs
category: computing-software
field: software-engineering
product: git
tags: [git, git-tools, git-blame, ignore-revs, blame-ignore-revs-file, code-archaeology, move-detection, git-blame-w]
level: practitioner
status: verified
description: "Get useful git blame output: skip whitespace and moved code (-w -M -C), ignore mass-reformat commits via .git-blame-ignore-revs, and blame past a change."
sources: ["https://git-scm.com/docs/git-blame", "https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git", "https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#ignore-commits-in-the-blame-view"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blame that points at the real author

**Goal:** find the commit that introduced the logic on a line, not the commit that
reformatted it, moved it or renamed the file.

## Flags that matter
```bash
git blame -L 40,80 src/cache.py      # just a range
git blame -L :evict src/cache.py     # a function (with diff driver configured)
git blame -w file                    # ignore whitespace changes
git blame -M file                    # detect lines moved within the file
git blame -C file                    # also lines moved/copied from other files changed in the same commit
git blame -C -C file                 # ... and copies from other files in the commit that created the file
git blame -C -C -C file              # ... and from any commit (slowest)
git blame --since=1.year file
git blame <sha>^ -- file             # blame as of the parent of a commit: "who was before this?"
```

## Ignoring formatting commits
1. Create `.git-blame-ignore-revs` at the repo root with full shas, one per line, with
   a comment for each (`# black reformat 2025-03`).
2. Tell local Git: `git config blame.ignoreRevsFile .git-blame-ignore-revs`.
3. GitHub reads `.git-blame-ignore-revs` automatically in its blame view; GitLab (17.10+) also reads it but a viewer must tick "Ignore specific revisions" in blame preferences.
   The file takes one unabbreviated object name per line; `#` comments are allowed. Command-line equivalent: `--ignore-revs-file <file>` or `--ignore-rev <rev>`.
Lines changed only by an ignored commit are attributed to the previous change; with
`blame.markIgnoredLines=true` they get a `?` marker so you know (verified: `^?8e00de`), and
`blame.markUnblamableLines=true` marks lines that could not be attributed with `*`.

Make the reformat a single dedicated commit (no logic changes) precisely so it can be
ignored.

## Getting from a line to "why"
1. `git blame -w -C -C -L ...` finds the commit.
2. `git show <sha>` for the full change and message; follow the PR/issue reference.
3. If the commit is a move or merge, repeat with `<sha>^`, or switch to
   `git log -L` for the whole evolution
   (see computing-software.software-engineering.git.searching-history-with-log-and-pickaxe).

## Gotchas
- Blame shows who last touched a line, not who designed it. Use it to find context,
  not culprits.
- `-C -C -C` (three) searches every commit for copies; slow on big repos.

## Verify
- [ ] `blame.ignoreRevsFile` is set and the ignore file contains every bulk-format commit.
- [ ] Blame on a reformatted file shows pre-reformat authors.
