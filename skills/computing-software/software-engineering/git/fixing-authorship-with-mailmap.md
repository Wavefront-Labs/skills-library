---
id: computing-software.software-engineering.git.fixing-authorship-with-mailmap
name: fixing-authorship-with-mailmap
category: computing-software
field: software-engineering
product: git
tags: [git, git-mailmap, rewrite-author, author-identity, filter-repo, shortlog, git-tools]
level: practitioner
status: verified
description: "Unify contributor identities with .mailmap without rewriting history, or rewrite author/committer names and emails with filter-repo or rebase --exec when history must change."
sources: ["https://git-scm.com/docs/gitmailmap", "https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History", "https://htmlpreview.github.io/?https://github.com/newren/git-filter-repo/blob/docs/html/git-filter-repo.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixing authorship with mailmap and history rewrites

**Goal:** one person = one identity in shortlog/blame, and wrong emails corrected, with
the least disruptive tool.

## Option 1: .mailmap (no rewrite - prefer this)
Commit a `.mailmap` at the repo root:
```
# Proper Name <proper@email>  Commit Name <commit@email>
Jane Doe <jane@example.org> <jane@laptop.local>
Jane Doe <jane@example.org> jdoe <jdoe@oldcorp.com>
Bot Account <bot@example.org> <12345+bot@users.noreply.github.com>
```
Used by `git shortlog`, `git blame`, `git log` with `%aN %aE` placeholders, and
`git check-mailmap "jdoe <jdoe@oldcorp.com>"` to test. `log`, `show` and `whatchanged` honour it by default via `log.mailmap` (true by default per git-config); `%aN`/`%aE` always map. Whether a hosting site's contributor graph reads .mailmap varies (not checked; verify in its docs).

## Option 2: fix the last commits before pushing
```bash
git commit --amend --reset-author --no-edit        # last commit, uses current config
git rebase -r --exec 'git commit --amend --no-edit --reset-author' origin/main
```
Set the right identity first: `git config user.email jane@example.org` (or per-directory
with `includeIf`).

## Option 3: rewrite all history (shared repo, coordinated)
```bash
pip install git-filter-repo
git filter-repo --mailmap my-mailmap.txt          # same format as .mailmap, applies permanently
# or callback for complex rules:
git filter-repo --email-callback 'return email.replace(b"@oldcorp.com", b"@example.org")'
```
filter-repo rewrites every commit hash, removes the `origin` remote as a safety measure (per its docs, `--force` disables that), and
requires a fresh clone by default (`--force` overrides). Everyone must re-clone; open PRs
break; signed commits lose valid signatures. `git filter-branch --env-filter` still works
but its manual says its use is not recommended (safety and performance) and points to git filter-repo.

## Preventing recurrence
- `git config --global user.useConfigOnly true` - refuse to commit until name/email set.
- Server-side or CI check that author emails match an allowed domain.
- GitHub "Keep my email private" -> use the `noreply` address consistently.

## Verify
- [ ] `git shortlog -sne` shows one line per person.
- [ ] After a rewrite: `git log --format='%ae' | sort -u` contains no old emails.
