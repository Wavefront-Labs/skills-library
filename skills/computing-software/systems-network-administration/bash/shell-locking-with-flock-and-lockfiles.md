---
id: computing-software.systems-network-administration.bash.shell-locking-with-flock-and-lockfiles
name: shell-locking-with-flock-and-lockfiles
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-flock, lockfile, single-instance, cron-overlap]
level: advanced
status: docs-checked
description: "Prevent overlapping script runs with flock: wrapper and file-descriptor forms, nonblocking and timeout options, exit codes and NFS caveats."
sources:
  - https://man7.org/linux/man-pages/man1/flock.1.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locking with flock

- `flock` (util-linux) manages flock(2) locks from scripts. Three forms: `flock [options] file|directory command [args]`, `flock [options] file|directory -c command`, and `flock [options] number` (an open file descriptor).
- Inside a script (the man page's idiom):
  ```bash
  (
    flock -n 9 || exit 1
    # ... commands executed under lock ...
  ) 9>/var/lock/mylockfile
  ```
  The open mode does not matter to flock; `>` or `>>` creates the file if missing (write permission needed), `<` requires an existing file and only read permission.
- Without a subshell: `exec 4<>/var/lock/mylockfile; flock -n 4` locks a descriptor the shell opened, with no extra process.
- Wrapper form for cron: `flock -n /var/lock/myjob.lock myjob.sh`. The lock file or directory is created if it does not exist; the exit status is the child's.
- By default flock waits for the lock. `-n` fails instead of waiting; `-w seconds` fails after the timeout (decimals allowed; 0 means nonblocking). In both cases the failure exit status is 1 unless `-E number` (0-255) sets another.
- `-x` / `-e` exclusive (the default, a write lock); `-s` shared (a read lock).
- A lock is dropped automatically when the file is closed. Use `-u` to drop it, or `-o` / `--close` to close the lock descriptor before running the command, when the command may leave a background child that should not hold the lock.
- `-F` / `--no-fork` replaces flock with the command, which keeps the lock; it cannot be combined with `--close`.
- Self-locking boilerplate from the man page, at the top of a script: `[ "${FLOCKER}" != "$0" ] && exec env FLOCKER="$0" flock -en "$0" "$0" "$@" || :`.
- Limits: flock does not detect deadlock; NFS and CIFS have limited flock(2) support and flock may always fail there, depending on mount options.
- Never implement locks with `[ -f lock ] || touch lock`: the test and create are two steps. Use flock, which takes the lock in one operation.

## Checked
Checked 2026-11-08 against flock(1) (forms, options, exit status, notes, examples) and the Bash manual (`exec` redirections used by the descriptor form). Removed: claims about the kernel releasing locks on crash beyond "dropped when the file is closed", the mkdir-lock fallback with PID checks, the macOS `flock` / shlock advice and the NFS fcntl-emulation claim, none of which the cited pages state.

Method: docs-only read of cited pages, 2026-11-08
