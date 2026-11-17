---
id: computing-software.firmware-embedded-development.esp-idf.efuse-management
name: efuse-management
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, efuse, espefuse, virtual-efuse, custom-efuse-table, esp-efuse-read-field-blob, manufacturing-provisioning, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Read, burn and protect ESP32 eFuses with espefuse.py and the esp_efuse API: summaries, custom user fields, virtual eFuses for testing, and production provisioning rules."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/efuse.rst
  - https://github.com/espressif/esptool/blob/master/docs/en/espefuse/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eFuse management

eFuses are one-time-programmable bits: a bit goes 0 to 1 once, never back. They hold the MAC,
chip revision, calibration, security config (flash encryption, secure boot, JTAG disable),
keys, and user blocks for your own data (serial numbers, hardware revision).

## Inspect
```bash
espefuse -p PORT summary               # all fields, values, R/W protection
espefuse -p PORT summary --format json --file efuse.json
idf.py -p PORT efuse-summary           # same via idf.py
espefuse -p PORT dump                  # raw blocks
```

## Burn
```bash
espefuse -p PORT burn-efuse DIS_USB_JTAG 1                 # named field (several fields can be given in one command)
espefuse -p PORT burn-key BLOCK_KEY1 hmac_key.bin HMAC_UP
espefuse -p PORT burn-block-data BLOCK3 serial.bin
espefuse -p PORT write-protect-efuse BLOCK3
espefuse -p PORT read-protect-efuse BLOCK_KEY1
```
espefuse v5 is invoked without `.py` and uses hyphenated command names; the older `espefuse.py` and underscore forms (`burn_efuse`) are deprecated. It asks for confirmation (type `BURN`); scripts use `--do-not-confirm`. `--virt --chip <chip>` runs the tool in a virtual mode without a chip, for testing commands first. `burn-block-data` is for non-key data; use `burn-key` for keys.

## Practise with virtual eFuses
```
CONFIG_EFUSE_VIRTUAL=y
CONFIG_EFUSE_VIRTUAL_KEEP_IN_FLASH=y   # persist across resets in an efuse_em partition
```
`CONFIG_EFUSE_VIRTUAL` virtualises eFuse values inside the eFuse Manager so writes are emulated and nothing is permanently burned. With `KEEP_IN_FLASH`, the partition table needs an `efuse_em` partition (type `data`, subtype `efuse`). `espefuse --virt` is the host-side equivalent. Turn virtual eFuses off for production builds.

## Custom fields for your data
`main/esp_efuse_custom_table.csv`:
```
# field_name,     efuse_block, bit_start, bit_count, comment
SERIAL_NUMBER,    EFUSE_BLK3,  0,         64,        Device serial
HW_REVISION,      EFUSE_BLK3,  64,        8,         PCB revision
```
```
CONFIG_EFUSE_CUSTOM_TABLE=y
CONFIG_EFUSE_CUSTOM_TABLE_FILENAME="main/esp_efuse_custom_table.csv"
```
`idf.py efuse-custom-table` generates `esp_efuse_custom_table.c` and the header. Rows may omit `bit_start` to follow the previous record in the same block. Then:
```c
#include "esp_efuse.h"
#include "esp_efuse_custom_table.h"
uint64_t sn = 0;
esp_efuse_read_field_blob(ESP_EFUSE_SERIAL_NUMBER, &sn, 64);
uint8_t mac[6];
esp_efuse_read_field_blob(ESP_EFUSE_MAC_FACTORY, mac, 48);
```
Writing from firmware: `esp_efuse_write_field_blob` (wrap several in
`esp_efuse_batch_write_begin/commit`). Prefer burning at the factory station, not from the app.

## Rules
- Some chips use an eFuse coding scheme (ESP32: 3/4 or Repeat, selected by `CONFIG_EFUSE_CODE_SCHEME_SELECTOR`; Reed-Solomon on newer chips), which reduces the usable bits per block. Plan the full content before the first burn.
- Write-protect user blocks after burning so later firmware or an attacker can't add bits.
- `burn-key` read- and write-protects flash encryption and secure boot v1 keys by default; for other purposes such as HMAC, check the protection flags in `summary`.
- Log the `summary --format json` of every produced unit in the manufacturing database.

## Verify
- [ ] Full provisioning flow rehearsed with virtual eFuses, then on a sacrificial board.
- [ ] Custom table fields read back correctly in firmware.
- [ ] Production builds have `CONFIG_EFUSE_VIRTUAL` off.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the ESP-IDF eFuse manager page, Kconfig and the esptool v5 espefuse docs: one-way 0 to 1 burning, summary --format json --file, dump, burn-efuse, burn-key, burn-block-data, read/write-protect-efuse, BURN confirmation and --do-not-confirm, --virt, CONFIG_EFUSE_VIRTUAL and KEEP_IN_FLASH with the efuse_em partition, custom CSV columns, CONFIG_EFUSE_CUSTOM_TABLE and _FILENAME, idf.py efuse-summary and efuse-custom-table, esp_efuse_read/write_field_blob and batch write API, coding schemes. Wrong for current tooling: espefuse.py with underscore commands (burn_efuse, burn_key, write_protect_efuse) were renamed in esptool v5; JTAG_SEL_ENABLE and BLOCK_USR_DATA examples replaced by documented names. Removed the unconfirmed hardenconfig claim.
Method: documentation only; no commands were run.
