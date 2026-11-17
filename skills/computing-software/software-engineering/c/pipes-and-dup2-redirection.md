---
id: computing-software.software-engineering.c.pipes-and-dup2-redirection
name: pipes-and-dup2-redirection
category: computing-software
field: software-engineering
product: c
tags: [c, dup2, pipe, redirection, popen, shell-pipeline]
level: practitioner
status: docs-checked
description: "Connect processes with pipe and dup2, close unused ends and avoid deadlocks."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://man7.org/linux/man-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipes and dup2 redirection

Goal: implement `cmd1 | cmd2` or capture a child's output safely.

- `int fd[2]; pipe(fd);` gives `fd[0]` read end, `fd[1]` write end. After `fork`, each side closes the end it does not use; a reader only sees EOF when ALL write ends are closed, so a forgotten copy hangs the reader.
- In the child: `dup2(fd[1], STDOUT_FILENO); close(fd[0]); close(fd[1]); execvp(...)`.
- Capture both stdout and stderr: use separate pipes read via `poll`, or redirect stderr to the same pipe; reading one fully before the other can deadlock when the other fills its (16 pages, 65,536 bytes with 4 KiB pages, on modern Linux per pipe(7); do not rely on it) buffer.
- Writing to a pipe with no reader raises `SIGPIPE`; ignore it (`signal(SIGPIPE, SIG_IGN)`) and handle `EPIPE`.
- Short reads/writes: loop until done; see the socket partial I/O skill.

Verify: implement `ls | wc -l` and confirm it terminates (no hang) and the count matches the shell.

## Checked

2026-11-02. Confirmed in pipe(7), pipe(2), send(2): EOF only after all write ends close, pipe capacity, SIGPIPE on a pipe without readers. Removed: the `popen` bullet (not fetched).

Method: documentation only; no commands were run.
