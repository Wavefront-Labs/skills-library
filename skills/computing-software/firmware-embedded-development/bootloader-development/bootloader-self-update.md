---
id: computing-software.firmware-embedded-development.bootloader-development.bootloader-self-update
name: bootloader-self-update
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader-self-update, bootloader-architecture, two-stage-bootloader, brick-risk, immutable-boot, firmware-embedded-development]
level: sme
status: docs-checked
description: "Update the bootloader itself without bricking: immutable first stage plus updatable second stage, A/B bootloader banks, or a guarded in-place rewrite."
sources:
  - https://docs.mcuboot.com/design.html
  - https://trustedfirmware-m.readthedocs.io/en/latest/design_docs/booting/tfm_secure_boot.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/bootloader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootloader self-update

The bootloader is the one component whose failed update cannot be recovered by the bootloader.
A power cut while erasing its first sector bricks the device unless the design plans for it.
First question: do you really need it? Keeping the bootloader minimal and **never** updating it
(immutable) is the most robust design and a common security requirement (root of trust).

## Option 1: immutable stage 1 + updatable stage 2
```
| stage 1 (tiny, write-protected, never updated) | stage 2 slot A | stage 2 slot B | app slots ... |
```
Stage 1 only validates (CRC/signature) and selects a stage-2 slot, falling back to the other on
failure. Stage 2 contains the update logic, transports and crypto that may need fixes. This is the
two-stage model of TF-M BL1/BL2 (immutable ROM stage plus an updatable BL2) and of the ESP-IDF
second-stage bootloader loaded by ROM code.

## Option 2: A/B bootloader slots with hardware bank swap
Dual-bank flash parts (check the vendor reference manual for the bank-swap option bit) let the boot address switch
between banks atomically: write the new bootloader+app into the inactive bank, verify, flip the
option bit, reset. If the new bank fails to boot, a watchdog reset plus logic in the old bank (or
the ROM checking validity) flips back.

## Option 3: guarded in-place rewrite (last resort)
1. Application receives and verifies the new bootloader image (signature, version) into a staging
   area.
2. Disable interrupts, refresh the watchdog with long timeout or avoid starting it, ensure power is
   sufficient (battery level check, supercap).
3. Erase and program the bootloader sector(s) from code running in RAM (or in the app region),
   verify by readback and CRC, retry on mismatch.
4. Only then reset.
The window of vulnerability is the erase/program time (measure it on your part). Keep a recovery
path that doesn't depend on the bootloader: ROM system bootloader via BOOT pin, SWD access
(if not locked), or the ROM's own DFU.

## Rules that apply to all options
- Version the bootloader and the bootloader-app interface (shared RAM layout, header format) and
  keep the app compatible with old bootloaders still in the field.
- Write protection (WRP/PCROP/secure boot locks) must be lifted and restored correctly; test that
  the lock state after update matches production.
- Anti-rollback for the bootloader (OTP counters) if it is part of the chain of trust.

## Verify
- [ ] Power-cut test at random points during a bootloader update: device recovers (options 1/2) or the vulnerable window is measured and documented (option 3).
- [ ] New app runs on both old and new bootloader versions.

## Checked

2026-10-28. Confirmed in the TF-M secure boot page (BL1 and BL2 stages, upgradeable BL2 versus immutable ROM stage) and the ESP-IDF bootloader guide (ROM loads the second-stage bootloader).
Removed: the specific STM32 option-bit names (vendor reference manual not fetchable here), the claim that MCUboot is the ROM+stage model, and the erase-time range.

Method: documentation only; no commands were run.
