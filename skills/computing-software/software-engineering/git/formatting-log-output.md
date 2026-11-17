---
id: computing-software.software-engineering.git.formatting-log-output
name: formatting-log-output
category: computing-software
field: software-engineering
product: git
tags: [git, git-log, git-log-format, pretty-format, log-graph, commit-limiting, git-basics]
level: practitioner
status: verified
description: "Shape git log output: --oneline --graph, --pretty=format placeholders, date formats, limiting by author/date/path/merges, and stable machine-readable output for scripts."
sources: ["https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History", "https://git-scm.com/docs/git-log", "https://git-scm.com/docs/pretty-formats"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formatting log output

**Goal:** get exactly the history view you need: visual topology, a release list, or
parseable data for a script.

## Everyday views
```bash
git log --oneline --graph --decorate --all     # topology of every branch
git log --oneline main..feature                # commits on feature not on main
git log --first-parent main                    # mainline only (one entry per merged PR)
git log -p -2                                  # last two commits with patches
git log --stat --since="2 weeks ago" -- src/api
```
Alias it (checked): `git config --global alias.lg "log --graph --pretty=format:'%C(auto)%h %d %s %C(dim)%an, %ar'"`.

## Pretty format placeholders
| Placeholder | Meaning |
|---|---|
| `%H` / `%h` | full / abbreviated hash |
| `%an` `%ae` / `%cn` `%ce` | author / committer name, email |
| `%ad` `%ar` / `%cd` `%cr` | author / committer date, relative |
| `%s` `%b` `%B` | subject, body, raw message |
| `%d` / `%D` | ref names decoration |
| `%(trailers:key=Co-authored-by)` | parsed trailers |
| `%C(auto)` `%Cred` `%Creset` | colours |

Author date = when written; committer date = when applied (rebases change it).
`--date=iso-strict`, `--date=short`, `--date=format:%Y-%m-%d` control `%ad`.

## Limiting
```bash
git log --author="alice" --since=2026-01-01 --until=2026-03-31
git log --no-merges   |   git log --merges
git log -n 20 --skip=40
git log --grep="JIRA-123" -i --all-match --grep="fix"
git log --diff-filter=D --name-only    # commits that deleted files
git log v1.4.0..v1.5.0 --format="- %s (%h)" --no-merges   # draft release notes
```
Author filters are regex on "Name <email>"; use a `.mailmap` so variants collapse.

## Script-safe output
- Use `--format` with an unambiguous separator: `--format='%H%x09%an%x09%s'` (tab) or
  `%x00` with `-z`.
- Never parse porcelain-for-humans (`--oneline`, colours); add `--no-color`.
- `git rev-list --count main..HEAD` is cheaper than counting log lines.
- `log.showSignature`, `log.decorate` and pager config change output; scripts should
  call `git -c log.showSignature=false --no-pager log ...`.

## Verify
- [ ] Release-note commands use `--no-merges` or `--first-parent` deliberately.
- [ ] Scripts use explicit `--format`, never default output.
