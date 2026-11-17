---
id: computing-software.cryptography-implementation.libsodium.sodium-malloc-guarded-allocations
name: sodium-malloc-guarded-allocations
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, sodium-helpers, sodium-malloc, sodium-mprotect-noaccess, guard-pages, canary, sodium-mlock, secure-memory, rlimit-memlock]
level: advanced
status: docs-checked
description: "Hold keys in sodium_malloc guarded allocations: guard pages and canary, mprotect_noaccess/readonly between uses, cost per allocation, and mlock limits."
sources: ["https://doc.libsodium.org/helpers/memory_management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sodium_malloc guarded allocations

`sodium_malloc(n)` returns memory that is:
- placed at the end of a page, immediately before a guard page (overflow terminates the process),
- preceded by a canary (checked at `sodium_free`) and, where supported, a guard page,
- `mlock`ed where possible and excluded from core dumps where supported
  (`MAP_NOCORE` or `MADV_DONTDUMP`),
- filled with 0xdb so uninitialised use is visible,
- zeroed by `sodium_free` before release.

```c
unsigned char *key = sodium_malloc(crypto_secretbox_KEYBYTES);
if (!key) abort();
crypto_secretbox_keygen(key);
sodium_mprotect_noaccess(key);         /* any access now segfaults */
/* ... when needed: */
sodium_mprotect_readonly(key);
crypto_secretbox_easy(c, m, mlen, nonce, key);
sodium_mprotect_noaccess(key);
/* shutdown */
sodium_free(key);
```

## Costs and limits

- The docs say these are not general-purpose allocators: they are slower than `malloc` and need 3 or 4 extra pages of virtual memory. `sodium_init()` must be called first. Use them for a handful of
  long-lived secrets (master keys, identity keys), not per-message buffers.
- `mlock` is subject to limits such as `RLIMIT_MEMLOCK` (raising it may need `CAP_IPC_LOCK`). If `mlock` is unsupported or fails, `sodium_malloc` still returns the memory, unlocked; call `sodium_mlock()` and check its `-1` return if you must rely on locking.
- `sodium_allocarray(count, size)` gives the same guarantees and guards against `count * size` overflow; a zero-byte allocation is valid.
- The returned pointer is not aligned if the size is not a multiple of the required alignment, so for packed or variable-length structures round the size up (the docs say all libsodium structures can safely be allocated this way).
- `sodium_mprotect_*` apply to regions from `sodium_malloc` or `sodium_allocarray`.

## For buffers on the stack or heap you do not control

Use `sodium_mlock(ptr, len)` / `sodium_munlock` (it zeroes the region before unlocking) and
`sodium_memzero` after use. Per the docs, `mlock` does not protect the stack or CPU registers, so secrets can still be copied there; `sodium_stackzero()` can wipe the stack after sensitive operations, and the docs call locking defence in depth, with encrypted or disabled swap as the stronger measure.

## Verify

- [ ] Long-lived keys allocated with `sodium_malloc` and freed with `sodium_free`.
- [ ] Locking verified where it matters (`sodium_mlock` returns 0), since `sodium_malloc` does not fail when `mlock` does.
- [ ] Test: writing past the allocation crashes in a debug build (guard page works).

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed against the memory management page: guard page after the region at the end of a page, canary checked in sodium_free, extra guard page before it where supported, 0xdb fill, mlock with MAP_NOCORE or MADV_DONTDUMP, mlock failure not failing the allocation, 3 or 4 extra pages and slower than malloc, sodium_init required, alignment note, sodium_allocarray, sodium_mlock and munlock behaviour, stack and register caveat, sodium_stackzero. The old skill wrongly implied sodium_malloc returns NULL when the lock limit is reached.

Method: documentation only; no commands were run.
