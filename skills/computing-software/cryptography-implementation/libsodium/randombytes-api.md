---
id: computing-software.cryptography-implementation.libsodium.randombytes-api
name: randombytes-api
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, sodium-helpers, randombytes-buf, randombytes-uniform, randombytes-buf-deterministic, csprng, rejection-sampling, test-reproducibility]
level: practitioner
status: docs-checked
description: "Generate randomness with libsodium: randombytes_buf, unbiased randombytes_uniform, seeded randombytes_buf_deterministic for tests/derivation, and fork/embedded caveats."
sources: ["https://doc.libsodium.org/generating_random_data", "https://doc.libsodium.org/advanced/custom_rng", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/randombytes/randombytes.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The randombytes API

libsodium's default RNG sources, per its documentation: `RtlGenRandom()` on Windows, `arc4random()` on OpenBSD, the `getrandom` system call on recent FreeBSD and Linux kernels, and `/dev/urandom` on other Unices; if none can be used safely, a custom implementation can be hooked.

## Functions

```c
unsigned char nonce[24];
randombytes_buf(nonce, sizeof nonce);              /* fill buffer */
uint32_t r = randombytes_random();                 /* 0 .. 2^32-1 */
uint32_t die = randombytes_uniform(6) + 1;         /* unbiased 1..6 */
unsigned char seed[randombytes_SEEDBYTES];         /* 32 */
randombytes_buf_deterministic(out, len, seed);     /* same bytes for the same seed */
```

## Use `randombytes_uniform` for ranges

`randombytes_random() % n` is biased when n does not divide 2^32 (e.g. picking
from 62 characters for a token). `randombytes_uniform(n)` uses rejection
sampling and is unbiased. For tokens, prefer encoding random bytes
(base64url of 32 bytes) over character-by-character selection.

## Deterministic stream

`randombytes_buf_deterministic` expands a 32-byte seed with the ChaCha20 stream cipher (the source uses the IETF variant with the fixed nonce "LibsodiumDRG"); up to 2^38 bytes (256 GB) per seed. The docs say it is mainly useful for writing tests and was introduced in libsodium 1.0.12. Uses:
- Reproducible test fixtures and fuzzing corpora.
- Deriving long pseudorandom outputs from a key (but `crypto_kdf` or HKDF is
  the clearer tool for keys).

Never use it as a nonce source across messages with the same seed - it
produces the same bytes every time by design.

## Caveats

- Forked processes: with the default generator, `randombytes_stir()` is not required even after `fork()`, unless the `/dev/urandom` descriptor was closed with `randombytes_close()`. With a non-default implementation (`randombytes_set_implementation`), the child must call `randombytes_stir()` after `fork()`.
- VM snapshots: if a VM is snapshotted and restored, the functions may produce the same output (libsodium docs note).
- Targets with no usable OS source need a custom implementation, for example backed by a hardware TRNG; review it carefully.
- `randombytes_close()` deallocates the generator's global resources (closing the `/dev/urandom` descriptor when that is used); the docs say calling it is almost never required.

## Verify

- [ ] No `rand()`, `% n` on random words, or seeded deterministic stream used for nonces/keys.
- [ ] Range selection uses `randombytes_uniform`.
- [ ] Custom RNG (if any) reviewed and fork-safe.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: platform sources, randombytes_random range, randombytes_uniform uniformity versus modulo, deterministic function (ChaCha20, 2^38 byte limit, 1.0.12, mainly for tests), randombytes_close and randombytes_stir fork behaviour, VM snapshot note (docs); randombytes_SEEDBYTES 32 and the IETF ChaCha20 fixed nonce LibsodiumDRG (source). Removed an unconfirmed libsodium.js statement.

Method: documentation only; no commands were run.
