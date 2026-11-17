---
id: computing-software.cryptography-implementation.openssl.checking-aes-ni-hardware-acceleration
name: checking-aes-ni-hardware-acceleration
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, cipher-strings, aes-ni, hardware-acceleration, openssl-ia32cap, armv8-crypto, pclmulqdq, vaes, chacha20-vs-aes, cache-timing]
level: advanced
status: draft
description: "Confirm AES-NI/ARMv8 crypto extensions are used: CPU flags, OPENSSL_ia32cap masking to compare, VM passthrough, and choosing ChaCha20-Poly1305 where AES hardware is absent."
sources: ["https://docs.openssl.org/3.0/man3/OPENSSL_ia32cap/", "https://www.intel.com/content/www/us/en/developer/articles/technical/advanced-encryption-standard-instructions-aes-ni.html", "https://datatracker.ietf.org/doc/html/rfc8439"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checking AES-NI and hardware acceleration

Hardware AES (x86 AES-NI + PCLMULQDQ for GHASH, VAES/AVX-512 on newer CPUs,
ARMv8 Crypto Extensions) makes AES-GCM several times faster **and** constant
time. Software AES with lookup tables is slow and leaks via cache timing.

## Check the CPU and VM

```bash
grep -o -w -E 'aes|pclmulqdq|vaes|vpclmulqdq|avx512f' /proc/cpuinfo | sort | uniq -c   # x86 Linux
grep -o -w -E 'aes|pmull|sha2' /proc/cpuinfo | sort -u                                 # ARM64 Linux
sysctl -a | grep -i 'hw.optional.arm.FEAT_AES'                                          # macOS ARM
```

Hypervisors sometimes mask CPU flags (old CPU models in VM configs, some
nested setups). If `aes` is missing inside a VM on modern hardware, fix the VM
CPU model (`host-passthrough`) rather than accepting slow crypto.

## Check OpenSSL uses it

```bash
openssl speed -evp aes-128-gcm -seconds 2                        # baseline
OPENSSL_ia32cap="~0x200000200000000" openssl speed -evp aes-128-gcm -seconds 2   # disable AES-NI+PCLMUL
```

The mask clears bit 57 (AES-NI) and bit 33 (PCLMULQDQ) of the capability vector.
A large drop (often 5-10x) confirms the accelerated path was in use. If both
runs are equally slow, the build or CPU lacks acceleration.

`openssl version -a` shows `CPUINFO: OPENSSL_ia32cap=...` in 3.x builds; a
non-default environment variable value here means someone has masked features.

## Choose the AEAD by platform

- AES hardware present (servers, modern laptops, ARMv8 phones): AES-128-GCM
  or AES-256-GCM.
- No AES hardware (older/low-end ARM, many MCUs without AES peripheral):
  ChaCha20-Poly1305 - fast in software and constant time without tables.
- TLS stacks (BoringSSL, Go, OpenSSL with `SSL_OP_PRIORITIZE_CHACHA`) can
  prefer ChaCha20 when the client lists it first, signalling no AES hardware.

## Embedded

On MCUs, use the AES peripheral via the vendor HAL or mbedTLS alt
implementations; check the peripheral handles key/IV loading without leaving
key material in readable registers after use.

## Verify

- [ ] CPU flags present in the production VM/container host.
- [ ] Masked vs unmasked `openssl speed` shows the expected gap.
- [ ] AEAD choice matches the hardware of the slowest major client population.
