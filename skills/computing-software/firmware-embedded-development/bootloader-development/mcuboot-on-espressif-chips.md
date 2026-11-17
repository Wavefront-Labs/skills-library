---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-on-espressif-chips
name: mcuboot-on-espressif-chips
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcuboot-espressif, mcuboot, esp32-mcuboot, zephyr-esp32, flash-encryption-mcuboot, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use MCUboot instead of the ESP-IDF second-stage bootloader on ESP32 parts: Espressif port build, Zephyr sysbuild, signing, secure boot and flash encryption, downgrade prevention."
sources:
  - https://docs.mcuboot.com/readme-espressif.html
  - https://docs.zephyrproject.org/latest/boards/espressif/esp32_devkitc/doc/index.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/bootloader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MCUboot on Espressif chips

The ESP-IDF flow boots the ROM bootloader, then the ESP-IDF second stage bootloader (at flash
address 0x1000 on ESP32). MCUboot's Espressif port is a second stage bootloader that replaces it
(the ROM bootloader is the first stage). The port supports Zephyr and NuttX and has a
standalone build that uses ESP-IDF as the HAL source.

## Building the Espressif port (standalone)
From the MCUboot docs (replace `<TARGET>` with the chip family such as `esp32`, `esp32s2`):
```sh
cd <MCUBOOT_DIR>/boot/espressif
cmake -DCMAKE_TOOLCHAIN_FILE=tools/toolchain-<TARGET>.cmake -DMCUBOOT_TARGET=<TARGET> \
      -DESP_HAL_PATH=<ESP_HAL_PATH> -DMCUBOOT_FLASH_PORT=<PORT> -B build -GNinja
ninja -C build/
ninja -C build/ flash
```
`ESP_HAL_PATH` can be omitted when ESP-IDF is the HAL source. Slot partitioning and MCUboot
features are set in `port/<TARGET>/bootloader.conf` (or a file passed with
`-DMCUBOOT_CONFIG_FILE`), for example `CONFIG_ESP_IMAGE0_PRIMARY_START_ADDRESS`,
`CONFIG_ESP_IMAGE_NUMBER` (multi-image is limited to 2 images) and `CONFIG_ESP_SCRATCH_OFFSET`.
To flash with esptool directly, write `build/mcuboot_<TARGET>.bin` at the bootloader offset
for the chip: 0x1000 (ESP32, ESP32-S2), 0x0 (ESP32-C3, S3, C2, C6, H2, C61), 0x2000 (ESP32-C5, P4).
**Erase the secondary slot and scratch area before the first boot** (`esptool.py -p <PORT> erase_flash`):
the erased value (0xFF) read from the trailers is part of MCUboot's update-state check, and
garbage there can be read as a valid state.

## Signing an application
```sh
imgtool.py sign --align 4 -v 0 -H 32 --pad-header -S <SLOT_SIZE> <BIN_IN> <SIGNED_BIN>
```
`<SLOT_SIZE>` is the slot size (the default slot0 size is 0x100000). For Zephyr images
`--pad-header` is not needed. This only adds the header and trailer; for authenticity configure
signature verification: `CONFIG_ESP_SIGN_EC256`, `CONFIG_ESP_SIGN_ED25519` (with
`CONFIG_ESP_USE_TINYCRYPT`) or `CONFIG_ESP_SIGN_RSA` with `CONFIG_ESP_SIGN_RSA_LEN` (with
`CONFIG_ESP_USE_MBEDTLS`), plus `CONFIG_ESP_SIGN_KEY_FILE`, and sign with `imgtool.py sign -k <key>
--pad --pad-sig --align 4 ...`. The docs recommend generating your own signing key with imgtool
instead of using the samples. Flash the signed image at the slot offset with `esptool.py write_flash`.

## Zephyr
```sh
west build -b esp32_devkitc/esp32/procpu --sysbuild samples/hello_world
west flash
```
The Zephyr ESP32 DevKitC page says the ESP32 sysbuild creates the MCUboot bootloader and
application images by default, and that a plain `west build` (no `--sysbuild`) is a Simple Boot
image with no MCUboot. Zephyr uses the partitions `boot_partition` and `slot0_partition` (plus the
others from the MCUboot Zephyr readme) in the board devicetree.

## Downgrade prevention
`CONFIG_ESP_DOWNGRADE_PREVENTION=y` compares the image version (imgtool `-v`) with the current one
before a swap. `CONFIG_ESP_DOWNGRADE_PREVENTION_SECURITY_COUNTER=y` uses the security counter
(imgtool `-s`) instead: an update must have a greater or equal counter, so some downgrade remains possible.

## Secure boot and flash encryption
- MCUboot's own encrypted images do not give full code confidentiality on a chip with only
  off-chip flash, because the primary slot (executed from) is stored in plaintext; the port
  therefore adds hardware-assisted Secure Boot and Flash Encryption.
- Secure Boot is based on ESP-IDF Secure Boot V2 (RSA based, except ESP32-C2 and ESP32-C61 which
  use ECDSA); the ROM bootloader verifies the MCUboot image, so the ROM is first stage and MCUboot
  second stage. Options in `bootloader.conf` include `CONFIG_SECURE_BOOT=1` and
  `CONFIG_SECURE_BOOT_V2_ENABLED=1`.
- Flash Encryption: `CONFIG_SECURE_FLASH_ENC_ENABLED=1` with
  `CONFIG_SECURE_FLASH_ENCRYPTION_MODE_RELEASE=1` or `_DEVELOPMENT=1`. The first boot encrypts the
  flash including bootloader, slots and scratch and burns eFuses that cannot be undone; a device
  generated key is not recoverable. Sign images with `--pad --align 32 --max-align 32` when flash
  encryption is on.
- Using Secure Boot, Flash Encryption and signature verification together may push the bootloader
  size past the ROM bootloader's fixed limit (MCUboot issue 1262).

## Differences from the IDF bootloader
`imgtool sign` adds the MCUboot header and trailer to the application image. Updates are written
to the secondary slot and MCUboot performs the swap.

## Verify
- [ ] Boot log shows MCUboot starting, then the application.
- [ ] An upgrade swaps and confirms correctly; an unconfirmed image reverts.

## Checked
2026-10-31. Confirmed against the MCUboot Espressif page (build commands, bootloader offsets, erase advice, signing
command, `CONFIG_ESP_*` options, downgrade prevention, Secure Boot V2 and flash encryption statements), the Zephyr
ESP32 DevKitC page (sysbuild default, plain build has no MCUboot, board target) and the ESP-IDF bootloader guide
(second stage at 0x1000). Removed: `esp32.cmake` and `mcuboot_esp32.bin` fixed names, `storage_partition`,
`esp_image_header_t`/`esp_ota_*`/`otadata` claims, the 64 KB MMU alignment, and the boot log expectations.
Method: documentation only; no commands were run.
