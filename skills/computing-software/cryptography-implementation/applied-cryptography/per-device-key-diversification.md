---
id: computing-software.cryptography-implementation.applied-cryptography.per-device-key-diversification
name: per-device-key-diversification
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, key-diversification, master-key, device-keys, an10922, emv, kdf]
level: advanced
status: docs-checked
description: "Diversify per-device keys from a master key (smartcards, IoT): KDF over device ID, NXP AN10922 CMAC method, master key custody and blast radius."
sources: ["https://www.nxp.com/docs/en/application-note/AN10922.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-108r1-upd1.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-device key diversification

Each device gets `K_dev = KDF(K_master, device_id || purpose)`. The backend stores only the master key and
recomputes any device key on demand. NXP AN10922 describes the point of diversification: each card gets different
key values, so if one key is broken the vulnerability is limited to that key on that card rather than the whole
system.

## Methods
- Generic: an SP 800-108 PRF-based KDF with a Label identifying the purpose and a Context carrying the device
  identity (SP 800-108 says Context may include the identities of the parties), or HKDF with the same inputs in `info`.
- NXP AN10922 (Rev. 2.2): CMAC-based diversification, the algorithm NXP recommends for MIFARE SAM AV3. A MAC is used
  rather than encryption so the function is one-way. For AES-128 the input is 1 to 31 bytes of diversification data
  M and a 16-byte master key K; D = 0x01 || M || padding (80h then 00h bytes) to 32 bytes; the output is
  AES128CMAC(K, D, Padded), where Padded is true if M is shorter than 31 bytes.
- AN10922 recommends, per card, a diversification input of at least the card UID plus: for MIFARE Plus the block
  number holding the key (all keys that must match for multi-sector authentication need the same block number); for
  MIFARE DESFire the key number concatenated with the application number.

## Design rules
- Include a purpose label so encryption and MAC keys differ: separate derivations per key type.
- Device ID must be unique and immutable (chip UID, serial); never let the device choose it freely.
- Keep the master key in secure hardware and derive there, as AN10922 describes for the SAM, so the master never leaves.
- Version the master key; record which version each device was provisioned with for rotation.

## Blast radius
Master key compromise exposes every device. Use separate masters per product line, region or batch, and plan
re-provisioning.

## Verify
- [ ] Vendor test vectors (AN10922 examples) reproduce.
- [ ] Derivation runs inside the secure module; audit logs show no master export.

## Checked

Confirmed from NXP AN10922 Rev. 2.2 (PDF read: purpose of diversification, CMAC construction, AES-128 algorithm with the 0x01 prefix and padding, UID plus block or key and application number inputs) and the SP 800-108 Rev. 1 PDF (Label and Context definitions). The EMVCo specifications link is a landing page and was not read. Removed: EMV Option A/B and ATC session keys, GlobalPlatform SCP03, the PKCS#11 mechanism name and the HSM-specific claims, none of which were confirmed.

Method: docs-checked 2026-11-09 against NXP AN10922 PDF and SP 800-108 Rev. 1 PDF.
