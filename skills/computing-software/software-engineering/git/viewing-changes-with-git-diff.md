---
id: computing-software.software-engineering.git.viewing-changes-with-git-diff
name: viewing-changes-with-git-diff
category: computing-software
field: software-engineering
product: git
tags: [git, git-diff, word-diff, staged-changes, diff-stat, diff-algorithm, git-basics]
level: practitioner
status: verified
description: "Read exactly what changed with git diff: working tree vs index vs HEAD, --staged, ranges, --stat/--name-status, word diffs, whitespace and move detection."
sources:
  - https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
  - https://git-scm.com/docs/git-diff
  - https://git-scm.com/docs/diff-options
  - https://git-scm.com/docs/git-difftool
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/gitattributes
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Viewing changes with git diff

**Goal:** know precisely what you are about to commit, what a branch changes, and
read noisy diffs (reformatting, moved code, prose) without missing the real change.

## The three trees
```bash
git diff                   # working tree vs index  (unstaged only!)
git diff --staged          # index vs HEAD          (what commit will record; alias --cached)
git diff HEAD              # working tree vs HEAD   (everything uncommitted)
git diff main...feature    # what feature added since it forked from main (merge-base)
git diff main..feature     # tip vs tip (includes main's newer changes, reversed) - rarely what you want
git diff A B -- path/      # limit to paths
```
Classic surprise: `git diff` shows nothing after `git add` because the change is now in
the index; use `--staged`.

## Summaries
```bash
git diff --stat main...HEAD          # files + insertions/deletions
git diff --name-status main...HEAD   # A/M/D/R100 per file
git diff --name-only --diff-filter=AM main...HEAD   # added/modified only, for scripts
git diff --shortstat
```

## Reading noisy diffs
```bash
git diff --word-diff                 # inline [-old-]{+new+}; good for prose/Markdown
git diff --word-diff=color --word-diff-regex='[^[:space:]]'   # character-level
git diff -w                          # ignore all whitespace (reindent PRs)
git diff --ignore-blank-lines
git diff --color-moved=zebra --color-moved-ws=allow-indentation-change   # moved blocks
git diff --diff-algorithm=histogram  # pick a different diff algorithm (default, minimal, patience, histogram)
git diff -M50% --stat                # rename detection threshold
git diff --function-context          # whole enclosing function per hunk (-W)
```
Make it permanent: `git config --global diff.algorithm histogram`,
`git config --global diff.colorMoved zebra`.

## Specials
- Binary file shows "Binary files differ": add a textconv driver in `.gitattributes`
  (e.g. `*.docx diff=docx`) - see custom diff drivers skill.
- `git diff --check` flags trailing whitespace and conflict markers; use in hooks.
- `git diff --no-index a.txt b.txt` diffs two arbitrary files outside a repo.
- `git difftool -d main...HEAD` opens a directory diff in your configured tool.
- Patches for email/apply: `git diff > fix.patch`; binary-safe needs `--binary`.

## Verify
- [ ] Before committing: `git diff --staged` reviewed, `git diff` empty or intentional.
- [ ] Before opening a PR: `git diff --stat origin/main...HEAD` matches what you expect.
- [ ] `git diff --check` clean.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed in git-diff and diff-options: `--cached` with `--staged` as a synonym, `A...B` merge-base form, `--stat`, `--shortstat`, `--name-status`, `--name-only` with `--diff-filter`, `--word-diff` and `--word-diff-regex`, `-w`, `--ignore-blank-lines`, `--color-moved` with `--color-moved-ws=allow-indentation-change`, `--diff-algorithm`, `-M<n>%`, `--function-context`, `--check`, `--no-index`, `--binary`; config `diff.algorithm` and `diff.colorMoved`; `git difftool -d/--dir-diff`. Removed as unconfirmed: the claim that histogram is often clearer than the default algorithm.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `git diff` is empty after `git add` while `--staged` and `--cached` show the change; `HEAD`, `main...feature` (feature's own commits only) versus `main..feature` (also shows main's newer change reversed); `--stat`, `--shortstat`, `--name-status`, `--name-only --diff-filter=AM`, `--word-diff` (`{+new+}`), `--word-diff-regex`, `-w`, `--ignore-blank-lines`, `--color-moved` with `--color-moved-ws=allow-indentation-change`, all four `--diff-algorithm` values, `-M50%`, `--function-context` and `-W`, `--binary`, `--no-index` on two files outside the repo, and `--check` (exit 0 clean, exit 2 with a trailing-whitespace report). Not run: `git difftool -d` and the docx textconv driver (docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
