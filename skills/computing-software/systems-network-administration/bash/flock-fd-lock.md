---
id: computing-software.systems-network-administration.bash.flock-fd-lock
name: flock-fd-lock
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, flock-fd-lock, flock-n, shell-scripting]
level: advanced
status: docs-checked
description: "Take an exclusive flock on an open bash file descriptor for the life of a script, with non-blocking and timeout modes."
sources:
  - https://man7.org/linux/man-pages/man1/flock.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flock on an open descriptor
**Goal:** one running instance, lock released automatically on exit.
```bash
exec 9> /var/lock/myjob.lock || exit 1
flock -n 9 || { echo "already running" >&2; exit 0; }     # non-blocking
# flock -w 30 9 || exit 1                                  # wait up to 30s
...work...
# lock drops when the script exits (fd closes)
flock -n /var/lock/myjob.lock -c 'command'                 # one-liner form
( flock -x 9; critical ) 9>/var/lock/x.lock                # scoped to a subshell
```
- The lock is dropped automatically when the file is closed. `flock -u` drops it explicitly, which matters if the locked group may have forked a background process that should not hold it.
- In the command form (`flock file cmd`), `-o` closes the lock's file descriptor before running the command so a child it spawns does not hold the lock.
- `-n` fails instead of waiting and `-w seconds` fails after a timeout; both exit 1 unless `-E number` sets another status (0-255). By default flock waits and takes an exclusive lock (`-x`; `-s` is shared).
- With the fd form the open mode does not matter to flock: `>` or `>>` creates the lock file if missing (write permission needed); `<` needs an existing, readable file.
- flock does not detect deadlock. NFS and CIFS have a limited flock implementation and it may always fail there, so keep lock files on a local filesystem.
- Self-check: a second invocation prints "already running".

## Checked
2026-11-08. Confirmed against the flock(1) man page: the three invocation forms, `-n`, `-w`, `-E`, `-o`, `-u`, `-x`/`-s`, the fd examples, open-mode note, exit status and the NFS/CIFS and deadlock notes. Removed the claims that flock is util-linux software, that macOS lacks it, the `9>&-` and "children keep it after the parent exits" wording, and the `mkdir` lock suggestion; the page does not cover them.
Method: documentation only; no commands were run.
