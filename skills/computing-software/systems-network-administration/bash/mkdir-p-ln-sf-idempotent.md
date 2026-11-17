---
id: computing-software.systems-network-administration.bash.mkdir-p-ln-sf-idempotent
name: mkdir-p-ln-sf-idempotent
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, mkdir-p-ln-sf-idempotent, ln-sfn, shell-scripting]
level: practitioner
status: docs-checked
description: "Write re-runnable file setup in shell: mkdir -p, ln -sfn, install, cp -n and checks that avoid errors on second run."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/install-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/rmdir-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Re-runnable mkdir and ln
**Goal:** setup commands that are safe to run twice (GNU coreutils behaviour).
```bash
mkdir -p "$dir"                              # no error if it is already a directory
ln -sfn "$target" "$link"                    # replace an existing link; -n: treat a symlink to a dir as a file
install -d -m 750 -o app -g app /var/lib/app
install -C -m 644 file /etc/app/file         # -C: leave dest untouched if content and attributes match
cp -n src dst                                # do not overwrite; silently skip (deprecated)
rm -f "$f"; rmdir --ignore-fail-on-non-empty "$d"
```
- `mkdir name` reports an error if name exists, unless `-p` is given and name is a directory. `-p` also creates missing parents (mode `=rwx,u+wx`, i.e. the umask modified by `u+wx`) and ignores existing parents. `-m` does not affect parents created by `-p`.
- `ln -f` removes an existing destination so the link can be created; without `-n`, a destination that is a symlink to a directory is treated like a directory, so the new link is created inside it. `-n` treats it as a normal file, and `-T` is stronger than `-n`.
- Without `--backup`, `ln -f` has no brief moment where the destination does not exist (a GNU extension to POSIX).
- `install -d` creates each directory and missing parents (parents get 755 regardless of `-m` and the umask); `-m`, `-o`, `-g` set mode, owner and group. `-o` only takes effect when run with the privilege to set ownership. `-C` is best used with `-m`, `-o` and `-g`, because otherwise install may determine the default attributes wrongly and make redundant copies.
- `cp --no-clobber` (`-n`) is deprecated because its exit status differs from other platforms; `--update=none` skips existing files without a failure and `--update=none-fail` diagnoses them and fails.
- `rm -f` ignores nonexistent files and missing operands and never prompts. `rmdir` errors on a directory that is not an existing empty one; `--ignore-fail-on-non-empty` ignores failures on non-empty directories.
- An exit status of zero indicates success and nonzero failure for each of these tools.

## Checked
Date: 2026-11-07
Method: Read the GNU coreutils manual pages for mkdir, ln, install, cp (the -n and --update entries), rm (-f) and rmdir in full; the old draft cited only the Bash manual, which does not describe these utilities, so the sources were replaced. Trims and corrections: replaced `install -m 644 file ...` "compare first" comment with `install -C`, removed `[ -e "$f" ] || touch "$f"` (touch is not on the pages), removed the `--` after `rm -f`, the "changed=1" advice and the invented Verify step, and marked `cp -n` as deprecated. The `--update=none` forms are quoted from the cp page.
