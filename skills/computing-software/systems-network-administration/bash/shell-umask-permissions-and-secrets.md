---
id: computing-software.systems-network-administration.bash.shell-umask-permissions-and-secrets
name: shell-umask-permissions-and-secrets
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-umask, file-permissions, secrets-in-scripts, process-list-leaks, secure-defaults]
level: advanced
status: docs-checked
description: "Handle permissions and secrets in bash scripts: umask, mktemp modes, silent reads, set -x, unset and PATH."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/coreutils/manual/html_node/mktemp-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions and secrets

- `umask 077` before creating sensitive files. The bash manual: if the mode begins with a digit it is octal; each digit of the umask is subtracted from 7, so `022` gives permissions of 755; `umask` with no mode prints the current mask, and `umask -S` prints it symbolically.
- `mktemp` creates files readable and writable only by the current user, and `mktemp -d` creates directories accessible only to that user (both reduced further by a stricter umask). The coreutils manual advises it over names built from `$$`, which are predictable and open to symlink races.
- `read -s` is silent mode: when input comes from a terminal, characters are not echoed. Use `read -rs` for password prompts.
- `set -x` prints a trace of expanded commands to standard error, so turn it off (`set +x`) around code that handles secrets.
- Pass secrets via a mode-restricted file, standard input, or an inherited file descriptor rather than command-line arguments or exported variables; exported variables are passed to every subsequently executed command (bash `export`). Remove variables you no longer need with `unset`, which also removes them from the environment passed to later commands; readonly variables cannot be unset.
- Do not source or `eval` files that other users can write; check ownership and mode first.
- Pin `PATH` to a known list in privileged scripts and use absolute paths for critical tools.- Strip secrets from logs and error messages, and rotate any credential that reached shell history or a log.

## Checked
2026-11-09. Confirmed in the bash manual (`umask` semantics, `read -s`, `set -x`, `export`, `unset`) and the coreutils mktemp page (permissions, `$$` warning). Removed: `install -m 0600`, `stat -c %a` / `stat -f %Lp`, `/proc/<pid>/cmdline` and `/proc/<pid>/environ` visibility, `curl -K -` and `mysql --defaults-extra-file` examples, the claim that setuid shell scripts are ignored on Linux, the process-listing visibility claim, the empty-PATH-entry remark, and the POSIX root URL (a stub page).
Method: documentation only; no commands were run.
