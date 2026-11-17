---
id: computing-software.cryptography-implementation.secure-implementation.secure-memory-and-key-zeroization
name: secure-memory-and-key-zeroization
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, zeroization, memory-safety, mlock, virtuallock, swap-prevention, core-dump, guard-pages, sodium-memzero, explicit-bzero, secure-allocator, key-lifetime, garbage-collection]
level: advanced
status: docs-checked
description: "Making key material disappear from memory: why plain memset gets optimized away, libsodium zeroing, locking memory against swap, core dumps and guard pages."
sources: ["https://doc.libsodium.org/memory_management", "https://man7.org/linux/man-pages/man2/mlock.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure memory handling and key zeroization

Key material in memory must be destroyed, kept out of swap and kept out of
crash dumps; each is a distinct failure mode with its own fix.

## Why `memset(key, 0, len)` is not reliable

The libsodium documentation warns that `memset()` and hand-written code can be silently stripped out by an
optimizing compiler or the linker. Use a call documented to survive optimization:
- **libsodium:** `sodium_memzero(pnt, len)` zeroes even when optimizations are applied; prefer it over rolling your
  own. `sodium_munlock` also zeroes the memory before making the pages swappable again.
- Otherwise use your platform's documented secure-zeroing primitive; never rely on a plain `memset` or hand-written
  loop.

## Garbage-collected languages: you don't control when memory is freed

In garbage-collected runtimes you cannot be sure an earlier copy of a key is gone, so prefer mutable buffers over
immutable strings, clear them when done, and treat zeroization as best-effort (not checked against vendor docs here). If this residual
  risk is unacceptable for your threat model, the key material needs to
  live in a non-GC component (a native extension, an HSM, a separate
  process using the mlock techniques below) rather than the managed
  runtime.

## Preventing swap and core dumps from leaking key material

Zeroing memory while it's live doesn't help if the OS already wrote a
plaintext copy to swap or a crash dump before you got to zero it:
- **`mlock()` (POSIX) or `VirtualLock()` (Windows)** pin pages in RAM so they are not swapped; libsodium's
  `sodium_mlock()` wraps both. Many systems limit the memory a process may lock (on Linux `RLIMIT_MEMLOCK`, unless the
  process has `CAP_IPC_LOCK`): raise the limit if needed and check the return value (`sodium_mlock()` returns -1 when a
  limit is reached). Where supported it also advises the kernel to exclude the locked memory from core dumps.
- **Core dump prevention:** libsodium advises disabling core dumps for crypto code outside development, with `ulimit`
  or `setrlimit(RLIMIT_CORE, &(struct rlimit){0, 0})`, and disabling kernel crash dumps where the OS allows.
- **Guard pages:** some hardened allocators (libsodium's `sodium_malloc`)
  place inaccessible guard pages around a sensitive allocation, so a
  buffer-overread/overwrite adjacent to the key buffer crashes
  immediately (loud failure) instead of silently reading/corrupting
  neighboring key material — prefer this allocator for standalone
  long-lived key buffers over a plain `malloc`.

## Verify

- [ ] All key-zeroization calls use a platform/library primitive documented
      to resist compiler dead-code elimination — no plain `memset`/manual
      loops relied upon.
- [ ] Long-lived key buffers are locked, with the lock limit checked, not assumed.
- [ ] Core dumps are disabled for processes holding live key material, or
      dump storage is access-controlled and encrypted if dumps are
      required.
- [ ] Standalone sensitive allocations use a guard-paged allocator where
      available.

## Checked

2026-10-31. Confirmed in the libsodium memory management page (memset and hand-written code can be stripped; sodium_memzero; sodium_mlock wraps mlock and VirtualLock and returns -1 at the limit; madvise core-dump exclusion; sodium_munlock zeroes; disable core dumps with ulimit or setrlimit; guarded heap allocations) and mlock(2) (RLIMIT_MEMLOCK, CAP_IPC_LOCK). Removed: CERT MSC06-C, per-platform zeroing function names, default limit sizes, systemd setting, and all language-specific GC details.

Method: documentation only; no commands were run.
