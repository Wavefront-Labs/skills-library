---
id: computing-software.software-engineering.git.custom-diff-and-merge-drivers
name: custom-diff-and-merge-drivers
category: computing-software
field: software-engineering
product: git
tags: [git, git-customization, diff-driver, merge-driver, gitattributes, textconv, lockfiles, binary-files]
level: practitioner
status: gated
description: "Make Git diff and merge non-code files sensibly: textconv diff drivers for binaries, word diffs, union and custom merge drivers for lockfiles and changelogs."
sources:
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes
  - https://git-scm.com/docs/gitattributes
  - https://git-scm.com/docs/git-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom diff and merge drivers

**Goal:** readable diffs for documents/images and fewer pointless conflicts in generated or append-only files.

## 1. Diff drivers with textconv
```
# .gitattributes
*.docx  diff=docx
*.pdf   diff=pdf
*.png   diff=exif
*.md    diff=markdown
*.lockb binary
```
```bash
git config --global diff.docx.textconv "pandoc --to=plain"
git config --global diff.pdf.textconv  "sh -c 'pdftotext -layout -q \"\$0\" -'"   # Git appends the file path; pdftotext needs it before the '-' (stdout) argument
git config --global diff.exif.textconv exiftool
git config diff.docx.cachetextconv true
```
Built-in hunk-header drivers (per gitattributes; enable with the attribute only): `diff=python`, `java`, `golang`, `rust`, `csharp`, `cpp`, `markdown`, `html`, etc. They improve the `@@ ... @@ function` context line.
Word-level review: `git diff --word-diff=color` or `diff.<name>.wordRegex`.

## 2. Merge drivers
Built-in: `merge=text` (default), `merge=binary` (keep ours, mark conflict), `merge=union` (keep both sides' lines; good for append-only lists like CHANGELOG entries, dangerous for code).

Custom driver:
```ini
# .git/config or ~/.gitconfig (drivers are not versioned; document setup)
[merge "npm-lock"]
    name = take theirs; regenerate afterwards
    driver = cp %B %A
```
Placeholders: `%O` ancestor, `%A` ours (write result here), `%B` theirs, `%P` path, `%L` marker size. Exit 0 = resolved, non-zero = conflict.
```
package-lock.json merge=npm-lock
CHANGELOG.md      merge=union
```
The driver's result is whatever it leaves in `%A`, so it cannot regenerate the lockfile itself (a command that rewrites `package-lock.json` in the work tree is overwritten by `%A`). Run `npm install` after the merge. Checked: `cp %B %A` took theirs with no conflict; `merge=union` kept both sides' lines; `merge=binary` conflicted keeping ours.
Simpler, safer lockfile practice: on conflict, take either side and regenerate (`git checkout --theirs package-lock.json && npm install`), then commit.

## 3. Hide generated noise
```
dist/**              -diff linguist-generated=true
*.min.js             -diff
```
`-diff` shows "Binary files differ" while still merging as text.

## Gotchas
- Drivers referenced in `.gitattributes` but not configured fall back silently to defaults; CI and teammates need the config too (script it in a setup task).
- `union` can produce syntactically invalid files (duplicate JSON keys); never use on structured data.
- textconv affects `git diff`/`log -p` display only; patches made with `format-patch` use real content (`--no-textconv` is default there).
- `git check-attr diff merge -- file` confirms which driver applies.

## Verify
- `git diff HEAD~1 -- report.docx` shows text changes; a test merge of two branches adding CHANGELOG lines merges without conflict.

> Review note: some commands in this skill (Git Credential Manager, exiftool/pandoc textconv, signed tags, the `e` hunk-edit recipe) were not run during review. (gated: unconfirmed, source is paywalled or blocked)
