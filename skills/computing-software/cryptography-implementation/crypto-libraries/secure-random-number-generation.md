---
id: computing-software.cryptography-implementation.crypto-libraries.secure-random-number-generation
name: secure-random-number-generation
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, csprng, random-number-generation, insecure-random, math-random, python-random, securerandom, getrandomvalues, dev-urandom, getrandom, fork-safety, docker-entropy, seeding, pcg, mersenne-twister]
level: practitioner
status: verified
description: "Picking and verifying a CSPRNG per language: which default RNG is insecure (Math.random, Python random, PCG), fork/container entropy pitfalls, and how to prove the right source is used."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues", "https://docs.python.org/3/library/secrets.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/SecureRandom.html", "https://man7.org/linux/man-pages/man2/getrandom.2.html", "https://v8.dev/blog/math-random", "https://pkg.go.dev/math/rand/v2", "https://www.debian.org/security/2008/dsa-1571"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure random number generation per language

Every cryptographic operation (keys, nonces, IVs, salts, session tokens) is
only as strong as the randomness behind it. The recurring real-world bug is
not "we forgot to use randomness" — it's **using the language's default
non-cryptographic RNG by accident**, because the insecure and secure APIs
often look nearly identical.

## The insecure-by-default traps, per language

- **JavaScript:** `Math.random()` is **not cryptographically secure** (V8 uses xorshift128+ since v4.9.41, per the V8 blog,
  and Firefox and Safari switched to it as well; it is a small-state generator and is not meant for secrets). Use `crypto.getRandomValues()` (browser/Node) or
  Node's `crypto.randomBytes()`. This is the single most common crypto bug
  in JS codebases — `Math.random()` used for a token, reset code, or even a
  nonce.
- **Python:** the `random` module (Mersenne Twister) is **not secure** —
  its full internal state can be recovered from 624 consecutive 32-bit outputs (run: untempering 624 `getrandbits(32)`
  values and calling `setstate` predicted the next 5 outputs exactly),
  after which all future outputs are predictable. Use the `secrets`
  module (`secrets.token_bytes`, `secrets.token_urlsafe`) or
  `os.urandom()`. `random.SystemRandom()` is also fine (it is the class
  `secrets` wraps: `secrets.SystemRandom is random.SystemRandom`, checked, and `secrets` builds `_sysrand = SystemRandom()`).
- **Java:** plain `Random` is a 48-bit linear congruential generator —
  trivially predictable (Java 8, run through `jjs`: from two consecutive `nextInt()` outputs, brute-forcing the 16 unseen low bits
  recovered the state and predicted the third output). Use `java.security.SecureRandom`. If you hit a startup hang in a
  Linux container, read the `SecureRandom` Javadoc and your JDK's `java.security` file for the configured entropy source;
  the blocking behaviour depends on the JDK version and OS and was not tested here.
- **Go:** `math/rand` and `math/rand/v2` are documented as not to be used for security-sensitive work (`math/rand`: "might be
  easily predictable regardless of how it's seeded"; `v2` calls its ChaCha8 source resistant to prediction and its PCG source unfit for
  security, but the package is still the wrong default for keys and tokens). Use `crypto/rand`. Easy mistake: `crypto/rand`
  has a different, more limited API (`rand.Read`, `rand.Int`) — reaching for
  the familiar `math/rand` API surface under deadline pressure is how this
  slips in.
- **.NET:** avoid `System.Random`. Use
  `System.Security.Cryptography.RandomNumberGenerator` (static `Fill`/`GetBytes`;
  the older `RNGCryptoServiceProvider` is marked `Obsolete` with diagnostic SYSLIB0023 in the dotnet-api-docs source, which tells you to use the
  `RandomNumberGenerator` static methods).
- **C/C++:** avoid `rand()`/`srand()` entirely for anything security-relevant.
  Use the platform's CSPRNG primitive directly (`getrandom(2)` on Linux,
  `arc4random_buf` on BSD/macOS, `BCryptGenRandom` on Windows) or go through
  a library (OpenSSL's `RAND_bytes`, libsodium's `randombytes_buf`).

## Fork and container entropy pitfalls

- **Fork safety:** a userspace generator seeded once at process start and then `fork()`ed (pre-fork server models) can produce
  **identical output streams in parent and child** if the library caches internal RNG state without re-seeding post-fork. Generators
  that read the kernel each time (`getrandom(2)`, `os.urandom`, `secrets`) do not have this problem. CPython's own `random` module
  guards against it: `Lib/random.py` registers `os.register_at_fork(after_in_child=_inst.seed)`. Verify older libraries and custom RNG
  wrappers (see the reseeding-after-fork skill). Fork cannot be tested on Windows, so this was read from source, not run.
- **Low-entropy boot in containers/VMs:** `getrandom(2)` (Linux 3.17, glibc 2.25 per its man page) blocks until the kernel
  entropy pool is initialised unless `GRND_NONBLOCK` is given, instead of returning weak output; early-boot reads of `/dev/urandom`
  on old kernels did not have that guarantee. Prefer libraries that call `getrandom(2)`. This matters mainly for minimal or early-boot
  images.
- **Never roll your own "entropy pool"** (mixing timestamps, PIDs, `/proc`
  noise) as a substitute for the OS CSPRNG. The 2008 Debian OpenSSL weak-key incident (DSA-1571: "predictable random number
  generator") came from a packaging change that removed entropy sources from OpenSSL's generator; home-made mixing is never an
  improvement over the kernel's generator.

## Verify

- [ ] Grep the codebase for the language's non-cryptographic RNG
      (`Math.random`, `random.random`/`random.randint`, plain `Random`,
      `math/rand`, `System.Random`, `rand()`) in any file that also handles
      tokens, keys, nonces, or salts.
- [ ] Every security-sensitive random value traces to the platform CSPRNG
      API, not a wrapper that silently falls back to a non-crypto source.
- [ ] If the process forks (pre-fork server models), confirmed the CSPRNG
      reseeds or draws fresh kernel entropy post-fork rather than replaying
      parent state.
- [ ] No custom "entropy mixing" code anywhere.

Startup-blocking behaviour varies by JDK/.NET version and OS; confirm against your deployed runtime. The C-level names
(`arc4random_buf`, `BCryptGenRandom`, OpenSSL `RAND_bytes`, libsodium `randombytes_buf`) and .NET `RandomNumberGenerator.Fill` are present in the
OpenBSD, Microsoft Learn, OpenSSL and libsodium manuals and the dotnet-api-docs source; those calls were not run.
