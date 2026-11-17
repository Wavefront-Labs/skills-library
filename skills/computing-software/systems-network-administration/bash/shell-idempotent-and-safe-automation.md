---
id: computing-software.systems-network-administration.bash.shell-idempotent-and-safe-automation
name: shell-idempotent-and-safe-automation
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-idempotent-scripts, dry-run, confirm-prompts, destructive-commands, rollback]
level: advanced
status: docs-checked
description: "Write automation scripts that can be re-run safely: idempotent steps, dry-run, ${var:?} guards, set -u and atomic switch-over."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html
  - https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent scripts

- Make each step check-then-act or declarative, so re-running produces no change and exits 0. GNU `ln -sfn` is one such step: `-f` replaces an existing destination, `-s` makes a symbolic link, and `-n` (`--no-dereference`) treats an existing symlink to a directory as a file; the coreutils manual says that, unless `--backup` is used, there is no brief moment when the destination does not exist.
- `--dry-run` support: wrap mutating commands in a `run()` function that prints instead of executing when `DRY_RUN=1`.
- Guard destructive operations with `${dir:?}`: if `dir` is null or unset, the shell writes a message to standard error and, if non-interactive, exits with a non-zero status, so `rm -rf -- "${dir:?}/"` cannot become `rm -rf -- /`.
- `set -u` (same as `set -o nounset`) treats unset variables and parameters (other than `@` and `*`) as an error during parameter expansion and makes a non-interactive shell exit.
- Require confirmation or an explicit `--yes` flag for destructive actions; refuse to prompt when not on a terminal unless forced.
- Order and recover: do the slow or fallible work in a temporary location, then switch with a rename or symlink swap (`mv -T` for the symlink case; `mv` falls back to copy-then-delete across file systems, `mv --no-copy` fails instead). Keep the previous version for rollback.
- Fail fast on missing prerequisites: `command -v tool >/dev/null || die` (`command -v` prints a single word naming the command or file and returns non-zero if it is not found).
- Move to a configuration-management tool once state spans many hosts.

## Checked
2026-11-09. Confirmed in the bash manual (`${parameter:?word}`, `set -u`, `command -v`) and the coreutils ln and mv pages (`-f`, `-s`, `-n`, no-gap statement, copy fallback, `--no-copy`, `-T`). Removed: `mkdir -p`, `install -m 0644 -D`, `grep -qxF` append idiom, `id user || useradd`, `systemctl enable --now`, and the Ansible and Terraform names, which the cited pages do not cover.
Method: documentation only; no commands were run.
