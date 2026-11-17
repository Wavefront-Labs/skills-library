---
id: computing-software.systems-network-administration.linux.cryptsetup-benchmark-cipher-choice
name: cryptsetup-benchmark-cipher-choice
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, luks, cryptsetup-benchmark, aes-xts, argon2id, pbkdf, disk-encryption-performance]
level: practitioner
status: docs-checked
description: "Choose LUKS cipher and KDF parameters with cryptsetup benchmark: AES-NI check, aes-xts key sizes, adiantum for CPUs without AES, argon2id memory and iteration time trade-offs."
sources:
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-benchmark.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/common_options.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksConvertKey.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/configure.ac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cryptsetup benchmark and cipher choice

## Run it
```bash
cryptsetup benchmark                       # a few common cipher and KDF configurations
cryptsetup benchmark --cipher aes-xts-plain64 --key-size 512   # a specific cipher
cryptsetup benchmark --pbkdf argon2id --iter-time 2000 --pbkdf-memory 1048576   # a specific KDF cost
```
The benchmark uses memory only and is informative: you cannot directly predict real storage encryption speed from it. Block-cipher tests need the kernel userspace crypto API (`CRYPTO_USER_API_SKCIPHER`).

## Choices
- Upstream builds default to `aes-xts-plain64` (see `cryptsetup --help` for what your build uses). For XTS the key size is twice that of other modes for the same security level: `--key-size 512` is AES-256 in XTS.
- Other ciphers can be benchmarked with `--cipher` and `--key-size` before choosing them.

## KDF (unlock cost, not disk speed)
The LUKS2 default PBKDF is set at compile time (upstream: argon2id, 2000 ms iteration time, 1048576 kB memory, up to 4 threads); `cryptsetup --help` shows your build's value. The benchmark tunes the cost to the creating machine.
```bash
cryptsetup luksFormat --type luks2 --pbkdf argon2id --iter-time 3000 --pbkdf-memory 1048576 /dev/sdX
cryptsetup luksConvertKey --pbkdf argon2id --iter-time 3000 /dev/sdX   # change an existing keyslot's KDF
```
- For argon2 the memory cost is a maximum that the benchmark or available RAM can lower; for PBKDF2 only the iteration count applies. LUKS1 supports only PBKDF2.
- A disk formatted on a fast desktop may unlock slowly on a slow device — set `--iter-time`/memory explicitly.

## Performance knobs
`--perf-no_read_workqueue --perf-no_write_workqueue` (accepted by `open` and `refresh`; `--persistent` stores them in the LUKS2 metadata) bypass the dm-crypt workqueue and process requests synchronously.
`--sector-size` (luksFormat, LUKS2) sets the encryption sector size; it must be a power of two from 512 to 4096 bytes.

## Verify
- [ ] `cryptsetup luksDump` shows the intended cipher, key size, sector size and PBKDF; measured throughput on the mapping meets requirements.

## Checked

Checked against the cryptsetup main branch (man/cryptsetup-benchmark, common_options, luksConvertKey, refresh; configure.ac), documentation fetched 2026-10-25.
Confirmed: benchmark scope and options; compile-time LUKS2 defaults (argon2id, 2000 ms, 1048576 kB, 4 threads) from configure.ac; PBKDF2 versus Argon2 cost parameters; XTS key size is doubled; `--perf-no_read_workqueue`, `--perf-no_write_workqueue` and `--persistent` apply to open/refresh; sector size range 512 to 4096; luksConvertKey converts a LUKS2 keyslot to new PBKDF parameters.
Removed unconfirmed claims: sample benchmark output, the adiantum recommendation, the serpent/twofish remark, the AES-NI cpuinfo check, GRUB PBKDF2 support, and the statement that 512-bit is the default (the upstream configure default is 256 bits; distributions differ).

Method: documentation only; no commands were run.
