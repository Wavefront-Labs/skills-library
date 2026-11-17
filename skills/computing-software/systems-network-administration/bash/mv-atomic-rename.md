---
id: computing-software.systems-network-administration.bash.mv-atomic-rename
name: mv-atomic-rename
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, mv-atomic-rename, atomic-replace, shell-scripting]
level: advanced
status: docs-checked
description: "Replace files in shell scripts by writing a temp file in the target directory and renaming it over the target with mv."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/mktemp-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomic replace with mv rename
**Goal:** readers never see a partial file.
```bash
dst=/etc/app/app.conf
tmp=$(mktemp "${dst}.XXXXXX") || exit 1      # same directory as the target
trap 'rm -f -- "$tmp"' EXIT
generate_config > "$tmp" && chmod 644 "$tmp"
mv --no-copy -f -- "$tmp" "$dst"             # rename only; fail rather than copy
ln -sfn "release-42" current.new && mv -T current.new current   # swap a symlink
```
- `mv` ordinarily renames. If the destination is on a different file system it falls back to copying then removing the original, so keep the temp file in the destination directory. GNU `mv --no-copy` fails with a diagnostic instead of copying.
- `mktemp` needs a template with at least three `X`s in the last component; the file is created readable and writable by the current user only (reduced further by a stricter umask), so set the final mode on the temp file before the rename.
- `-T` (`--no-target-directory`) stops `mv` and `ln` treating the last operand specially when it is a directory or a symlink to a directory; that is why the symlink swap uses `mv -T`.
- GNU `ln -f` replaces the destination, and the coreutils manual says that unless `--backup` is used there is no brief moment when the destination does not exist (stated as an extension to POSIX). `-n` (`--no-dereference`) is weaker than `-T`.
- Avoid a trailing slash on a source name that may be a symlink to a directory; `mv` behaviour then depends on the underlying rename call.
- Self-check: a reader loop never sees an empty or partial file while the writer runs.

## Checked
2026-11-09. Confirmed in the coreutils manual pages for mv, ln and mktemp: rename-then-copy fallback, `--no-copy`, `-T`, `ln -f` / `-n` behaviour, the no-gap statement, mktemp template and permissions. Removed: claims that rename(2) is atomic, that `ln -sfn` alone is not atomic (the ln page says otherwise), `sync -d` and its coreutils version, and the fsync advice (sync page was not readable).
Method: documentation only; no commands were run.
