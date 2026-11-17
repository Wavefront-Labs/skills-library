---
id: computing-software.cryptography-implementation.secure-implementation.hidden-copies-of-secrets-in-memory
name: hidden-copies-of-secrets-in-memory
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, secret-copies, secure-memory, zeroization, memory-safety, rust, libsodium]
level: advanced
status: docs-checked
description: "Find and reduce hidden secret copies: reallocation, moves and stack spills, serialization, swap and hibernation, with the libsodium and Rust zeroize/secrecy controls."
sources: ["https://docs.rs/zeroize/latest/zeroize/", "https://docs.rs/secrecy/latest/secrecy/", "https://doc.libsodium.org/memory_management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden copies of secrets in memory

Zeroising "the key buffer" is pointless if other copies exist. Copies come from:

## Sources of copies

| Source | Detail (from the documentation read) |
|---|---|
| Reallocation | `Vec`, `String` and `CString` zeroize their whole capacity but cannot remove copies made earlier by buffer reallocation |
| Moves and stack spills | Rust move semantics copy values; stack spilling and optimisations may leave temporary copies of heap data on the stack |
| Registers and stack | `mlock()` protects only heap data; data is copied to registers and the stack when used |
| Serialization | `secrecy::SecretBox` has no `Serialize` impl by default, to prevent exfiltration through serde; clean up intermediate input when deserializing |
| Swap, core dumps, hibernation | Hibernation writes all RAM to disk and bypasses memory locking |
| Microarchitecture | Spectre/Meltdown-style attacks may leak "zeroized" secrets; zeroize makes no guarantee against them |

## Controls

- **Zeroing that survives optimisation:** libsodium notes that `memset()` and hand-written
  loops can be stripped by the compiler or linker and offers `sodium_memzero()`. Rust's
  `zeroize` crate uses volatile writes and fences so the zeroing cannot be optimised away.
- **Allocate once at final size:** for `Vec`/`String`, initialise to the correct capacity and
  prevent later reallocation. The `secrecy` crate offers higher-level types that avoid
  reallocating patterns.
- **Heap over stack in Rust:** zeroize recommends keeping sensitive data on the heap to reduce
  copies from moves; `Pin` can keep stack data from moving, and `zeroize_stack` clears stack space.
- **Types that always hold secrets:** zeroize recommends a `Drop` impl (marked with
  `ZeroizeOnDrop`) instead of implementing `Zeroize`, to avoid a use-after-zeroize state.
- **Wrapper types:** `secrecy::SecretBox` makes access explicit (`ExposeSecret`), prevents debug-log
  leakage and wipes on drop, but does not use `mlock`/`mprotect`.
- **C allocations:** `sodium_malloc` places the region against a guard page, adds a canary,
  calls `mlock()` (which may fail or be a no-op) and excludes the memory from core dumps where
  `MAP_NOCORE` or `MADV_DONTDUMP` exists; `sodium_free` zeroes before release.
  `sodium_stackzero()` wipes stack after sensitive operations.
- **Process level:** libsodium recommends disabling swap (or using encrypted swap), disabling
  core dumps with `ulimit` or `setrlimit(RLIMIT_CORE, ...)`, disabling kernel crash dumps, and
  disabling hibernation on systems with sensitive workloads. `mlock` limits are governed by
  `RLIMIT_MEMLOCK`. Treat memory locking as defence in depth.

## Verify

- [ ] Secret types do not print their value in debug or log output.
- [ ] Buffers holding secrets are sized once and not grown.
- [ ] Core dumps, swap and hibernation are handled per the deployment's threat model.

## Checked

Method: docs-checked 2026-11-09 against docs.rs/zeroize (full page), docs.rs/secrecy (full page), doc.libsodium.org/memory_management (full page). Removed: the USENIX Security 2017 reference (talk page not read), per-language advice for Java, Go, Python and JS, `prctl(PR_SET_DUMPABLE)`, `explicit_bzero`/`OPENSSL_cleanse`, claims about immutable strings, bignum temporaries, key schedules and TLS session state, and the core-dump grep verification step.
