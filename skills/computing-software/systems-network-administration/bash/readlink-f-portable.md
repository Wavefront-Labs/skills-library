---
id: computing-software.systems-network-administration.bash.readlink-f-portable
name: readlink-f-portable
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, readlink-f-portable, realpath-fallback, shell-scripting]
level: advanced
status: docs-checked
description: "Resolve symlinks in shell scripts: readlink -f, -e and -m semantics, realpath, and a plain-sh loop when they are missing."
sources:
  - https://man7.org/linux/man-pages/man1/readlink.1.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Portable readlink -f
**Goal:** get an absolute, symlink-free path where `readlink -f` may not exist.
```bash
rl() {                         # POSIX sh version, follows a final symlink chain
  target=$1
  while [ -L "$target" ]; do
    link=$(readlink "$target")
    case $link in /*) target=$link ;; *) target=$(dirname "$target")/$link ;; esac
  done
  ( cd "$(dirname "$target")" 2>/dev/null && printf '%s/%s\n' "$(pwd -P)" "$(basename "$target")" )
}
command -v realpath >/dev/null && realpath -- "$1"
```
- GNU `readlink` options (readlink(1)): `-f` canonicalises by following every symlink in every component recursively, all but the last component must exist; `-e` requires all components to exist; `-m` has no requirement that components exist; `-n` omits the trailing newline; `-z` ends output with NUL.
- The man page itself says `realpath(1)` is a better command for canonicalisation, so prefer it when present.
- `pwd -P` prints a working directory without symbolic links (bash manual), which is what resolves the directory part in the fallback above.
- A symlink loop never ends in the fallback: cap the iterations.
- Where `readlink -f` is missing, use the loop above or install the GNU tool; check the platform's own man page for which options its `readlink` supports.
- Self-check: compare the function's output with `realpath` on a system that has it, for a chain of symlinks.

## Checked
2026-11-09. Confirmed in the readlink(1) man page (options `-f`, `-e`, `-m`, `-n`, `-z`; realpath recommendation) and the bash manual (`pwd -P`). Removed: the python3 fallback, the macOS release-version remarks, the `greadlink` remark, and the claim about `realpath` on BSD, none of which the cited pages state.
Method: documentation only; no commands were run.
