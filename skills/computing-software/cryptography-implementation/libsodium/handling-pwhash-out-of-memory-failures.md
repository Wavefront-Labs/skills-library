---
id: computing-software.cryptography-implementation.libsodium.handling-pwhash-out-of-memory-failures
name: handling-pwhash-out-of-memory-failures
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, pwhash-out-of-memory, crypto-pwhash, argon2id, libsodium, error-handling, memory-limits]
level: practitioner
status: docs-checked
description: "Handle crypto_pwhash failures: -1 returns from memory allocation, container memory limits, MEMLIMIT bounds, concurrency caps, and safe error responses."
sources: ["https://doc.libsodium.org/password_hashing/default_phf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling pwhash out-of-memory failures

`crypto_pwhash`, `crypto_pwhash_str` and `_str_verify` return -1 on failure. For Argon2 the usual cause is that
`memlimit` bytes could not be allocated, which looks identical to a wrong password if you only check `!= 0`.

## Distinguish failures
- `crypto_pwhash_str_verify` returns -1 on any error (the docs list 0 for success and -1 otherwise), which includes allocation failure; `crypto_pwhash_str_needs_rehash` also returns -1 on error. Log at error level when the process is under
  memory pressure, and monitor rates; do not tell users their password was wrong when it was an OOM.
- `crypto_pwhash` (key derivation) failing must abort the operation; never continue with an uninitialised key
  buffer.

## Prevent it
- Container limits: 10 concurrent logins x 256 MiB = 2.5 GiB. The libsodium docs advise sizing `memlimit` from the highest number of simultaneous hashing threads/processes (ideally no more than 1 per CPU core) and the physical memory guaranteed to be available. Cap concurrent hash operations with a semaphore
  sized to `available_memory / memlimit`, queue the rest, and return 503 when the queue is full.
- Keep `memlimit` between `crypto_pwhash_MEMLIMIT_MIN` and `_MAX`; for interactive logins 64 MiB
  (`MEMLIMIT_INTERACTIVE`) is common, `MODERATE` 256 MiB, `SENSITIVE` 1 GiB.
- In libsodium.js, `crypto_pwhash_*` exists only in the sumo build, which reserves more memory than the standard build; test memlimits on the target runtime.
- Do not accept hashing parameters from untrusted input; a stored hash string with a huge memlimit verified
  server-side is a DoS vector, so validate stored parameters against your policy before verifying.

## Verify
- [ ] Load test at peak concurrency shows no -1 results; alerts exist for pwhash failures.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: crypto_pwhash returns -1 when the computation did not complete, usually because the OS refused the memory; str_verify returns 0 or -1; INTERACTIVE 64 MiB, MODERATE 256 MiB, SENSITIVE 1024 MiB; memlimit must lie between MEMLIMIT_MIN and MEMLIMIT_MAX; concurrency guidance; sumo-only pwhash in libsodium.js (libsodium.js README). Removed an unconfirmed 32-bit and WebAssembly claim and the RFC 9106 source.

Method: documentation only; no commands were run.
