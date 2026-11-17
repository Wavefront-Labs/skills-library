---
id: computing-software.firmware-embedded-development.esp-idf.raw-partition-access
name: raw-partition-access
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-storage, esp-partition, esp-partition-api, custom-partition, flash-mmap, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read, erase and write custom flash partitions directly with the esp_partition API, including memory-mapped reads and flash-encryption aware access."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/partition.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/partition-tables.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_partition/include/esp_partition.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw partition access

For data that needs no file system: audio clips, ML models, ring-buffer logs, firmware for a
co-processor.

## Declare
```
# partitions.csv
# Name,  Type, SubType, Offset, Size, Flags
model,   0x40, 0x01,    ,       1M,
```
Custom data types use 0x40-0xFE; subtypes are yours.

## Find and access
```c
#include "esp_partition.h"
const esp_partition_t *p = esp_partition_find_first(0x40, 0x01, "model");
assert(p);
ESP_ERROR_CHECK(esp_partition_erase_range(p, 0, 64 * 1024));   /* offset and size must be multiples of p->erase_size */
ESP_ERROR_CHECK(esp_partition_write(p, 0, data, len));
ESP_ERROR_CHECK(esp_partition_read(p, 0, buf, len));
```
Erase before writing: `esp_partition_write` documents that the flash must have been erased with
`esp_partition_erase_range` first (NOR flash writes can only clear bits). Offsets and lengths are checked against the
partition bounds (`ESP_ERR_INVALID_SIZE`) and a partition with the `readonly` flag returns `ESP_ERR_NOT_ALLOWED`.

## Memory-map large read-only data
```c
const void *ptr; esp_partition_mmap_handle_t h;
ESP_ERROR_CHECK(esp_partition_mmap(p, 0, p->size, ESP_PARTITION_MMAP_DATA, &ptr, &h));
run_model(ptr);              /* reads through the cache, no RAM copy */
esp_partition_munmap(h);
```
MMU address space is limited (the header quotes 4 MB of data window on ESP32); map only what you need. Offsets need not be 64 kB aligned, but the mapping is rounded down to a 64 kB boundary. While a mapped region exists, erasing or programming flash disables the cache (unless you pass `ESP_PARTITION_MMAP_BLOCKS_WRITE`, which blocks erase and write until unmap).

## Flash encryption
If the partition has the `encrypted` flag and flash encryption is enabled, `esp_partition_write` and `esp_partition_read`
encrypt and decrypt transparently (reads through a cache mapping); writes to an encrypted partition need offsets and lengths that are
multiples of 16 bytes. `esp_partition_write_raw` and `esp_partition_read_raw` never transform data. App, bootloader,
partition table, `data/ota` and `data/nvs_keys` partitions are always encrypted regardless of the flag. Data written by a host tool to an encrypted
partition must be encrypted for the device (see the flash encryption guide).

## Flash from host
```bash
parttool.py --port PORT write_partition --partition-name model --input model.bin
parttool.py read_partition --partition-name model --output dump.bin
```

## Pitfalls
- Erase and program operations temporarily disable the flash cache, so code that runs from flash (including ISRs not placed in IRAM) cannot execute meanwhile.
- Large erases take time; erase in chunks (a design suggestion, size them from measurement).
- Track validity with a header (magic, length, CRC) so an interrupted write is detected.

## Verify
- [ ] Header/CRC check rejects a half-written partition.
- [ ] mmap data matches the host file byte for byte.

## Checked

Checked against ESP-IDF v6.1 (components/esp_partition/include/esp_partition.h, docs/en/api-reference/storage/partition.rst, docs/en/api-guides/partition-tables.rst).
Confirmed: custom partition types 0x40-0xFE (types up to 0x3F reserved for ESP-IDF core use); `esp_partition_find_first`, `esp_partition_read`, `esp_partition_write` (erase first), `esp_partition_erase_range` (aligned to `erase_size`), `esp_partition_mmap` and `esp_partition_munmap`, `ESP_PARTITION_MMAP_DATA`, the 64 kB rounding and cache-disable behaviour, the 4 MB data window note, encrypted-flag behaviour with the 16-byte write rule and the `_raw` variants, the always-encrypted partition list, and the `parttool.py` `write_partition`/`read_partition` subcommands with `--partition-name`, `--input`, `--output`. Removed unconfirmed claims: the 4096-byte erase constant, safe concurrent erase across cores, the interrupt crash claim for non-IRAM ISRs (replaced by the documented cache-disable effect), and plaintext behaviour of unflagged partitions (corrected).

Method: documentation only; no commands were run.
