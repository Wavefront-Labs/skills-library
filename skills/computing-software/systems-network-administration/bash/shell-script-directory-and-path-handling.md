---
id: computing-software.systems-network-administration.bash.shell-script-directory-and-path-handling
name: shell-script-directory-and-path-handling
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-script-dir, dirname-basename, realpath, cd-safety]
level: practitioner
status: docs-checked
description: "Find the script's own directory and handle paths safely with cd -P, pwd -P, parameter expansion and readlink -f."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://man7.org/linux/man-pages/man1/readlink.1.html
  - https://www.shellcheck.net/wiki/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paths in scripts

- Script directory (bash): `script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)`. `BASH_SOURCE` holds the source filenames for the function call stack; `$0` is the name of the shell or script, set at initialisation. `pwd -P` prints a path with no symbolic links; `cd -P` (and `set -o physical`) uses the physical directory structure rather than following the logical chain. Resolve a symlinked script itself with GNU `readlink -f`, which canonicalises every symlink in every component (all but the last component must exist); its man page recommends `realpath` for canonicalisation.
- Always handle `cd` failure: `cd -- "$dir" || exit 1` (ShellCheck SC2164: use `cd ... || exit` in case `cd` fails). A subshell, `( cd "$dir" && cmd )`, keeps the directory change from leaking.
- With a non-empty `CDPATH`, `cd` also prints the new absolute directory to standard output, which pollutes `$(...)` captures.
- In bash, `${p##*/}` strips the longest match of `*/` from the front (the file name part) and `${p%/*}` strips the shortest match of `/*` from the end (the directory part), without forking `basename` and `dirname`. Test paths without a slash, with trailing slashes, and `/`, because those cases behave differently.
- Extension handling: `${f%.*}` removes the shortest match of `.*` from the end; `${f##*.}` strips everything through the last dot.
- Tilde expansion applies to an unquoted tilde-prefix, so use `"$HOME/dir"` rather than `"~/dir"`.
- Build paths with `"${dir%/}/$name"` to avoid a doubled slash.

## Checked
2026-11-09. Confirmed in the bash manual (`BASH_SOURCE`, `$0`, `cd`/`pwd` `-P`, CDPATH output, `${parameter#word}`, `${parameter%word}` and the `##` / `%%` forms, tilde expansion) and the readlink man page; SC2164 title in the ShellCheck wiki index. Removed: macOS 12.3 version remark, `pushd`/`popd`, the file-test operator list and TOCTOU remark, and the leading-dot-file extension note, none of which the cited pages state; the POSIX root URL (a stub page) was dropped from sources.
Method: documentation only; no commands were run.
