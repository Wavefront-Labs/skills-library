---
id: computing-software.cryptography-implementation.secure-implementation.madv-dontdump-and-madv-wipeonfork
name: madv-dontdump-and-madv-wipeonfork
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, madv-wipeonfork, madv-dontdump, madvise, secure-memory, fork-safety, linux]
level: advanced
status: docs-checked
description: "Protect key memory with madvise flags: MADV_DONTDUMP to keep secrets out of core dumps and MADV_WIPEONFORK so forked children do not inherit keys or RNG state."
sources: ["https://man7.org/linux/man-pages/man2/madvise.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MADV_DONTDUMP and MADV_WIPEONFORK

## Usage
```c
size_t len = 4096;                                   /* page-aligned */
void *p = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
madvise(p, len, MADV_DONTDUMP);                       /* Linux 3.4+: excluded from core dumps */
madvise(p, len, MADV_WIPEONFORK);                     /* Linux 4.14+: child sees zero-filled pages */
```

## What each does
- `MADV_DONTDUMP` (since Linux 3.4): region omitted from core dumps; this takes precedence over the
  `/proc/pid/coredump_filter` mask. `MADV_DODUMP` undoes it.
- `MADV_WIPEONFORK` (since Linux 4.14): after `fork()`, the child sees zero-filled memory in the range. The man page
  gives forking servers as the use case, to keep per-process sensitive data such as PRNG seeds and cryptographic
  secrets from being handed to children. The setting stays in the child and is cleared by `execve()`. Use for:
  - per-process DRBG state, so a forked child cannot repeat the parent's random output;
  - session keys that children must not inherit.
  Code must detect zeroed state and reseed/reinitialise (e.g. a non-zero magic marker in the page).
- `MADV_KEEPONFORK` (since Linux 4.14) undoes `MADV_WIPEONFORK`.

## Notes
- `MADV_WIPEONFORK` applies only to private anonymous pages (`EINVAL` otherwise); advice addresses must be
  page-aligned, so memory from `malloc` is unsuitable unless you control alignment.
- Linux only. On other systems use that OS's equivalent or fork detection (for example a PID change, with care for
  PID reuse); check its documentation.

## Verify
- [ ] Test: fork after generating random bytes; child and parent next outputs differ; core dump lacks canary.

## Checked

2026-10-31. Confirmed in the man7.org madvise(2) page: `MADV_DONTDUMP` and `MADV_DODUMP` since Linux 3.4 (precedence
over `/proc/pid/coredump_filter`), `MADV_WIPEONFORK` and `MADV_KEEPONFORK` since Linux 4.14, WIPEONFORK limited to
private anonymous pages with EINVAL otherwise, setting cleared on execve. Removed (no source read): the claim that
`/proc/pid/mem` and ptrace are unaffected, the FreeBSD/OpenBSD `minherit(INHERIT_ZERO)` and macOS statements, the
`pthread_atfork` suggestion, and "OpenSSL/BoringSSL/libsodium apply these internally" (the OpenSSL `rand_lib.c`
page fetched shows no madvise call), and the `mlock` line.
Method: documentation only; no commands were run.
