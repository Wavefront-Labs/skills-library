---
id: computing-software.systems-network-administration.bash.mktemp-template
name: mktemp-template
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, mktemp-template, mktemp-suffix, shell-scripting]
level: practitioner
status: docs-checked
description: "Create temp files and dirs with mktemp templates, TMPDIR, suffixes and safe cleanup, and avoid predictable names."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/mktemp-invocation.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mktemp templates and suffixes
**Goal:** unpredictable, newly created temp paths.
```bash
tmp=$(mktemp)                              # template tmp.XXXXXXXXXX in $TMPDIR, else /tmp
dir=$(mktemp -d "${TMPDIR:-/tmp}/myapp.XXXXXX") || exit 1
f=$(mktemp --suffix=.json)                 # default template plus a suffix
f=$(mktemp "$dir/part.XXXXXX")
trap 'rm -rf "$dir"' EXIT
file=$(mktemp -q) && { echo data > "$file"; rm "$file"; }   # ignore failure to create
```
- `mktemp [option]... [template]` safely creates a temporary file or directory and prints its name. The template must include at least three consecutive `X`s in its last component; the final run of `X`s is replaced with alphanumeric characters (`62**n` possible names for n `X`s on a case-sensitive file system).
- With no template, `tmp.XXXXXXXXXX` is used and `--tmpdir` is implied: the file goes in `$TMPDIR` if set, otherwise `/tmp`.
- A file is created with read and write permission for the current user only, and a directory (`-d`) with read, write and search for the user only; the permissions are reduced further if the umask is more restrictive.
- `--suffix=suffix` appends a suffix (no slash); the template must then end in `X`. `-p dir` (`--tmpdir[=dir]`) makes the template relative to dir, or to `TMPDIR` / `/tmp` if dir is omitted or empty, and then the template must not be absolute. `-t` is deprecated in favour of `-p`.
- Joining a program name with `$$` is predictable and open to a symlink race; the manual says modern scripts should use mktemp because the name is unpredictable and knowing it implies this script created the file.
- `-u` (`--dry-run`) only generates a name that does not exist and creates nothing; using that name to create a file is inherently unsafe, since another process can create it first.
- `-q` suppresses diagnostics, but the exit status still shows whether a file was created: 0 if created, 1 otherwise.
- `trap action EXIT` (or `0`) runs the action when the shell exits, so it can remove the directory.

## Checked
Date: 2026-11-07
Method: Read the GNU coreutils mktemp page in full and the Bash manual trap builtin entry (EXIT). Trims: removed "6 X recommended", the BSD/macOS comparison and "--suffix is GNU only", the atomicity claim, the advice to use the same filesystem as an `mv` target, the `rm -rf --` form, the placeholder expansion `/tmp/tmp.XXXXXXXXXX` (the manual says `TMPDIR` or `/tmp`), and the `stat -c %a` self-check.
