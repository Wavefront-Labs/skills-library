---
id: computing-software.firmware-embedded-development.bootloader-development.measured-boot-and-attestation
name: measured-boot-and-attestation
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [measured-boot, secure-boot, remote-attestation, boot-measurements, dice, firmware-embedded-development]
level: sme
status: docs-checked
description: "Add measured boot to an MCU: each stage hashes the next into a measurement log, DICE/CDI identity derivation, and attestation tokens a server can verify."
sources:
  - https://trustedcomputinggroup.org/resource/dice-layering-architecture/
  - https://trustedfirmware-m.readthedocs.io/en/latest/design_docs/booting/measured_boot_integration_guide.html
  - https://arm-software.github.io/psa-api/attestation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measured boot and attestation

**Secure boot** refuses to run unsigned code. **Measured boot** records *what* ran (hashes of each
stage) so a remote verifier can decide whether to trust the device. Both are usually combined.

## Measurement chain
1. Immutable first stage (ROM/BL1) hashes BL2 before jumping, stores the measurement.
2. BL2 (e.g. MCUboot) hashes the secure firmware and the application, extends/stores them.
3. Measurements live in a protected place: TPM PCRs on larger systems; on MCUs a shared-memory
   area handed to the secure partition (the TF-M measured boot design), or derived
   secrets (DICE).
Each record typically holds a measurement value, the signer ID, version and a component
description (see the TF-M measured boot design and the PSA Attestation API for the exact fields).

## DICE (Device Identifier Composition Engine)
Small-device alternative to a TPM, standardised by TCG:
- Hardware provides a **Unique Device Secret (UDS)**, readable only by the first code at boot,
  then locked (latch register or fuse).
- First stage derives a Compound Device Identifier (CDI) from the UDS and a measurement of the
  next stage, then locks the UDS. The next stage gets only the CDI.
- Any change to firmware changes the CDI, so device keys derived from it change automatically:
  modified firmware cannot use the genuine device's identity keys.
- Layers repeat: each stage derives the next CDI and an alias key pair; certificates chain from a
  manufacturer-registered DeviceID key.

## Attestation
The device produces a signed token containing a server-provided nonce and the measurements:
- The PSA Attestation API gives a health-check token attesting to a device's components and
  serial numbers.
- Verifier (e.g. Veraison) checks the signature against the device's registered attestation key
  and compares measurements against reference values (the known-good firmware hashes published at
  release time, often as CoRIM).

## Design points
- Publish reference measurements for every release from CI (hash of each signed image).
- Decide the policy for unknown measurements: deny service, quarantine, or force update.
- Protect the attestation key (secure element, TF-M isolation, DICE-derived).
- Nonce freshness prevents replay of an old token.

## Verify
- [ ] Token from a device running release N verifies; a debug build or modified image yields different measurements and fails policy.
- [ ] Replayed token with an old nonce is rejected.

## Checked

2026-10-28. Confirmed in the PSA Attestation API page (token attests components and serial numbers) and the TCG DICE Layering Architecture page (DICE as TCG specification). The TF-M measured boot guide URL returned 404 and was removed from reading; general DICE and verifier descriptions rely on the TCG page only for existence.
Removed: the exact CDI formula, `psa_initial_attest_get_token()`, `sw-components`, the 8+ slot count, SHA-256 and EAT claim names, Veraison and CoRIM names.

Method: documentation only; no commands were run.
