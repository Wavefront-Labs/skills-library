---
id: computing-software.firmware-embedded-development.iot-protocols.mcuboot-ota
name: mcuboot-ota
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mcuboot-ota, ota-update, mcuboot, bootloader, swap, image-ok, iot-protocols]
level: practitioner
status: docs-checked
description: "MCUboot image swap and confirm: slots, upgrade strategies, test/permanent/revert swap types, image trailer, signatures and boot flow."
sources:
  - https://docs.mcuboot.com/design.html
  - https://github.com/mcu-tools/mcuboot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MCUboot image swap and confirm

**Goal:** Use MCUboot for safe, signed, dual-slot updates.

## Steps
1. Each image has a primary slot (normal run location) and a secondary slot (upgrade candidate). Images must run from flash at a fixed location (not position-independent).
2. Strategies: swap using scratch (scratch at least as large as the largest swapped sector), swap using offset (stated preferred swap method, two status flags per sector), swap using move (three flags per sector), overwrite-only, direct-xip (equal slots, run from either) and RAM load.
3. Swap types: TEST (new image boots once and reverts on the next reset unless it marks itself OK), PERM (final, no revert), REVERT (restores the previous image). FAIL and PANIC make MCUboot hang rather than boot a bad image.
4. The image trailer at the end of each slot holds swap status, swap info, copy-done and image-ok flags (image-ok 0x01 = confirmed, 0xff = not confirmed) and a 16-byte magic.
5. Validation checks magic, TLV info, SHA256 and, if configured, the signature (RSA 2048/3072 PSS, ECDSA, ed25519), with keys embedded at build time and matched by hash.
6. Boot flow: resume any interrupted swap, check trailers for a requested swap (validate then swap, or erase and mark failure), then boot the primary image.
7. Direct-xip and RAM load pick the slot with the highest version. Software downgrade prevention (MCUBOOT_DOWNGRADE_PREVENTION) compares versions and needs overwrite-only mode.

## Gotcha
In a TEST swap, an image that never marks itself OK is reverted on the next reset, so every update appears to roll back.

## Verify
- [ ] New image boots and is marked OK, and stays after the next reset
- [ ] Unconfirmed image reverts
- [ ] Image signed with the wrong key is refused

## Checked

2026-11-08. Confirmed on the MCUboot design page: slots, strategies, swap types, trailer fields, validation and signature types, downgrade prevention, boot flow. Removed as not on the page: the imgtool sign command line, mcumgr and boot_set_pending/boot_set_confirmed names, CONFIG_BOOT_UPGRADE_ONLY and Zephyr Kconfig integration. The GitHub repository link is a landing page and was not relied on.
Method: documentation only; no commands were run.
