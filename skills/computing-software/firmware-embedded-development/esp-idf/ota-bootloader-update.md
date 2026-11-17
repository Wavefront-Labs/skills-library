---
id: computing-software.firmware-embedded-development.esp-idf.ota-bootloader-update
name: ota-bootloader-update
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, esp-bootloader-update, bootloader-ota, recovery-bootloader, secure-boot-bootloader, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Update the ESP-IDF second-stage bootloader in the field safely: when it is needed, the risk of bricking, chip support for recovery bootloader and verification."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/bootloader.rst
  - https://github.com/espressif/esp-idf/blob/master/examples/system/ota/partitions_ota/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating the bootloader over the air

Standard OTA replaces only the app. The second-stage bootloader (offset 0x1000 on ESP32; 0x0 on ESP32-S2, S3, C2, C3, C6, C61, H2;
0x2000 on the Key Manager targets C5, P4, S31, per the bootloader guide) has a single copy: if a bootloader write is interrupted, the device does not boot and
needs serial reflash. Avoid it unless you must.

## Do you need it
- Usually no: updating the bootloader is rarely necessary and generally not recommended (partitions_ota
  README); check the release notes of your IDF version for exceptions.
- Reasons: bootloader security fix, enabling features that live in the bootloader (flash
  encryption/secure boot enablement on first boot, new flash chip support, anti-rollback).

## Safe path on newer chips: recovery bootloader
Chips with `SOC_RECOVERY_BOOTLOADER_SUPPORTED` (ESP32-C5, C61, P4 and S31 in the current soc_caps;
not C6, C3 or S3) have ROM support for a recovery bootloader whose flash sector is held in the eFuse
field `ESP_EFUSE_RECOVERY_BOOTLOADER_FLASH_SECTOR` (default 0 = disabled; 0xFFF disables it
permanently). Set it with espefuse or `esp_efuse_set_recovery_bootloader_offset()`, choose the address
with `CONFIG_BOOTLOADER_RECOVERY_OFFSET` (multiple of 0x1000) and enable `CONFIG_BOOTLOADER_RECOVERY_ENABLE`.
Back up the primary bootloader to the recovery copy before updating; if the primary fails to load, the
ROM boots the recovery copy. Read the bootloader guide and the partitions_ota example README; the eFuse
write is permanent.

## Older chips: minimise risk
- The partitions_ota README warns that updating the bootloader and partition table is not safe: if the
  final copy to the destination is interrupted the chip may fail to boot, so do the final copy only when
  power is stable. Download into a passive app partition or staging area first and verify the image
  before copying.
- Ensure stable power (battery above threshold, no brownout margin issues) before starting.
- With Secure Boot v2 the new bootloader must be signed with a key whose digest is enrolled in eFuse;
  with flash encryption, check how the copy is encrypted (not covered by the pages read here).
- Keep the old partition table: changing it at the same time doubles the risk.

## Example
IDF ships `examples/system/ota/partitions_ota`, showing OTA updates of the application, bootloader,
partition table and storage partitions through the `esp_https_ota` APIs. Start from it rather than
hand-writing flash offsets. It states there is no rollback mechanism for non-application partitions.

## Verify
- [ ] Bench test: interrupt power at many points during update; count bricks (must be zero
  with recovery bootloader, quantified otherwise).
- [ ] `esptool.py read_flash` of bootloader region matches the intended image after update.
- [ ] Fleet rollout staged to a small cohort first.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in api-guides/bootloader.rst, soc_caps.h files and the partitions_ota README: bootloader offsets per chip, recovery bootloader eFuse field and its default and permanent-disable value, set function, CONFIG_BOOTLOADER_RECOVERY_OFFSET and CONFIG_BOOTLOADER_RECOVERY_ENABLE, SOC_RECOVERY_BOOTLOADER_SUPPORTED chip list, unsafe-update warning and no rollback for non-app partitions. Removed the unconfirmed SPI_FLASH_DANGEROUS_WRITE_ALLOWED claim, the IDF version numbers and the Secure Boot and flash-encryption copy specifics.

Method: documentation only; no commands were run.
