---
id: computing-software.systems-network-administration.bash.shell-temp-files-mktemp-and-safe-paths
name: shell-temp-files-mktemp-and-safe-paths
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-mktemp, temp-files, race-conditions, safe-file-writes, umask]
level: practitioner
status: docs-checked
description: "Create temp files and directories safely with mktemp, understand the umask effect and clean up with an EXIT trap."
sources:
  - https://man7.org/linux/man-pages/man1/mktemp.1.html
  - https://man7.org/linux/man-pages/man2/umask.2.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temp files

- Use `tmp=$(mktemp)` for a file or `dir=$(mktemp -d)` for a directory. mktemp creates the file or directory safely and prints its name; files are created u+rw and directories u+rwx, minus umask restrictions. Do not invent names such as `/tmp/myscript.$$`.
- With no TEMPLATE, mktemp uses `tmp.XXXXXXXXXX` and `--tmpdir` is implied, so the file goes in `$TMPDIR` if set, else `/tmp`.
- A TEMPLATE must contain at least 3 consecutive `X`s in its last component. `mktemp -p "${TMPDIR:-/tmp}" myapp.XXXXXXXX` puts the template under a directory; with `-p` the TEMPLATE must not be an absolute name. `-t` is marked deprecated.
- `--suffix=SUFF` appends a suffix (no slash); it is implied if TEMPLATE does not end in `X`.
- `-u` / `--dry-run` only prints a name and creates nothing; the man page marks it unsafe, so do not use it for real temp files. `-q` silences creation-failure diagnostics.
- Clean up with a trap that runs when the shell exits: `trap 'rm -rf -- "$dir"' EXIT` (a sigspec of `0` or `EXIT` runs the action on shell exit).
- The umask removes permission bits from the mode requested at creation. The usual default umask is 022 (0666 becomes 0644). To make new secret files private, set `umask 077` before creating them (shell builtin; umask(2) describes the effect).
- A child created by `fork` inherits its parent's umask, and `execve` leaves it unchanged. A default ACL on the parent directory overrides the umask.
- Self-check: `ls -l "$tmp"` shows `-rw-------` under `umask 077`.

## Checked
Checked 2026-11-08 against mktemp(1) (template rules, defaults, options), umask(2) (effect, default 022, inheritance, default ACL) and the Bash manual (trap EXIT). Removed because the pages do not state them: BSD/macOS template behaviour, atomic replacement with `mv` and its cross-filesystem caveat, `chmod --reference` / `chown --reference`, and the advice about `ls`/`find` on temp dirs.

Method: docs-only read of cited pages, 2026-11-08
