---
id: computing-software.firmware-embedded-development.bootloader-development.recovery-mode-and-unbrick-strategy
name: recovery-mode-and-unbrick-strategy
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader, recovery-mode, dfu, bricking, golden-image, uart-recovery, boot-pin-strap, factory-reset, usb-dfu, stm32-system-bootloader, force-recovery, field-recoverable, unbrick, firmware-embedded-development]
level: advanced
status: draft
description: "Design a bootloader's recovery path so a bad update, corrupted slot or user mistake never permanently bricks the device: strap-pin entry, golden image, and vendor DFU fallback."
sources:
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-an2606-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovery mode and unbrick strategy for bootloaders

**Goal:** guarantee there is always a way back from a corrupted application
image, a failed OTA, or a user mistake — a different concern from the
rollback-after-bad-update logic in
`computing-software.firmware-embedded-development.bootloader-development.ab-firmware-update-with-rollback`,
which assumes the bootloader itself is healthy. This skill covers what happens
when it isn't, or when there's no second slot to fall back to at all.

## Layered recovery, cheapest-and-most-reliable first
1. **Vendor ROM bootloader (hardware strap)**: most MCUs have a factory-masked
   bootloader entered via a boot-pin strap (e.g. STM32's BOOT0 pin, or a
   hold-button combination) that talks UART/USB/I2C and can reprogram flash
   regardless of what your own bootloader or application did. This is the
   ultimate fallback and cannot itself be bricked by firmware — know the exact
   strap sequence for your MCU family and keep it reachable on the PCB (a test
   point or accessible pin, not buried under a BGA) at design time, not after
   the first field brick.
2. **Your own recovery/golden image**: a known-good, rarely-updated image kept
   in a protected flash region your normal bootloader always falls back to if
   the primary application slot fails validation (bad CRC/signature, repeated
   failed-boot count exceeded). Must be written once at manufacture and
   write-protected afterward — if it's field-updatable by the same path that
   can corrupt the primary slot, it's not actually a fallback.
3. **A forced-recovery entry condition** reachable without the application
   running: a GPIO strap sampled very early in your bootloader (before
   jumping anywhere), a magic value in a non-volatile register set by the
   application before a deliberate reboot-to-recovery, or a UART break
   condition held during boot. Document this for whoever does field support —
   an unbrick procedure nobody remembers is as good as none.

## Boot counting and failure thresholds
Increment a boot-attempt counter (in a register that survives reset but not
power-on, or in flash/EEPROM) before jumping to the application; the
application clears it once it proves itself up (e.g. after N seconds running,
or after a specific "I'm healthy" call). If the counter exceeds a threshold
without being cleared, the bootloader falls back to recovery automatically —
this is the same trial-boot pattern used for OTA rollback, generalized to any
cause of a non-booting application, not just a bad update.

## What actually bricks a device permanently
- Erasing or corrupting the vendor ROM bootloader's entry condition itself
  (rare, usually requires actively fighting the hardware strap).
- Setting irreversible protection (RDP level 2, debug-lockout fuses) before
  the recovery path is proven working — test the full recovery flow *before*
  enabling any one-way protection in production.
- A recovery image that depends on the same clock/pin configuration the bad
  application left behind (e.g. application reconfigured a pin needed for the
  recovery UART) — recovery code must reset relevant peripherals to known
  states itself, not assume a clean slate.

## Verify
- [ ] The hardware strap/vendor ROM bootloader entry sequence is documented and was tested on a production (not just dev-kit) board.
- [ ] A golden/recovery image exists, is write-protected after manufacture, and was verified to boot standalone.
- [ ] Boot-attempt counting and automatic fallback were tested by deliberately flashing a broken application image.
- [ ] Any irreversible protection (RDP2, debug fuses) is enabled only after the full recovery path was proven on that exact hardware revision.
