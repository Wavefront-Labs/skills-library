---
id: computing-software.software-engineering.v-lang.v-fmt-vet-and-doc-tools
name: v-fmt-vet-and-doc-tools
category: computing-software
field: software-engineering
product: v-lang
tags: [v-fmt-vet-and-doc-tools, v-cli-run-and-build, v fmt, v vet, v doc, formatting, lint, check-md, -verify, ci, v-lang]
level: practitioner
status: docs-checked
description: "Format with v fmt -w and -verify, switch it off with vfmt off, install the pre-commit hook and generate docs with v doc."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# v fmt and v doc

Goal: keep code consistent without debate.

- `v fmt file.v` formats; `v fmt -w file.v` writes the result back. The docs recommend running `v fmt -w` on every save and before pushing. A run takes under 30 ms.
- `v fmt -verify` and `v fmt -c` check formatting without writing; during the formatter transition they accept either current or legacy output, while `-w` rewrites to current formatting.
- The formatter checks syntax only, so it works on incomplete code that does not pass semantic checks.
- Wrap a region in `// vfmt off` and `// vfmt on` to leave it alone.
- Single-statement function, loop, `if` or `match` bodies stay on one line if written that way and they fit in 100 columns.
- `v git-fmt-hook install` (inside a Git repo) installs a pre-commit hook that runs `v fmt -w` on staged V files; `status` and `remove` manage it; `git commit --no-verify` skips it. `git config --bool --add hooks.stopCommitOfNonVfmtedVFiles true` makes it reject instead of format.
- `v doc net.http` generates documentation for a module; comments are written in present tense and the module overview goes in the first comment after the module name.

Gotchas:
- The hook on Windows needs `v` visible in Git Bash/MSYS2/Cygwin (`v symlink`).
- `v fmt` is not configurable beyond the off/on comments.

Verify: `v fmt -verify file.v` accepts a formatted file.

## Checked

2026-11-08. Read: the "Tools" section (`v fmt`, disabling formatting, Git pre-commit hook) and the documentation-comments section of doc/docs.md (vlang/v). Removed unconfirmed claims: `v vet`, `v fmt -diff`, `v doc -f html -o`, `v missdoc`, `v check-md` usage (only a pointer exists), attribute-syntax migration, CRLF normalisation and `v-analyzer`. docs.vlang.io and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
