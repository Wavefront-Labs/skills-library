---
id: computing-software.cryptography-implementation.secure-implementation.rowhammer-and-software-induced-faults
name: rowhammer-and-software-induced-faults
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, rowhammer, fault-attack, software-induced-faults, plundervolt, ecc-memory]
level: sme
status: draft
description: "Protect keys against Rowhammer and software-induced faults: ECC memory limits, signature verification after signing, redundancy checks, and Plundervolt-style undervolting."
sources: ["https://users.ece.cmu.edu/~yoonguk/papers/kim-isca14.pdf", "https://plundervolt.com/", "https://eprint.iacr.org/2016/618"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rowhammer and software-induced faults

## Threats
- **Rowhammer**: repeated DRAM row access flips bits in neighbouring rows. Demonstrated against RSA keys in
  co-located VMs (Flip Feng Shui), page tables, and via JavaScript. DDR4 TRR and DDR5 on-die ECC reduce but have
  not eliminated it (TRRespass, Blacksmith, ZenHammer).
- **Software-controlled undervolting/overclocking**: Plundervolt (CVE-2019-11157), CLKSCREW and V0LTpwn induce
  computation faults from privileged software, breaking SGX or TrustZone crypto.
- A single fault in RSA-CRT signing reveals the private key (Bellcore attack); a faulted deterministic ECDSA or
  EdDSA signature can leak the key too.

## Defences
- **Verify before release**: check RSA-CRT signatures with the public key before output (OpenSSL does); for
  deterministic EdDSA/ECDSA consider hedged signing or verify-after-sign on high-value signers.
- **Integrity of stored keys**: keep a checksum/MAC of key material and check before use; re-derive from a
  protected seed when possible.
- **Memory**: ECC DIMMs for servers holding keys (detects/corrects single-bit flips; multi-bit flips remain);
  do not share physical hosts with untrusted tenants for high-value keys; disable memory deduplication (KSM) where
  Flip Feng Shui applies.
- **Voltage interfaces**: microcode updates lock undervolting MSRs when SGX is enabled; BIOS options to disable
  software voltage control.

## Verify
- [ ] Signing paths verify output; key-holding hosts use ECC memory and dedicated tenancy; KSM disabled.
