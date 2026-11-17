---
id: computing-software.software-engineering.git.removing-and-moving-files
name: removing-and-moving-files
category: computing-software
field: software-engineering
product: git
tags: [git, git-mv, git-rm, rename-detection, follow-renames, case-only-rename, git-basics]
level: practitioner
status: verified
description: "Remove and rename tracked files with git rm and git mv, understand that Git detects renames heuristically, follow history across renames and fix case-only renames."
sources:
  - https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
  - https://git-scm.com/docs/git-mv
  - https://git-scm.com/docs/git-rm
  - https://git-scm.com/docs/git-log
  - https://git-scm.com/docs/git-blame
  - https://git-scm.com/docs/diff-options
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Removing and moving files

**Goal:** delete and rename files so history stays followable and nothing surprising
lands in the commit.

## Removing
```bash
git rm path/file.py            # delete from disk and stage the deletion
git rm -r build/               # directory
git rm --cached secrets.env    # stop tracking, keep the local file (then .gitignore it)
git rm -n -r 'logs/*.log'      # dry run; quote globs so Git (not the shell) expands them
```
Deleting with the OS then `git add -A` (or `git add -u`) stages the same thing.
`git rm` requires the files to be identical to the tip of the branch with no updates staged; `-f` overrides that check - think first. With `--cached` the staged content must match either the branch tip or the file on disk.

## Renaming
```bash
git mv old_name.py new_name.py
```
Git stores no rename metadata. `git mv` is equivalent to `mv` + `git rm` + `git add` (Pro Git). Renames are
inferred at diff/log time by content similarity (the default similarity index is 50%).

Consequences:
- Rename **and** heavily edit in one commit and similarity drops below 50%: history
  shows delete + add. Do the rename in its own commit, then edit.
- `git log --follow -- new_name.py` follows one file across renames (single path only).
- `git blame -M` detects lines moved within a file and `-C` lines copied from other files (repeat `-C` to look harder).
- Tune detection: `git log -M30% --stat`, `git diff -M --find-copies`.
- Large renames in merges: `merge.renameLimit` (falling back to `diff.renameLimit`) caps the rename detection work; raise it if detection is skipped.

## Case-only renames (Windows / macOS)
On case-insensitive filesystems (APFS, HFS+, FAT, NTFS) `git clone` and `git init` probe the filesystem and set `core.ignoreCase` to true, which makes Git treat a name differing only in case as the same file. Check the result of a case-only rename with `git status` and `git ls-files` before committing, and do not turn `core.ignoreCase` off to work around it: the setting reflects the filesystem.

## Verify
- [ ] `git status` shows `renamed:` not `deleted:` + `new file:` for intended renames (after staging).
- [ ] After a case-only rename, `git ls-files` lists only the new spelling.
- [ ] `git log --follow --oneline -- <new path>` reaches the pre-rename history.
- [ ] `git rm --cached` targets are now in `.gitignore`.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22) and the Pro Git recording-changes chapter. Confirmed: `git rm` checks, `--cached`, `-n`/`--dry-run`, `-r`; `git mv` equivalence and no stored rename metadata (Pro Git); default rename similarity 50% and `-M<n>` / `-C` (diff-options); `git log --follow` works for a single file only; `git blame -M` / `-C` / `-C -C`; `merge.renameLimit` falls back to `diff.renameLimit`; `core.ignoreCase` is probed and set by clone and init on case-insensitive filesystems. Removed as unconfirmed: the exact rename-limit warning text, the temporary-name case-rename recipe, the phantom-duplicates claim and the statement that blame follows renames automatically.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed: `git rm -n -r 'logs/*.log'` dry run; `git rm --cached` keeps the file on disk; `git rm` refuses a file with local modifications and `-f` overrides; `git rm --cached` refuses staged content that differs from both file and HEAD; `git rm -r`; `git mv` shows as `R` in status; `git log --follow`; `git log -M30% --stat`; `git diff -M --find-copies`; `git blame -M -C -C`; `core.ignoreCase` is `true` after init on NTFS; a case-only `git mv` leaves only the new spelling in `git ls-files`. `merge.renameLimit` is docs only.

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
