---
id: computing-software.cryptography-implementation.applied-cryptography.xts-aes-block-device-encryption
name: xts-aes-block-device-encryption
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, storage-encryption-modes, xts-aes, sp-800-38e, ieee-1619, disk-encryption, luks, dm-crypt, sector-encryption, tweak]
level: advanced
status: gated
description: "Use XTS-AES for sector/block storage correctly: double-length keys, distinct key halves, tweak = sector number, data-unit limits, and what XTS does not protect against."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/e/final", "https://standards.ieee.org/ieee/1619/4205/", "https://gitlab.com/cryptsetup/cryptsetup/-/wikis/FrequentlyAskedQuestions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XTS-AES for block-device encryption

XTS (IEEE 1619, approved by SP 800-38E "for protecting the confidentiality of data on storage devices" with one additional requirement) is a tweakable,
length-preserving mode: each sector encrypts independently, with the sector
number as the tweak, so equal data in different sectors encrypts differently
and there is no room for an IV or tag. It is the right choice when ciphertext
must be the same size as the sector (disks, LUKS, BitLocker, FileVault,
APFS). It is the wrong choice for files, records or messages.

## Key and tweak

- Key is two AES keys concatenated: XTS-AES-128 uses 32 bytes, XTS-AES-256
  uses 64 bytes. `aes-xts-plain64` with `--key-size 512` in cryptsetup is
  AES-256.
- The two halves must differ. pyca/cryptography (OpenSSL 3.2.3 backend) raises `In XTS mode duplicated keys are not allowed` (run);
  the FIPS 140-3 Implementation Guidance requirement for distinct halves (gated: unconfirmed, source is paywalled or blocked). Generate the full
  length from the CSPRNG, never duplicate a 256-bit key. pyca accepts 32 and 64 byte keys and rejects 48 (run).
- Tweak = data-unit (sector) number, little-endian, 16 bytes. Use 64-bit
  sector numbers (`plain64`) - 32-bit `plain` wraps on disks over 2 TiB and
  reuses tweaks.
- Data unit: SP 800-38E says a data unit "shall not exceed" 2^20 AES blocks (16 MiB), noting IEEE 1619 only recommends it; in
  practice 512 B or 4096 B sectors. Minimum 16 bytes (pyca rejects a first update under 16 bytes, run); partial final blocks use
  ciphertext stealing inside XTS (a 17-byte input gives 17 bytes, run).

## What XTS does not give you

- **No integrity**: an attacker with write access can replace a sector with
  random data (which decrypts to random garbage) or with an older ciphertext
  of the same sector (rollback). Use dm-integrity / `cryptsetup --integrity`
  or a filesystem with authenticated metadata if tampering matters.
- **Deterministic per sector**: re-writing the same data to the same sector
  gives the same ciphertext, and changes are visible at 16-byte granularity.
  An attacker who images the disk repeatedly learns which blocks changed.
- Protects data at rest when powered off; nothing once the volume is unlocked.

## LUKS2 example

```bash
# options (--type luks2 --cipher --key-size --sector-size --pbkdf) are listed in the cryptsetup-luksFormat man page source;
# command not run: no Linux host or block device here (gated: unconfirmed, source is paywalled or blocked)
cryptsetup luksFormat --type luks2 --cipher aes-xts-plain64 --key-size 512 \
  --pbkdf argon2id --sector-size 4096 /dev/sdX
cryptsetup luksDump /dev/sdX | grep -E 'cipher|sector|PBKDF'
```

## Verify

- [ ] Cipher string ends in `plain64` and key size is 512 bits for AES-256.
- [ ] Key halves generated independently (check custom code: no `key + key`).
- [ ] XTS used only for fixed-size storage units, not application records.
- [ ] Integrity requirement assessed; dm-integrity or AEAD layer added if needed.
- [ ] KATs pass from the IEEE 1619 / SP 800-38E (CAVP XTSGenAES) vectors for custom code (IEEE 1619 vector 2, key 11..11|22..22,
  tweak 3333333333, plaintext 44 x 32, gives `c454185e...94f0` in pyca).
