---
id: computing-software.systems-network-administration.bash.invoke-as-sh-mode
name: invoke-as-sh-mode
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, invoke-as-sh-mode, bash-posix-mode, shell-scripting]
level: advanced
status: docs-checked
description: "Understand how bash behaves when invoked as sh or with --posix: startup files, POSIX mode and what changes in it."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bash invoked as sh
**Goal:** predict behaviour of `#!/bin/sh` on systems where sh is bash.
```bash
ls -l /bin/sh                       # which shell is sh here?
bash --posix script.sh              # or: set -o posix inside the script
echo "$SHELLOPTS"                   # lists enabled set -o options; posix appears when enabled
POSIXLY_CORRECT=1 bash -c '...'     # variable in the environment at startup enables POSIX mode
```
- Startup when invoked with the name `sh`: as an interactive login shell (or non-interactive with `--login`) it reads `/etc/profile` then `~/.profile` (`--noprofile` inhibits this). As an interactive non-login shell it expands `ENV` and reads that file. A non-interactive `sh` reads no other startup files, and `--rcfile` has no effect. `~/.bashrc` is not read (`--norc` is on by default as `sh`).
- Invoked as `sh`, bash enters POSIX mode after reading the startup files. `--posix` or `set -o posix` enables it at other times, and `POSIXLY_CORRECT` in the environment at startup enables it before the startup files are read.
- Some things the manual lists as changed in POSIX mode: `POSIXLY_CORRECT` is set; alias expansion is always enabled, even in non-interactive shells; function names may not be the same as a POSIX special builtin; special builtins are found before functions; redirection words are not word-split; `!` does not start history expansion inside double quotes; the `time` reserved word can stand alone; `inherit_errexit`, `shift_verbose` and `interactive_comments` are set; the default history file is `~/.sh_history`.
- In POSIX mode a non-interactive shell exits on: an error status from a POSIX special builtin (such as incorrect options or redirection errors), a variable assignment error with no command name, `.` not finding its file, a syntax error in a sourced file or an `eval` string, and `export`, `readonly` or `unset` given an invalid identifier.
- With `xpg_echo` enabled in POSIX mode, `echo` does not interpret its arguments as options and converts escape sequences.
- The manual notes some POSIX behaviour bash does not implement even in POSIX mode, for example byte-oriented word splitting of `IFS`.
- Testing a script against another shell is up to that shell's own documentation; this skill does not claim which bashisms fail elsewhere.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 6.2 Bash Startup Files (invoked with name sh), the BASHOPTS/SHELLOPTS/POSIXLY_CORRECT variable entries, and section 6.11.2 Bash POSIX Mode (the full list from "When invoked as sh" through the exit-on-error and echo items). Trims and corrections: removed the draft's claims about dash (arrays, `[[ ]]`, `local -r`, `$'..'`, `${var//x/y}` failing), checkbashisms and the `ls -l /bin/sh` self-check, the "process substitution is not guaranteed portable" sentence (not in the manual), and the `$BASHOPTS` mention (it lists shopt options, not POSIX mode). "echo unchanged unless xpg_echo" became the manual's actual xpg_echo wording.
