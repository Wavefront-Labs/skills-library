---
id: computing-software.software-engineering.c.fork-exec-waitpid
name: fork-exec-waitpid
category: computing-software
field: software-engineering
product: c
tags: [c, c-posix-processes, fork-exec, waitpid, zombie-process, posix-spawn, close-on-exec]
level: practitioner
status: docs-checked
description: "Spawn child processes correctly with fork/exec, reap them with waitpid and avoid fd leaks and zombies."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://man7.org/linux/man-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fork exec waitpid

Goal: run subprocesses without leaks, zombies or surprises.

- `pid_t p = fork();` returns 0 in the child, the child PID in the parent, -1 on error. In the child, call `execvp(argv[0], argv)`; if it returns, report with `perror` and leave the child with `_exit` (not `exit`, which calls atexit handlers and flushes open stdio streams per exit(3)).
- Parent: `waitpid(p, &status, 0)`; decode with `WIFEXITED`, `WEXITSTATUS`, `WIFSIGNALED`, `WTERMSIG`. Unreaped children remain zombies; handle `SIGCHLD` or wait in a loop (`waitpid(-1, &st, WNOHANG)`).
- File descriptors are inherited by default. Open with `O_CLOEXEC` / `SOCK_CLOEXEC` or set `FD_CLOEXEC` so children do not inherit secrets and sockets.
- In multithreaded programs only async-signal-safe functions are safe between `fork` and `exec`; prefer `posix_spawn` (or `posix_spawnp`) which avoids most pitfalls.
- Flush stdio before `fork` so buffered output is not duplicated in the child.

Verify: run a loop spawning 1000 children then check `ls /proc/self/fd | wc -l` and `ps` for zombies.

## Checked

2026-11-02. Confirmed in fork(2), _exit(2), exit(3), waitpid(2), posix_spawn(3), socket(2), open(2): fork return values, async-signal-safe restriction in a multithreaded child, `WIFEXITED`/`WIFSIGNALED`/`WTERMSIG`, `WNOHANG`, `O_CLOEXEC`/`SOCK_CLOEXEC`/`FD_CLOEXEC`, `posix_spawnp`, exit(3) flushing stdio. Removed: the `_exit(127)` code and the `system()` bullet.

Method: documentation only; no commands were run.
