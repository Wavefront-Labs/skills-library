---
id: computing-software.firmware-embedded-development.bootloader-development.delta-firmware-updates
name: delta-firmware-updates
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [delta-update, differential-ota, binary-diff, detools, bsdiff, janpatch, patch-apply, base-version-check, fota, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Ship delta (differential) firmware updates to MCUs: choosing a diff algorithm, base image verification, applying into the update slot with bounded RAM, signing the result."
sources:
  - https://github.com/eerimoq/detools
  - https://www.daemonology.net/bsdiff/
  - https://github.com/janjongboom/janpatch
  - https://docs.mcuboot.com/design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta updates

**Goal:** cut OTA payload size for
cellular/LoRa/BLE fleets, without weakening the boot-time integrity checks.

## Architecture that keeps security intact
1. Build and **sign the full new image** as usual.
2. On the server, diff the **signed old image** (exactly what the device runs) against the
   signed new image to make the patch.
3. Device downloads the patch, verifies its own envelope (hash/signature of the patch or a
   manifest), checks the **base image hash** matches its running slot.
4. Device applies the patch reading the old image from the primary slot and writing the
   reconstructed image into the secondary/update slot.
5. Bootloader (MCUboot or yours) validates the reconstructed image's signature exactly as for a
   full update, swaps, and the test/confirm rollback flow proceeds unchanged.
The bootloader never needs to know a delta was used.

## Algorithms for MCUs
| Tool | Notes |
|---|---|
| detools | binary delta encoding tools (Python, with a C library for applying patches); check its docs for patch types and compression |
| bsdiff + bspatch | very small patches but classic bspatch needs RAM for whole images; use streaming variants |
| JojoDiff + janpatch | janpatch is a memory-efficient C library that applies JojoDiff patches over basic I/O primitives |
| vendor | check each SDK for delta-update support |
Choose by **apply-time RAM** (a few KB page buffer) and whether the target can apply to a
separate slot (simple) or must patch in place (no second slot; complex and power-fail-unsafe
unless the algorithm is designed for it).

## Making patches small
- Reproducible builds: same toolchain, flags, path prefix maps, no
  timestamps embedded; otherwise every build differs everywhere.
- Linker layout stability: inserting code early shifts all addresses; diff algorithms handle
  shifts partially. Keep libraries in fixed order; consider placing frequently changing code last.
- Compression of the full image defeats diffing - diff uncompressed images, then compress the patch.

## Fleet management
- The server must know each device's exact running build (report the image hash, not just a
  version string) and keep patches per base version; fall back to full images for unknown or
  very old bases.
- If apply fails (base mismatch, power loss mid-write), erase the update slot and retry; the
  running image was never touched.

## Verify
- [ ] Reconstructed image hash on device equals the server's full image hash before reboot.
- [ ] Power cut during apply: device keeps running the old image and retries successfully.
- [ ] Patch for wrong base version is rejected before any flash write.

## Checked

2026-10-28. Confirmed in the detools GitHub page (binary delta encoding tools, C directory), the janpatch README (memory-efficient JojoDiff patch applier for delta firmware updates) and the bsdiff page; MCUboot design page for swap and test/confirm flow.
Removed: the 5-20 percent saving figure, the detools command line, compression names, `esp_delta_ota`, `-ffile-prefix-map` and `imgtool sign` (not on the fetched pages).

Method: documentation only; no commands were run.
