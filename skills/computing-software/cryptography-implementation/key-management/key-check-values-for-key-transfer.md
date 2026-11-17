---
id: computing-software.cryptography-implementation.key-management.key-check-values-for-key-transfer
name: key-check-values-for-key-transfer
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-check-value, kcv, key-transfer, hsm, payment-hsm, aes-cmac, key-ceremony, key-verification]
level: practitioner
status: gated
description: "Compute and verify key check values (KCV) when moving keys between HSMs, KMS and partners: AES-CMAC and legacy encrypt-zeros methods and what KCVs leak."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/b/final", "https://x9.org/standards/x9-24-part-1/", "https://docs.aws.amazon.com/payment-cryptography/latest/userguide/keys-validattributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key check values for key transfer

A key check value is a short fingerprint used to confirm that a key entered from components, imported, or unwrapped
on another system is the same key, without revealing it.

## Methods
| Method | Computation | Typical length |
|---|---|---|
| Encrypt-zeros (legacy, TDES and AES) | Encrypt an all-zero block with the key; take the leftmost bytes | 3 bytes (6 hex) |
| AES-CMAC (ANSI X9.24-1:2017 (gated: unconfirmed, source is paywalled or blocked)) | CMAC of an all-zero block (or empty message, per profile) under the key | 5 bytes (as commonly configured) |
| SHA-based fingerprint | Hash of the key, truncated (some KMS/HSMs) | varies |

```
# Run on OpenSSL 3.2.3 with key 000102..0f: first command gives c6a13b, second gives BE7ED6AE78
# (the CMAC command with zero-length input gives 97DD6E5A88; agree which one your peer uses)
# Legacy AES KCV (encrypt zero block, first 3 bytes)
printf '\x00%.0s' {1..16} | openssl enc -aes-128-ecb -K <hexkey> -nopad | xxd -p | cut -c1-6
# AES-CMAC KCV
printf '\x00%.0s' {1..16} | openssl mac -cipher AES-128-CBC -macopt hexkey:<hexkey> CMAC | cut -c1-10
```
Agree the exact method and length with the other party; HSM vendors and payment networks differ.

## Use in key ceremonies
- Each key component has its own KCV, recorded by its custodian; the combined key has a KCV checked after entry.
- Record KCVs in the ceremony log and compare at the receiving side after import.

## What KCVs leak
- Encrypt-zeros KCVs give an attacker a known plaintext/ciphertext pair; for TDES that weakens the key slightly and is
  why the method is being replaced. Never compute a full-block KCV.
- A KCV lets anyone confirm a guessed key, so keys must have full entropy (true for RBG keys).

## Verify
- [ ] Both sides report the same KCV after import using the agreed method.
- [ ] KCVs are recorded in the key inventory, never the key itself.
