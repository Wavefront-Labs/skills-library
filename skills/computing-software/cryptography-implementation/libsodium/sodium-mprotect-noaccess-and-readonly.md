---
id: computing-software.cryptography-implementation.libsodium.sodium-mprotect-noaccess-and-readonly
name: sodium-mprotect-noaccess-and-readonly
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, sodium-mprotect, sodium-malloc, secure-memory, libsodium, mprotect]
level: advanced
status: docs-checked
description: "Lock down sodium_malloc'd secrets with sodium_mprotect_noaccess, readonly and readwrite: access windows, page granularity, crash behaviour and platform caveats."
sources: ["https://doc.libsodium.org/helpers/memory_management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sodium_mprotect_noaccess and readonly

Memory from `sodium_malloc` sits on its own pages with guard pages around it, so it can be page-protected.

## Pattern
```c
unsigned char *key = sodium_malloc(32);
crypto_secretbox_keygen(key);
sodium_mprotect_noaccess(key);           /* any access now segfaults */

/* when needed */
sodium_mprotect_readonly(key);
crypto_secretbox_easy(c, m, mlen, n, key);
sodium_mprotect_noaccess(key);

sodium_free(key);                        /* works even if readonly; zeroes the memory */
```

## Benefits
- With `noaccess` the data is preserved but cannot be read or written, so a stray access terminates the process instead of leaking it.
- With `readonly`, an attempt to modify the data terminates the process.
- `sodium_mprotect_readwrite(ptr)` restores read-write access after either protection.

## Caveats
- The functions apply only to regions from `sodium_malloc` or `sodium_allocarray`; each allocation needs 3 or 4 extra pages, so do not use them for many small objects.
- Toggling protection changes page permissions; avoid it in hot loops.
- Not thread-safe across concurrent users of the same buffer: one thread setting noaccess while another reads
  crashes. Guard with a lock or keep the region readonly while shared.
- The functions return an `int`; check it.

## Verify
- [ ] Test that reading the buffer after `sodium_mprotect_noaccess` crashes (in a forked child test).

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: noaccess preserves data but blocks reads and writes, readonly makes writes terminate the process, readwrite restores access, sodium_free works on protected regions and zeroes memory, only sodium_malloc and sodium_allocarray regions are valid, 3 or 4 extra pages. Removed an unconfirmed statement about platforms without mprotect and the Heartbleed reference.

Method: documentation only; no commands were run.
