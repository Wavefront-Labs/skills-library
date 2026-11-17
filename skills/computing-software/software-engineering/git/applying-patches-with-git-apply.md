---
id: computing-software.software-engineering.git.applying-patches-with-git-apply
name: applying-patches-with-git-apply
category: computing-software
field: software-engineering
product: git
tags: [git, git-apply, patches, git-am, three-way-apply, reject-hunks, maintaining-a-project]
level: practitioner
status: verified
description: "Apply contributed diffs safely with git apply: --check and --stat first, --3way for drift, --reject for partial hunks, whitespace fixes, and when to use git am instead."
sources: ["https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project", "https://git-scm.com/docs/git-apply", "https://git-scm.com/docs/git-am"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying patches with git apply

**Goal:** take a diff from an issue, email or CI artifact and land it without
half-applied files or lost authorship.

## apply vs am
| Input | Tool | Result |
|---|---|---|
| plain `git diff` / `diff -u` output | `git apply` | changes in working tree (no commit) |
| `git format-patch` mbox (has From/Subject/Date) | `git am` | commits with original author + message |

`git apply` is all-or-nothing by default: if any hunk fails, nothing is applied. GNU
`patch` would apply partially and leave `.rej` files silently.

## Workflow
```bash
git switch -c review/issue-482          # never on main
git apply --stat fix.patch              # what files
git apply --check -v fix.patch          # would it apply?
git apply fix.patch                     # working tree only
git apply --index fix.patch             # also stage
git commit --author="Jane Doe <jane@example.org>" -m "Fix parser crash on empty input"
```
Attribute when the patch came from someone else (`--author`, or a `Co-authored-by:` trailer).

## When it does not apply
```bash
git apply --3way fix.patch       # 3-way merge via blob ids in the patch's index lines; implies --index (stages the result), may leave conflict markers
git apply --reject fix.patch     # apply good hunks, write *.rej for failures; fix by hand (cannot combine with --3way)
git apply -p2 fix.patch          # strip 2 leading path components (patch made outside repo root)
git apply --directory=sub fix.patch   # prepend a directory
git apply -C1 fix.patch          # require less context (risky)
```
`--3way` needs the preimage blobs to exist in your repo (patch made with `git diff` from
a related history). For `git am` failures: `git am -3`, resolve, `git add`, `git am --continue`;
`git am --abort` to give up.

## Whitespace
`--whitespace=warn|fix|error|nowarn`. Patches pasted through chat/email often have
CRLF or trailing-space damage: `git apply --whitespace=fix --ignore-whitespace`.
"corrupt patch at line N" usually means a wrapped or tab-mangled patch: ask for an
attachment, not inline text.

## Reverse
`git apply -R fix.patch` undoes an applied patch (also `--check -R` to test if already applied).

## Verify
- [ ] `--check` passed before applying; tests run on the branch.
- [ ] Commit carries the contributor's authorship.
