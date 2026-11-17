---
id: computing-software.firmware-embedded-development.iot-protocols.iot-secure-element-keys
name: iot-secure-element-keys
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [iot-secure-element-keys, iot-security, secure-element, atecc608, tpm, key-storage, iot-protocols]
level: practitioner
status: draft
description: "Secure element key storage: Keep device keys non-extractable."
sources:
  - https://www.etsi.org/deliver/etsi_en/303600_303699/303645/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure element key storage

**Goal:** Keep device keys non-extractable.

## Steps
1. Choose secure element (ATECC608B, SE050, STSAFE) or TPM or MCU TrustZone/PSA
2. Generate the private key inside the chip and lock the slot configuration
3. Use the chip for TLS signature via PKCS#11 or mbedTLS ALT interface
4. Lock config zone and data zone at manufacturing
5. Enable debug port lockout (RDP level, secure debug)
6. Verify against ETSI EN 303 645 provisions: unique per-device passwords, update support, secure storage

## Gotcha
Unlocked configuration zones allow later key overwrites; lock the chip as the last factory step.

## Verify
- [ ] Key slot cannot be read
- [ ] TLS signs via chip
- [ ] Debug port locked
