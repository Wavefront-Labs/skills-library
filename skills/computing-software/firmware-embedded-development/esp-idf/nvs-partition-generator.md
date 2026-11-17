---
id: computing-software.firmware-embedded-development.esp-idf.nvs-partition-generator
name: nvs-partition-generator
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-storage, nvs-partition-gen, nvs-csv, factory-data, mass-manufacturing, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Generate per-device NVS partition images from CSV with nvs_partition_gen.py and the mfg_gen tool for factory data, optionally encrypted, and flash them."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/nvs_flash/nvs_partition_generator/README.rst
  - https://github.com/espressif/esp-idf/blob/master/tools/mass_mfg/docs/README.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/storage/nvs_encryption.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NVS partition generator

Use it to pre-load serial numbers, calibration, certificates or config into an NVS partition
at manufacturing, separate from the app.

## CSV format
```
key,type,encoding,value
factory,namespace,,
serial,data,string,SN-000123
hw_rev,data,u8,3
cal_offset,data,i32,-42
dev_cert,file,string,certs/dev123.pem
blob_cfg,file,binary,cfg.bin
```
Types: `namespace` (starts a namespace), `data`, `file`. Encodings: u8..u64, i8..i64, string,
hex2bin, base64, binary; for the `file` type only hex2bin, base64, string and binary are supported.

## Generate and flash
```bash
python $IDF_PATH/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py \
    generate factory.csv factory_nvs.bin 0x6000
esptool.py --chip esp32 write_flash 0x9000 factory_nvs.bin   # offset from partitions.csv
```
The size argument must equal the partition size and be a multiple of 4096 (minimum 0x3000).
The tool has subcommands `generate`, `generate-key`, `encrypt` and `decrypt`.

## Encrypted NVS
```bash
python nvs_partition_gen.py encrypt factory.csv out.bin 0x6000 --keygen
# writes <outdir>/keys/keys-<timestamp>.bin; flash it to the nvs_keys partition
```
`--inputkey FILE` reuses an existing key file instead. With flash encryption enabled, the `nvs_keys`
partition must be marked `encrypted` and the bootloader encrypts it on first boot. On chips with the
HMAC peripheral an HMAC-based scheme can derive the keys instead (`generate-key --key_protect_hmac`
and the `--kp_hmac_keygen` / `--kp_hmac_inputkey` options); check the nvs_encryption page for your target.

## Many devices: mfg_gen
```bash
python $IDF_PATH/tools/mass_mfg/mfg_gen.py generate config.csv values.csv Prefix 0x6000
```
`config.csv` holds the key schema and `values.csv` one row per device; the tool creates intermediate CSV
files and runs the NVS generator on them. The size must be a multiple of 4096.

## Reading on device
Open the partition by label so app data and factory data stay separate:
```c
nvs_flash_init_partition("factory");
nvs_open_from_partition("factory", "factory", NVS_READONLY, &h);
```
Keep factory data read-only from the app; a factory reset should erase only the app `nvs` partition.

## Verify
- [ ] Generated image decodes back (`nvs_partition_gen.py decrypt` for encrypted images; otherwise read keys on a test device and compare to CSV).
- [ ] Factory reset leaves the factory partition intact.
- [ ] Production log records serial to image mapping.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in the generator README (components/nvs_flash/nvs_partition_generator) and mass_mfg README: CSV columns and types, supported encodings and the file-type restriction, size multiple of 4096 and 0x3000 minimum, subcommands generate / generate-key / encrypt / decrypt, encrypt --keygen and --inputkey, keys/keys-<timestamp>.bin output, mfg_gen.py generate usage, nvs_keys partition encrypted on first boot. Fixed a wrong command (`--encrypt` is the `encrypt` subcommand), removed the unverified pip package name and the claim that there is no decoder.

Method: documentation only; no commands were run.
