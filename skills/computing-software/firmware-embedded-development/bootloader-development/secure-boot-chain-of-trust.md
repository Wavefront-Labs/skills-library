---
id: computing-software.firmware-embedded-development.bootloader-development.secure-boot-chain-of-trust
name: secure-boot-chain-of-trust
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [secure-boot, chain-of-trust, root-of-trust, immutable-bootloader, rot, hsm, key-provisioning, public-key-pinning, signature-verification, ecdsa-p256, secure-element, atecc608, debug-lockout, fault-injection, glitch, bricking-risk, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build a secure boot chain of trust from an immutable first-stage bootloader: key provisioning, key pinning, verification order, debug lockout trade-offs, glitch risks."
sources:
  - https://trustedfirmware-m.readthedocs.io/en/latest/design_docs/booting/tfm_secure_boot.html
  - https://docs.mcuboot.com/design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure boot chain of trust

**Goal:** make every stage of boot cryptographically verify the next before
running it, rooted in something that can't itself be modified — distinct from
just signing OTA images (that's covered in
`computing-software.firmware-embedded-development.bootloader-development.ab-firmware-update-with-rollback`);
this is about the *boot-time* verification chain, not the update mechanism.

## The chain, stage by stage
1. **Root of trust (RoT)**: silicon-level immutable boot ROM (mask ROM, or OTP
   fuses that can be written once) that cannot be updated in the field. It
   verifies stage-1 bootloader's signature against a public key hash burned
   into fuses. If this stage is compromised, nothing above it can be trusted —
   this is why it's kept as small and simple as possible, often vendor-provided
   and not something you write yourself.
2. **Stage-1 (immutable or field-updatable with its own anti-rollback) verifies
   stage-2** (often the "real" bootloader, e.g. MCUboot) the same way.
3. **Stage-2 verifies the application image** before jumping to it.
Each stage verifies *only* the next, and only ever executes code after
verification succeeds — never "verify, and run anyway if it fails" as a
debug convenience left in production.

## Key provisioning
- Public key (or its hash, to save fuse space) is burned into one-time-
  programmable fuses or a secure element during manufacturing — this step is
  often the actual weak point: a provisioning line that reuses one key across
  every unit built means one leaked private key compromises the whole fleet.
  Per-device keys (provisioned via HSM at manufacture, with the private key
  never leaving the HSM) cost more in production tooling but bound the blast
  radius of a compromise to one device.
- Where available, a secure element holds the
  private key and performs signing/verification without it ever touching MCU
  RAM — relevant on the signing/manufacturing side, not the device's
  verification side (verification only ever needs the public key).

## Debug port lockout trade-off
A JTAG/SWD port left open after secure boot is enabled is a bypass: an attacker
with physical access can read out flash, extract keys or firmware, or write
arbitrary code directly, skipping the verification chain entirely. Locking the
debug port (the highest readout-protection level or equivalent fuses, per vendor) closes this but is
typically irreversible and kills your own field-debugging ability. Common
middle ground: ship with debug locked, keep a small fleet of unlocked
"engineering" units provisioned with different (non-production) keys for
debugging.

## Fault injection / glitching
Voltage or clock glitching can skip a single instruction — including the branch
that acts on a signature-verification failure — on parts without hardware
countermeasures. This is why security-certified RoT implementations double-
check critical branches (verify twice, compare), use redundant/non-linear
encodings for pass/fail state rather than a single flag bit, and why this
matters mainly for products facing a motivated, resourced attacker (payment,
access control) more than a typical IoT sensor — know which threat model
applies before over-building against it.

## Verify
- [ ] Every stage verifies the next's signature before any instruction of it executes, with no bypass path left reachable (not even a debug build flag) in production firmware.
- [ ] Public keys are provisioned per-device or per-batch, not one key hardcoded across the whole product line, unless the threat model explicitly accepts that risk.
- [ ] Debug port state (locked/unlocked) matches the intended production policy and was verified on a production-provisioned unit, not just an engineering sample.
- [ ] Anti-rollback counters (if used) are checked at every stage that could be downgraded to a vulnerable older signed image.

## Checked

2026-10-28. Confirmed in the TF-M secure boot design page: staged boot with an immutable first stage verifying the next stage, and upgrade of later stages. Replaced two dead source URLs (an NXP PDF that returned 404, a TF-M user guide root that returned 404) with the TF-M secure boot and MCUboot design pages.
Removed: named secure elements and the STM32 RDP level label. The rest of the skill is design guidance with no checkable figures.

Method: documentation only; no commands were run.
