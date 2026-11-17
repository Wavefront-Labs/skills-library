---
id: computing-software.cryptography-implementation.libsodium.sodium-init-and-thread-safety
name: sodium-init-and-thread-safety
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, sodium-helpers, sodium-init, thread-safety, cpu-feature-detection, static-linking, version-check, libsodium-installation]
level: practitioner
status: docs-checked
description: "Initialise libsodium correctly: sodium_init return values, calling it before threads, CPU feature detection, version checks, and linking/packaging gotchas."
sources: ["https://doc.libsodium.org/usage", "https://doc.libsodium.org/installation", "https://doc.libsodium.org/helpers", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/sodium/core.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sodium_init and thread safety

## Call it once, early, and check it

```c
#include <sodium.h>
int main(void) {
    if (sodium_init() < 0) {
        /* panic: library cannot be used safely */
        return 1;
    }
    /* sodium_init returns 0 on success, 1 if already initialised, -1 on failure (docs) */
}
```

- Call before any other libsodium function. After init returns, the docs say all other libsodium functions are thread-safe; state structures such as `crypto_generichash_state` are per-caller objects, so do not share one between threads without your own locking.
- `sodium_init` detects CPU features (the source calls its runtime CPU feature detection) and seeds the RNG; the docs say it ensures the system RNG is properly seeded before returning, that `crypto_pwhash_*` works without it but possibly much slower, and that `sodium_malloc` and the other guarded allocation functions require it. `crypto_aead_aes256gcm_is_available()` reports whether hardware support exists.
- It is safe to call more than once and from different threads; later calls have no effect and return 1. It does no memory allocation but on Unix may open `/dev/urandom` and keep the descriptor.
- On some Linux systems (virtual machines, cloud instances, right after boot) `sodium_init` can stall while the entropy pool fills; the docs suggest `virtio-rng`, a kernel 5.4 or later, or `haveged` or `rng-tools` as workarounds.
- Bindings usually call it for you (PyNaCl on import, libsodium.js after
  `await sodium.ready`). In JS, every call before `ready` resolves fails.

## Version checks

```c
printf("%s\n", sodium_version_string());              /* release string, e.g. 1.0.x */
```

Feature availability by version is in the docs' notes: AEGIS and `crypto_kdf_hkdf_*` need 1.0.19+, the XOF functions 1.0.21, SHA-3 and ML-KEM 1.0.22; the docs name 1.0.22 as the latest stable release. Distribution packages lag
(Debian stable, RHEL); vendor or pin if you need newer APIs.

## Linking and packaging

- `pkg-config` (`--cflags libsodium`, `--libs-only-L`, `--libs-only-l`); link with `-lsodium`. For static linking, Visual Studio users define `SODIUM_STATIC=1` and `SODIUM_EXPORT=`.
- The docs list pre-built x86 and x86_64 libraries for Visual Studio 2017, 2019, 2022 and 2026; Visual Studio solutions are also in `builds/msvc` of the source.
- Minimal builds (the `--enable-minimal` configure option, which the libsodium test suite also covers) can omit functions; check this if a symbol is missing. The libsodium.js standard build likewise omits some functions that only the sumo build has.
- Verify downloads: distribution files can be verified with minisign using the Ed25519 public key printed on the docs installation page (`minisign -VP <key> -m <file>`).

## Verify

- [ ] `sodium_init()` called in process startup before threads; `< 0` handled.
- [ ] Version printed in logs/diagnostics and checked against required features.
- [ ] Release tarball signature verified in the build pipeline.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: sodium_init return values (0, -1, 1), safe to call repeatedly and from different threads, later functions thread-safe, no allocations but may keep /dev/urandom open, Linux stalling advice, requirement before guarded allocation functions, pkg-config, SODIUM_STATIC and SODIUM_EXPORT, minisign verification, prebuilt Visual Studio libraries, version gates (1.0.19, 1.0.21, 1.0.22), core.c runtime CPU feature detection and RNG seeding. Removed the sodium_library_version_major example (it is not the release number), the MSVC runtime remark and an AES-GCM-on-ARM claim. The source URLs for a library_version page are dropped because the documentation repository has no such page.

Method: documentation only; no commands were run.
