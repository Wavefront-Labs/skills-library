---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.secure-boot-and-hardware-security-module
name: secure-boot-and-hardware-security-module
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [secure-boot, hsm, hardware-security-module, chain-of-trust, anti-rollback, key-management, code-signing]
level: practitioner
status: gated
description: "Design secure boot with an HSM: chain of trust, signature verification, key storage and provisioning, anti-rollback, debug lock and secure diagnostics."
sources:
  - "EVITA final publishable summary (https://trimis.ec.europa.eu/system/files/project/documents/20130702_175923_78998_EVITA_ProjectSummary.pdf)"
  - "Uptane Standard (https://uptane.org/docs/2.0.0/standard/uptane-standard)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Secure boot and hardware security module

1. **Chain of trust:** immutable ROM code or HSM verifies the first-stage bootloader's signature; each stage verifies the next (bootloader -> OS/application -> calibration data) before running.
2. Signature: hash (SHA-256 or stronger) and asymmetric signature (ECDSA or RSA of adequate size per current guidance) or a MAC (CMAC) for lighter systems; the public key or root hash is held in OTP or protected memory.
3. **HSM:** a separate secure core or peripheral (EVITA defines full, medium and light HSM classes; a simple SHE-style key store (gated: unconfirmed, source is paywalled or blocked) is a lighter option) that holds keys, performs crypto operations, and enforces key usage policy; main CPU never sees private keys.
4. Key management: unique per-ECU keys provisioned in a secure factory step, key hierarchy (root, intermediate, session), revocation or key update capability, and secure storage of counters.
5. **Anti-rollback:** a monotonic counter prevents flashing older, vulnerable firmware.
6. Debug and test interfaces: lock or authenticate JTAG, disable bootloader backdoors in production.
7. Secure diagnostics: UDS SecurityAccess with strong challenge-response (not simple seed-key) and authenticated flashing.
8. Time to boot: secure boot adds time; plan for the requirement (for example fast boot for CAN wake-up).
9. Test: boot with modified image and confirm refusal; fuzz the update interface.

**Gotchas:** shared keys across fleet; key leakage through supplier tools.

## Verify
- [ ] Tampered firmware fails verification and is not executed.
- [ ] Rollback attempt rejected by the anti-rollback counter.
