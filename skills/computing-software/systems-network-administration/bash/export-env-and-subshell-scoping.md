---
id: computing-software.systems-network-administration.bash.export-env-and-subshell-scoping
name: export-env-and-subshell-scoping
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, env-command, subshell, export, environment-variables, env-i, child-process, variable-scope]
level: practitioner
status: verified
description: "Understand what children inherit: shell vs environment variables, export and env, VAR=x cmd one-shots, env -i clean runs, subshell vs grouped commands, and sourcing vs executing."
sources:
  - https://www.gnu.org/software/bash/manual/html_node/Environment.html
  - https://www.gnu.org/software/bash/manual/html_node/Command-Grouping.html
  - https://man7.org/linux/man-pages/man1/env.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# export, env and subshells

## Shell variable vs environment variable
```bash
FOO=1            # shell variable: visible to this shell only
export FOO       # now in the environment of every child process
BAR=2 ./app      # BAR set only for this one command (not in the current shell afterwards)
env | grep FOO ; declare -px          # exported vars
export -n FOO ; unset FOO              # un-export / remove
```
A child can never change the parent's environment — that's why `cd` in a script doesn't move your shell and
why env files are **sourced** (`. ./env.sh` / `source`) not executed.

## env
```bash
env -i PATH=/usr/bin:/bin HOME=/tmp ./script.sh     # clean environment: reproduce cron/systemd conditions
env -u HTTP_PROXY curl ...                            # drop one var
env --chdir=/srv/app -S 'python3 -u' app.py           # --chdir: coreutils 8.28+; -S (split args): 8.30+
#!/usr/bin/env -S python3 -u                          # portable shebang with args
```
Check a running process's initial environment (Linux): `tr '\0' '\n' < /proc/<pid>/environ` (NUL-delimited; shows the environment at exec time, later `putenv` changes are not reflected - proc_pid_environ(5)).

## Subshell vs group
| Syntax | Runs in | Variable changes persist? |
|---|---|---|
| `( cd /tmp; x=1 )` | subshell | no — handy for temporary cd/umask/set options |
| `{ cd /tmp; x=1; }` | current shell | yes (note spaces and final `;`) |
| `$(...)`, pipelines, `&` | subshells | no |
`BASH_SUBSHELL` shows nesting depth.

## Gotchas
- `export VAR=$(cmd)` masks `cmd`'s exit status; split the lines under `set -e`.
- sudo resets the environment by default (`env_reset`); `sudo -E` (needs the `setenv` flag or `SETENV` tag in sudoers) or `env_keep` pass variables through (sudoers manual).
- systemd units get their environment from `Environment=` / `EnvironmentFile=` (systemd.exec); do not assume your shell profile is applied to a service.

## Verify
- [ ] `env -i` run of the script behaves the same as from your interactive shell (no hidden env dependencies).
