---
id: computing-software.systems-network-administration.bash.rcfile-option
name: rcfile-option
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, rcfile-option, bash-norc, shell-scripting]
level: advanced
status: docs-checked
description: "Start bash with --rcfile, --norc and --noprofile for clean, reproducible shells in tests, containers and support sessions."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# --rcfile and --norc
**Goal:** control which startup files load.
```bash
bash --norc                           # interactive, skip ~/.bashrc
bash --noprofile --norc               # skip login-shell files and ~/.bashrc
bash --rcfile /path/test.rc -i        # use a custom file instead of ~/.bashrc
env -i HOME="$HOME" TERM="$TERM" bash --noprofile --norc   # also empty environment
BASH_ENV=/path/env.sh bash script.sh  # non-interactive: file sourced first
bash -l -c 'echo $PATH'               # login shell reproduction
```
- `--rcfile file` (same as `--init-file file`) runs commands from file instead of `~/.bashrc` in an interactive shell. `--norc` skips `~/.bashrc` in an interactive shell and is on by default when the shell is invoked as `sh`.
- `--noprofile` skips `/etc/profile` and `~/.bash_profile`, `~/.bash_login` and `~/.profile` when bash is a login shell.
- A non-interactive shell does not read `~/.bashrc`; it expands `BASH_ENV` and sources that file (as if `if [ -n "$BASH_ENV" ]; then . "$BASH_ENV"; fi` ran, without searching `PATH`).
- `-i` forces the shell to run interactively. `-l` / `--login` makes the shell act as a login shell, and when non-interactive it reads the login startup files.
- Invoked with the name `sh`, bash reads the file named by `ENV` when interactive, and `--rcfile` has no effect.
- `env -i` is an `env` option (clears the environment) used here to remove local environment variables; see the env manual page.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 6.1 Invoking Bash (--init-file/--rcfile, --noprofile, --norc, -c, -i, -l) and section 6.2 Bash Startup Files (login, interactive non-login, non-interactive, invoked as sh). Trims: removed the sentence "scripts ignore it" in favour of the documented non-interactive BASH_ENV behaviour, the "bug reports and CI" advice and the `bash --norc -ic 'alias'` self-check (not in the manual). Searched the manual for the option text and read the startup-files section; did not read the whole page.
