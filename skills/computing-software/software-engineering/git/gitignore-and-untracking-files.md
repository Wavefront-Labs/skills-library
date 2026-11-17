---
id: computing-software.software-engineering.git.gitignore-and-untracking-files
name: gitignore-and-untracking-files
category: computing-software
field: software-engineering
product: git
tags: [git, gitignore, git-rm-cached, check-ignore, exclude, global-gitignore, untrack-file]
level: practitioner
status: verified
description: "Write .gitignore patterns that do what you expect, debug them with check-ignore, and stop tracking files that were committed by mistake."
sources: ["https://git-scm.com/docs/gitignore", "https://git-scm.com/docs/git-check-ignore", "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .gitignore patterns and untracking files

**Goal:** keep build output, secrets and editor junk out of the repo, and fix it cleanly
when something got committed anyway.

## Where ignore rules live (highest priority first)
1. Command line (rare).
2. `.gitignore` in the file's directory, then parents up to the repo root (shared, committed).
3. `.git/info/exclude` - personal, per-clone, never committed.
4. `core.excludesFile` (default `$XDG_CONFIG_HOME/git/ignore`, else `~/.config/git/ignore`) - personal, all repos. Put
   `.DS_Store`, `.idea/`, `*.swp` here instead of every project's `.gitignore`.

## Pattern rules that bite
| Pattern | Matches |
|---|---|
| `build` | any file or dir named build at any depth |
| `/build` | only build at the root of this .gitignore's dir |
| `build/` | directories named build only |
| `*.log` | any depth (no slash in pattern) |
| `docs/*.md` | only direct children of docs (a middle slash anchors the pattern) |
| `docs/**/*.md` | any depth under docs |
| `!keep.log` | re-include |

- You cannot re-include a file if a parent directory is excluded: `logs/` then
  `!logs/keep.txt` does nothing. Use `logs/*` then `!logs/keep.txt`.
- Trailing spaces are ignored unless quoted with a backslash (gitignore docs), so to match a name that ends in a space write `name\ `.
- To keep an empty directory, commit `dir/.gitkeep` and ignore `dir/*` with `!dir/.gitkeep`.

## Debug: why is this file ignored (or not)?
```bash
git check-ignore -v path/to/file      # prints source file:line:pattern that matched
git status --ignored                  # list ignored files
git ls-files -ci --exclude-standard   # tracked files that WOULD be ignored now
```

## Untrack a committed file but keep it locally
```bash
echo "config/local.env" >> .gitignore
git rm --cached config/local.env      # -r for a directory
git commit -m "Stop tracking local.env"
```
`.gitignore` never affects files already tracked; the `rm --cached` is required.
Warning: teammates who pull this commit get the file DELETED from their working tree.
Tell them to back it up first, or ship a `local.env.example` template.

If the file held a secret, untracking is not enough: it is still in history. Rotate the
secret, then see computing-software.software-engineering.git.removing-sensitive-data-from-history.

## Ignoring local edits to a tracked file
`git update-index --skip-worktree path` hides local changes (for example a dev config)
from `status`. It is per-clone and lost on some operations; prefer a template file plus
an ignored local override.

Checked in a scratch repo: `logs/` + `!logs/keep.txt` ignores keep.txt (check-ignore names the `logs/` rule), the `logs/*` form does not, `/build` vs `build/` match as tabled, and `ls-files -ci --exclude-standard` lists tracked-but-now-ignored files.
## Verify
- [ ] `git check-ignore -v <file>` names the rule you intended.
- [ ] `git ls-files -ci --exclude-standard` returns nothing unexpected.
- [ ] A fresh clone plus build leaves `git status` clean.
