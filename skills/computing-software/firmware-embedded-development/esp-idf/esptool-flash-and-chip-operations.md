---
id: computing-software.firmware-embedded-development.esp-idf.esptool-flash-and-chip-operations
name: esptool-flash-and-chip-operations
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-debug, esptool, esptool-write-flash, read-flash, chip-id, merge-bin, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use esptool for ESP32 flashing and inspection: write_flash with offsets, read_flash backups, erase, chip_id/flash_id, merge_bin for factory images and baud/reset troubleshooting."
sources:
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/index.html
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html
  - https://docs.espressif.com/projects/esptool/en/latest/esp32/migration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esptool

`idf.py flash` calls esptool for you; use esptool directly for production, recovery and
inspection. In esptool v5 the console script is `esptool` (no `.py`) and commands and options use
dashes (`write-flash`, `--before default-reset`); the `.py` scripts and underscore names still run
with a deprecation warning and are slated for removal in the next major release.

## Identify
```bash
esptool --port PORT chip-id             # chip type, revision, MAC
esptool --port PORT flash-id            # flash manufacturer/size
esptool --port PORT read-mac
```

## Flash
```bash
esptool --chip esp32s3 -p PORT -b 921600 --before default-reset --after hard-reset \
  write-flash --flash-mode dio --flash-size detect --flash-freq 80m \
  0x0 bootloader.bin 0x8000 partition-table.bin 0x10000 app.bin
cd build && esptool --chip esp32s3 write-flash @flash_args         # offsets from the build
```
Bootloader offset (esptool targets): 0x1000 on ESP32 and S2, 0x0 on C3/S3/C6/H2, 0x2000 on P4/C5.

## Factory single image
```bash
esptool --chip esp32s3 merge-bin -o factory.bin --flash-mode dio --flash-size 8MB \
  0x0 bootloader.bin 0x8000 partition-table.bin 0xd000 ota_data_initial.bin 0x10000 app.bin
esptool write-flash 0x0 factory.bin
```

## Backup and erase
```bash
esptool -p PORT read-flash 0 ALL backup.bin         # ALL autodetects the flash size
esptool -p PORT erase-flash                          # wipes NVS, secure cert partition too
esptool -p PORT erase-region 0x9000 0x6000          # just NVS; address and length are multiples of 4096
```

## Connection troubleshooting
| Error | Fix |
|---|---|
| `No serial data received` | hardware or reset problem: check RX/TX wiring and the reset into download mode; enter download mode manually (hold the BOOT button while pressing EN) |
| Random errors part way through flashing | retry with a lower baud rate (`-b 115200`, or `-b 9600` to rule out baud) |
| `Invalid head of packet` | serial noise or corruption: bad USB cable, breadboard shorting the SPI flash pins, or brown-out while flashing |
| USB-Serial-JTAG chip disappears after app starts | the app reconfigured or disabled the USB pins; enter download mode manually, run `erase-flash`, fix the app |
| Secure Download Mode enabled | flash cannot be read, RAM cannot be read or written, `erase-flash` is unavailable (use `erase-region` on 4096-byte aligned regions), and the flasher stub cannot be used |

## Verify
- [ ] `write-flash` ends with "Hash of data verified".
- [ ] Factory image boots on a blank board with no other steps.

## Checked

Checked against the esptool repository docs (docs/en, master; latest release v5.6.0 on 2026-10-15) and esptool/targets sources.
Confirmed: v5 migration guide (console scripts without .py, underscore command and option names and `default_reset` style reset modes deprecated but still working with a warning); `write-flash`, `read-flash ... ALL`, `erase-region` (multiples of 4096), `merge-bin` including `@flash_args` and `--flash-mode/--flash-size/--flash-freq`; BOOTLOADER_FLASH_OFFSET in targets (ESP32 0x1000, S2 inherits ESP32 0x1000, S3/C3/C6 0x0, H2 inherits C6 0x0, P4/C5 0x2000); troubleshooting entries (no serial data, invalid head of packet causes, lower baud advice, USB-Serial/JTAG pin reconfiguration, Secure Download Mode limits). Removed unconfirmed details: the esptool 4.6 version gate for ALL, the EN RC delay capacitor remark, the `--no-stub` advice for Secure Download Mode and the claim that another program holding the port causes "Invalid head of packet".

Method: documentation only; no commands were run.
