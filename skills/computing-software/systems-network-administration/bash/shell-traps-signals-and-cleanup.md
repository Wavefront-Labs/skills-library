---
id: computing-software.systems-network-administration.bash.shell-traps-signals-and-cleanup
name: shell-traps-signals-and-cleanup
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-trap, signals, exit-trap, cleanup, sigint-sigterm]
level: advanced
status: docs-checked
description: "Use trap for cleanup on EXIT, handle INT/TERM correctly and avoid common signal pitfalls."
sources: ["https://www.gnu.org/software/bash/manual/bash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traps and cleanup

- `trap 'rm -rf "$tmp"' EXIT` runs when the shell exits (`0` is accepted as a synonym for `EXIT`); set it right after creating the resource. `trap - EXIT` resets it to the disposition at shell start.
- Signal handlers: `trap 'echo interrupted >&2; exit 130' INT TERM` (130 is 128+2 for SIGINT). A plain `trap '' INT` ignores the signal in the shell and in the commands it invokes; in a non-interactive shell, signals ignored on entry cannot be trapped or reset.
- `ERR` trap (bash) fires when a pipeline, list or compound command returns non-zero, with the same exceptions as `errexit`. It is not inherited by functions, command substitutions or subshells unless `set -E` (`errtrace`) is on. Diagnostics example: `trap 'echo "line $LINENO: $BASH_COMMAND" >&2' ERR`.
- Single quote the trap string so variables expand when it fires; use a function for anything non-trivial. To append to an existing trap, read it with `trap -p EXIT` (the output is reusable as shell input) and re-set the combined action, because a new action for a signal replaces the old one.
- If bash is waiting for a foreground command and receives a trapped signal, it does not run the trap until that command completes. If it is waiting with the `wait` builtin, `wait` returns at once with a status above 128 and then the trap runs, so run long children in the background and `wait` to react promptly.
- Trapped signals that are not ignored are reset to their original values in a subshell.
- Non-interactive bash does not enable job control by default, so a keyboard Ctrl-C (SIGINT) reaches the whole terminal process group, including the script and its foreground child.

Verify: send SIGTERM to a running script with `kill -TERM <pid>` and confirm temp files are removed.

## Checked
2026-11-08. Confirmed in the GNU Bash manual: trap builtin (EXIT/0, reset with -, empty action ignores, -p, ERR conditions, subshell reset), errtrace, Signals section (trap deferred until foreground command ends, wait returns above 128, job control and process groups). Removed (not stated in the manual): that EXIT runs after a fatal signal, that SIGKILL cannot be caught, the `kill 0` / `kill -- -$$` process-group advice, and the dash/POSIX sh trap-naming note.
Method: documentation only; no commands were run.
