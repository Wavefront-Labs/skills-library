---
id: computing-software.cryptography-implementation.libsodium.password-hashing-parameter-tuning
name: password-hashing-parameter-tuning
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-pwhash, argon2id, opslimit, memlimit, password-hashing, parameter-tuning, rehashing, benchmark, pynacl, dos-resistance, pwhash-needs-rehash]
level: advanced
status: docs-checked
description: "Tuning libsodium's crypto_pwhash (Argon2id) OPSLIMIT/MEMLIMIT for your actual hardware and latency budget, picking a profile, and migrating users to stronger parameters later."
sources: ["https://doc.libsodium.org/password_hashing/default_phf", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_pwhash_argon2id.h"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tuning libsodium's crypto_pwhash (Argon2id) parameters

The existing `authenticated-encryption-and-signatures` skill in this product
names `crypto_pwhash` as the password-hashing call; this skill is the part
that actually determines whether it protects anything — the OPSLIMIT/MEMLIMIT
parameters, which libsodium deliberately does not pick for you beyond rough
presets.

## The three built-in profiles, and why you shouldn't stop there

Libsodium ships `_INTERACTIVE`, `_MODERATE`, and `_SENSITIVE` constants for
both OPSLIMIT (iteration count) and MEMLIMIT (memory in bytes):
- `INTERACTIVE` (64 MiB, opslimit 2 for Argon2id): the docs call it a baseline for interactive, online operations, and note higher values may improve security.
- `MODERATE` (256 MiB, opslimit 3): the docs say it takes about 0.7 seconds on a 2.8 GHz Core i7.
- `SENSITIVE` (1024 MiB, opslimit 4): for highly sensitive data and non-interactive operations; about 3.5 seconds on the same CPU per the docs.

**These presets are not calibrated to your actual server and your actual
latency budget** — they're libsodium's generic defaults. A senior
implementer benchmarks on the actual production hardware class and picks
the highest MEMLIMIT/OPSLIMIT that fits the latency budget, rather than
shipping a preset unexamined.

## Benchmark on real hardware, not a laptop

Follow the libsodium docs' procedure: decide the highest number of simultaneous hashing threads or processes (ideally no more than one per CPU core) and the memory guaranteed to be available, set `memlimit` to the memory you want to reserve, set `opslimit` to 3 and measure on the
actual instance type/CPU the login path will run on. If it is too slow, reduce `memlimit` and keep `opslimit` at 3; if it is fast enough to afford more work, increase `opslimit`. Choose the latency target from your own threat model and login UX; the docs give no universal figure.

## DoS consideration: password hashing is a two-edged sword

The same cost that defeats offline brute force also costs *you* CPU/memory
per login attempt — an unauthenticated login endpoint calling
`crypto_pwhash` at `SENSITIVE` parameters on every request is a
self-inflicted amplification vector for a login-flood DoS. Rate-limit login
attempts (per-IP and per-account) independently of the hashing cost itself;
don't rely on the hash cost as your only anti-abuse control.

## Migrating to stronger parameters later (rehash-on-login)

Hardware gets faster; parameters chosen as "moderate" in 2024 are weaker
relative to attacker capability in 2028. Libsodium's stored hash string
(`crypto_pwhash_str` output) embeds the algorithm and parameters used, so
you can detect a mismatch and upgrade incrementally:
1. On every successful login, check whether the stored hash's embedded
   parameters match your *current* target profile
   (`crypto_pwhash_str_needs_rehash` is the libsodium helper for exactly
   this check; it returns 1 when the string is valid but the parameters differ, 0 when they match, and -1 on error).
2. If not, re-hash the password (which you have in plaintext at that moment
   because the user just typed it correctly) with current parameters and
   overwrite the stored hash.
3. This naturally migrates your whole user base to stronger parameters over
   time, driven by login frequency, with zero forced-reset campaign and
   zero moment where you ever need the plaintext password outside a live
   login.
- Users who never log in during the migration window never get upgraded —
  decide whether that residual risk is acceptable or whether it needs a
  forced reset for long-dormant accounts.

## Verify

- [ ] OPSLIMIT/MEMLIMIT were benchmarked against the actual production
      hardware class and a stated latency budget — not left at an unexamined
      preset name.
- [ ] `opslimit` and `memlimit` were set following the documented procedure (opslimit 3, tune memlimit first).
- [ ] Login endpoint has independent rate-limiting so the hash cost isn't
      also your only DoS control.
- [ ] `crypto_pwhash_str_needs_rehash` (or equivalent) is checked on every
      login, with transparent rehash-and-store on mismatch.
- [ ] A decision is on record for how long-dormant accounts get migrated
      (or whether that gap is accepted).

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: INTERACTIVE 64 MiB (opslimit 2), MODERATE 256 MiB (3, about 0.7 s), SENSITIVE 1024 MiB (4, about 3.5 s) from the docs and the Argon2id header; tuning procedure (memlimit from concurrency and available RAM, opslimit 3, adjust); parameters embedded in the str output; needs_rehash return values; parameters must be stored rather than relying on constants. Removed the unsourced 250 ms to 1 s target, claims about local-secret sizing and GPU resistance, and the RFC 9106 and OWASP source entries that were not consulted.

Method: documentation only; no commands were run.
