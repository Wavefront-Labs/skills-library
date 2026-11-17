---
id: computing-software.systems-network-administration.bash.posix-sh-portability-and-checkbashisms
name: posix-sh-portability-and-checkbashisms
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, checkbashisms, dash-portability, posix-sh, bin-sh, shellcheck, portability, bashisms]
level: practitioner
status: docs-checked
description: "Write scripts that run under /bin/sh (dash, busybox ash): common bashisms and POSIX replacements, checkbashisms and shellcheck -s sh, and when to just require bash."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
  - https://www.shellcheck.net/wiki/SC2039
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# POSIX sh portability

**Why:** `/bin/sh` is not always bash.
A `#!/bin/sh` script that uses bash-only features may fail where `/bin/sh` is a different shell.

## Common bashisms → POSIX
| Bash | POSIX sh |
|---|---|
| `[[ $a == b* ]]` | `case $a in b*) ...;; esac` |
| `[ "$a" == "$b" ]` | `[ "$a" = "$b" ]` |
| `function f { }` | `f() { }` |
| `local x` | not in the POSIX shell command language; avoid in `#!/bin/sh` scripts if strictly portable |
| arrays `a=(1 2)` | positional params `set -- 1 2`, or newline-separated strings |
| `$'\n'` | `nl='\n'` via `printf` : `nl=$(printf '\n_'); nl=${nl%_}` |
| `echo -e` | `printf '%s\n'` |
| `${var//a/b}`, `${var:0:3}` | `sed`/`cut`/`expr` |
| `source f` | `. f` |
| `&>file` | `>file 2>&1` |
| `<(cmd)` | temp file or FIFO |
| `read -a`, `read -p` | plain `read`, `printf` prompt |
| `set -o pipefail` | listed in POSIX.1-2024 (Shell Command Language); older shells may lack it, so do not rely on it in portable scripts |

## Check
```bash
checkbashisms -f script.sh          # Debian devscripts package
shellcheck -s sh script.sh          # warns about non-POSIX features
dash -n script.sh                                # parse test
```

## Decide
If you need arrays, `[[ ]]`, pipefail: write `#!/usr/bin/env bash` and say so. Use POSIX sh for
portable installers and anything run by `sh -c`.

## Verify
- [ ] `checkbashisms` clean.

## Checked
2026-11-02: confirmed against POSIX Shell Command Language (pubs.opengroup.org V3 chap 2: pipefail option in pipelines) and the ShellCheck wiki (SC3xxx replaced SC2039; scripts should declare their shell). Removed: distro-to-shell mapping, dash version gate, local support, busybox claims.
Method: documentation only; no commands were run.
