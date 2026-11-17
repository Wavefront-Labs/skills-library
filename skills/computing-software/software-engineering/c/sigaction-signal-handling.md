---
id: computing-software.software-engineering.c.sigaction-signal-handling
name: sigaction-signal-handling
category: computing-software
field: software-engineering
product: c
tags: [c, sigaction, signal-handler, async-signal-safe, sigatomic, sigprocmask]
level: advanced
status: docs-checked
description: "Install robust signal handlers with sigaction and keep them async-signal-safe."
sources: ["https://man7.org/linux/man-pages/man2/sigaction.2.html", "https://man7.org/linux/man-pages/man7/signal-safety.7.html", "https://man7.org/linux/man-pages/man2/signalfd.2.html", "https://man7.org/linux/man-pages/man3/sigwait.3.html", "https://en.cppreference.com/w/c/program/signal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sigaction signal handling

Goal: handle SIGINT/SIGTERM/SIGCHLD without races or undefined behaviour.

- Use `sigaction`, not `signal` (portable semantics): `struct sigaction sa = {0}; sa.sa_handler = on_term; sigemptyset(&sa.sa_mask); sa.sa_flags = SA_RESTART; sigaction(SIGTERM, &sa, NULL);`
- A handler may only call async-signal-safe functions (the list in `signal-safety(7)`; `write`, `_exit`, `sigaction`, but NOT `printf`, `malloc`, `free`). Otherwise the common safe pattern: set a `volatile sig_atomic_t` flag and handle it in the main loop.
- Self-pipe trick or `signalfd` (Linux) turns signals into readable events for `poll`; `sigwait` in a dedicated thread with signals blocked is the clean multithreaded design.
- Save and restore `errno` in handlers that call functions which may set it.
- `SA_RESTART` restarts most slow syscalls; otherwise handle `EINTR` by retrying.
- `SIGKILL` and `SIGSTOP` cannot be caught. Use `sigprocmask`/`pthread_sigmask` to block around critical sections.

Verify: send the signal with `kill -TERM PID` during a blocking call and confirm clean shutdown with no deadlock.

## Checked

- Date: 2026-11-02
- Confirmed in man7: sigaction(2) `sa_flags`, `SA_RESTART`, SIGKILL/SIGSTOP cannot be caught; signal-safety(7) (async-signal-safe list includes `write`, `_exit`, `sigaction`; errno must be saved and restored in handlers); signalfd(2) and sigwait(3) (signal must be blocked first); cppreference signal page lists `sig_atomic_t`. Nothing removed.
Method: documentation only; no commands were run.
