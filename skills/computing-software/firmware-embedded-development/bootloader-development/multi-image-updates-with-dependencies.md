---
id: computing-software.firmware-embedded-development.bootloader-development.multi-image-updates-with-dependencies
name: multi-image-updates-with-dependencies
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [multi-image-update, ab-update, mcuboot-multi-image, dependency-tlv, network-core-update, firmware-embedded-development]
level: sme
status: docs-checked
description: "Update several images together (secure + non-secure, app + network core, MCU + co-processor) with MCUboot dependencies or an orchestrated sequence."
sources:
  - https://docs.mcuboot.com/design.html
  - https://docs.mcuboot.com/imgtool.html
  - https://docs.mcuboot.com/readme-zephyr.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-image updates with dependencies

Products often run several firmware images that must stay compatible: a secure image plus a
non-secure app, an application core plus a network core, a main MCU plus a radio module or FPGA
bitstream. Updating one without the other can leave the device unable to communicate internally.

## MCUboot multi-image
Zephyr: `CONFIG_UPDATEABLE_IMAGE_NUMBER=2` ("Number of updateable images", default 1) enables
multi-image update; each image has its own primary/secondary slot pair (for image 1,
`slot2_partition` and `slot3_partition`). Dependencies are declared at signing time as protected
TLV entries (`IMAGE_TLV_DEPENDENCY`):
```sh
imgtool sign --key <signing-key>.pem --version 2.1.0 \
    --dependencies "(1, 1.4.0)" \
    --header-size 0x400 --slot-size 0x60000 app.bin app.signed.bin
```
The format is `(<image_ID>, <image_version>)`; the version is the minimum needed (imgtool's
example is `-d "(1, 1.2.3+0)"`). Here: image 0 version 2.1.0 requires image 1 at 1.4.0 or newer.
MCUboot finalises aborted swaps, determines the swap type of every image, then checks all
dependencies; if one is not satisfied the swap type of that image is changed (an update is not
applied, or a revert is applied together with the other image) and the check restarts. There is
always at least one valid configuration; in the worst case the system returns to its initial state.

## Orchestrated updates (external co-processors)
For a Wi-Fi module, a second MCU over UART, or an FPGA that MCUboot does not manage:
1. Download all images first and verify signatures.
2. Update the component that can tolerate both old and new peers first (design protocols with
   version negotiation so N and N+1 interoperate).
3. Update the next, verify it reports the new version, then confirm the main image last.
4. If any step fails, roll back the already-updated components or keep a compatible fallback.
Record the state of the multi-step update in persistent storage so a reset mid-sequence resumes
correctly.

## Version compatibility contract
- Maintain a compatibility matrix (app vX works with netcore >= Y) in the release process.
- Prefer backward-compatible inter-image protocols (versioned IPC messages) so strict lockstep
  is not required.
- Package the set as one release artefact with a manifest listing all images and their versions
  so the server never deploys half a release.

## Verify
- [ ] Deploying only the dependent image without its dependency: upgrade refused or reverted.
- [ ] Power-cut during each step of a multi-image update ends in a consistent, working pair.

## Checked
2026-10-31. Confirmed against the MCUboot design doc (multiple image boot, dependency check, `IMAGE_TLV_DEPENDENCY`),
the imgtool page (`--dependencies` format and example), the MCUboot Zephyr readme (slot2/slot3 for image 1) and
`boot/zephyr/Kconfig` (`UPDATEABLE_IMAGE_NUMBER`). Removed: `MCUBOOT_IMAGE_NUMBER = 2`, the nRF5340 network core
section (PCD, `SB_CONFIG_NETCORE_APP_UPDATE`, `dfu_application.zip`; the Nordic page is blocked to scripts), the
sample log line, and the SUIT mention.
Method: documentation only; no commands were run.
