---
id: computing-software.software-engineering.git.line-endings-autocrlf-and-gitattributes
name: line-endings-autocrlf-and-gitattributes
category: computing-software
field: software-engineering
product: git
tags: [git, git-customization, line-endings, autocrlf, gitattributes, eol, crlf, cross-platform]
level: practitioner
status: verified
description: "Stop CRLF/LF churn across Windows, macOS and Linux with .gitattributes eol rules, sane core.autocrlf settings and a one-time renormalisation."
sources:
  - https://git-scm.com/docs/gitattributes
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/git-add
  - https://git-scm.com/docs/git-ls-files
  - https://git-scm.com/docs/git-blame
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Line endings with autocrlf and .gitattributes

**Goal:** the repository stores LF for text, each OS gets what its tools need, and diffs never show whole-file changes caused by line endings.

## 1. Commit a .gitattributes (repo policy beats personal config)
```
* text=auto eol=lf
*.sh   text eol=lf
*.bat  text eol=crlf
*.cmd  text eol=crlf
*.ps1  text eol=crlf
*.sln  text eol=crlf
*.png  binary
*.jpg  binary
*.zip  binary
```
- `text=auto`: Git decides whether a file is text; text files are converted to LF in the repo (unless they already contain CRLF in the repo).
- `eol=lf|crlf`: the line ending the working tree gets on checkout; it only has effect with `text` or `text=auto`, and setting `eol` implies `text` if `text` was unspecified.
- `binary` = `-text -diff -merge`: never converted, never textually diffed.

## 2. Personal setting (fallback when no attributes)
- Windows: `git config --global core.autocrlf true` (equivalent to `text=auto` everywhere with `core.eol=crlf`: LF in repo, CRLF on checkout).
- macOS/Linux: `git config --global core.autocrlf input` (CRLF to LF on commit, no conversion on checkout).
- `core.safecrlf=warn` warns when a conversion would not be reversible (`true` rejects the file).
`core.autocrlf` is consulted only for paths where the `text` attribute is unspecified (and for the checkout ending when `eol` is unspecified), so a committed `.gitattributes` takes precedence for the paths it matches.

## 3. Renormalise an existing repo once
```bash
# after adding .gitattributes, on a clean tree
git add --renormalize .
git status          # shows files whose stored endings change
git commit -m "Normalize line endings"
```
List that commit in a file (conventionally `.git-blame-ignore-revs`) and point blame at it with `git config blame.ignoreRevsFile .git-blame-ignore-revs`; Git does not read that file name on its own.

## 4. Diagnose
```bash
git ls-files --eol                        # i/ = index, w/ = working tree, attr/ = attribute applied
git check-attr -a -- path/to/file
```

## Gotchas
- Files that keep showing as modified usually mean conflicting rules; compare `git ls-files --eol` with `git check-attr -a`.
- Shell scripts checked out with CRLF break on Linux; force `eol=lf` for them.
- Do not mark generated lockfiles `binary` just to hide diffs; `-diff` alone stops textual diffs without disabling text conversion or merge.

## Verify
- Fresh clone on Windows and Linux: `git status` clean, and `git ls-files --eol` shows `i/lf` in the index column for every text file.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed in gitattributes and git-config: `text`, `text=auto`, `eol` semantics and the unspecified-attribute fallback to `core.autocrlf` / `core.eol`; `binary` macro is `-diff -merge -text`; `core.autocrlf true` equals `text=auto` plus `core.eol=crlf`, `input` does no output conversion; `core.safecrlf` true/warn; `git add --renormalize`; `git ls-files --eol` output format (`i/`, `w/`, `attr/`); `blame.ignoreRevsFile`. Removed as unconfirmed: the `.editorconfig`, `linguist-generated`, `file` command and `/bin/sh^M` remarks and the exact warning text. The GitHub line-endings page cited earlier was not re-fetched and is no longer listed.

2026-11-01, run with Git 2.46.2 (Windows, Git Bash) in throwaway repos with a local bare remote. Confirmed on Windows: with `* text=auto eol=lf`, a CRLF text file is stored as LF (`i/lf w/crlf`, warning that CRLF will be replaced); `*.bat text eol=crlf` stores LF and checks out CRLF; `binary` shows `text: unset`, `diff: unset`, `merge: unset` in `check-attr -a` and the PNG is stored untouched (`i/crlf`); `git ls-files --eol` columns `i/`, `w/`, `attr/`; `git add --renormalize .` re-stages files after attributes change; `core.safecrlf`, `core.autocrlf` and `blame.ignoreRevsFile` accepted as config. macOS `core.autocrlf input` was not run (docs only).

Method: documentation checked, then the commands were run as above (Git 2.46.2, local repositories only).
