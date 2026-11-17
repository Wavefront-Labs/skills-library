---
id: computing-software.software-engineering.c.errno-and-return-code-conventions
name: errno-and-return-code-conventions
category: computing-software
field: software-engineering
product: c
tags: [c, c-error-handling, errno, return-codes, perror, strerror, error-propagation]
level: practitioner
status: docs-checked
description: "Use errno and return codes consistently: save errno, never test it without a failing call, and propagate errors."
sources: ["https://man7.org/linux/man-pages/man3/errno.3.html", "https://man7.org/linux/man-pages/man3/strerror.3.html", "https://man7.org/linux/man-pages/man4/full.4.html", "https://en.cppreference.com/w/c/error/errno"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Errno and return code conventions

Goal: errors that are detectable, diagnosable and not clobbered.

- `errno` is meaningful only immediately after a call that documents setting it and reported failure; successful calls may change it. Set `errno = 0` before calls like `strtol` whose only error signal is errno.
- Save it before cleanup that may overwrite it: `int e = errno; free(p); errno = e;`.
- Choose one convention per library: return 0/-1 and `errno`; or return negative error codes (`-ENOMEM`); or return an enum. Do not mix `bool`, `-1` and `NULL` for the same kind of failure.
- Provide an `foo_strerror(int)` for library error enums.
- glibc documents `strerror` as MT-Safe; when you need a caller-supplied buffer use `strerror_r` (the XSI and GNU variants differ in return type).
- Print diagnostics to `stderr`, with the function and the argument that failed (`perror("open")` adds the errno text).
- Check return values of `close`, `fclose`, `fsync` and `write`; a `write` may transfer fewer bytes than requested.

Verify: force each failure path (bad path, ENOSPC via `/dev/full`, ENOMEM via wrapper) in tests.

## Checked

- Date: 2026-11-02
- Confirmed in man7: errno is thread-local; some functions can only be checked by setting errno to 0 first; `strerror` is MT-Safe in glibc; `strerror_r` has XSI and GNU variants with different signatures; `/dev/full` writes fail with ENOSPC; write(2) may write fewer bytes than requested. Removed: the claim that `strerror` may be unsafe in threads and the `strerror_s` mention.
Method: documentation only; no commands were run.
