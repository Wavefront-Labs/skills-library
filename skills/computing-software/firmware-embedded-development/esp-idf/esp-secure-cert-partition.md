---
id: computing-software.firmware-embedded-development.esp-idf.esp-secure-cert-partition
name: esp-secure-cert-partition
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, esp-secure-cert, esp-secure-cert-mgr, device-identity, manufacturing-partition, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Provision per-device certificates and keys into the esp_secure_cert partition with esp_secure_cert_mgr and read them from firmware for TLS, DS and cloud onboarding."
sources:
  - https://github.com/espressif/esp_secure_cert_mgr
  - https://github.com/espressif/esp_secure_cert_mgr/blob/main/tools/README.md
  - https://github.com/espressif/esp_secure_cert_mgr/blob/main/include/esp_secure_cert_read.h
  - https://components.espressif.com/components/espressif/esp_secure_cert_mgr
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/partition-tables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_secure_cert partition

A dedicated partition (custom type 0x3F, named `esp_secure_cert`) holding device identity: certificate,
CA, private key or DS context. Separating it from NVS means factory reset and app updates never
touch identity.

## Partition table
```
# Name,           Type, SubType,         Offset,  Size,   Flags
esp_secure_cert,  0x3F, ,                0xD000,  0x2000, encrypted
nvs,              data, nvs,             ,        0x6000,
```
Place it at the conventional offset 0xD000 (the configure tool's `--sec_cert_part_offset` defaults
to it). Mark `encrypted` when flash encryption is used.

## Provision
The tool is for development: its README warns it enables no protection for the data it writes,
and without `--configure_ds` the private key is stored as plaintext. For production, use flash
encryption or the DS peripheral.
```bash
pip install esp-secure-cert-tool
configure_esp_secure_cert.py -p PORT --target_chip esp32c3 \
    --ca-cert ca.pem --device-cert dev.pem --private-key dev.key \
    --priv_key_algo RSA 2048 --configure_ds        # omit --configure_ds to store a plain key
```
The tool writes the TLV-format partition by default (`--secure_cert_type cust_flash_tlv`; `cust_flash`
and `nvs` are legacy formats). Use `--skip_flash` to only generate the bin for a programming station.

## Read in firmware
```yaml
dependencies:
  espressif/esp_secure_cert_mgr: "^2.9.3"
```
```c
#include "esp_secure_cert_read.h"
char *cert; uint32_t len;
ESP_ERROR_CHECK(esp_secure_cert_get_device_cert(&cert, &len));
char *ca; uint32_t ca_len;
esp_secure_cert_get_ca_cert(&ca, &ca_len);
#ifdef CONFIG_ESP_SECURE_CERT_DS_PERIPHERAL
esp_ds_data_ctx_t *ds = esp_secure_cert_get_ds_ctx();
#else
char *key; uint32_t key_len; esp_secure_cert_get_priv_key(&key, &key_len);
#endif
```
Free each result with the matching `esp_secure_cert_free_*` call (for example `esp_secure_cert_free_device_cert`).

## Pre-provisioned modules
Espressif's pre-provisioned modules (e.g. for AWS IoT, Matter DAC) ship with this partition
filled at the factory. Do not overwrite it with a full-chip erase; `idf.py erase-flash` wipes it.
Use `idf.py flash` or exclude that region.

## Verify
- [ ] Device cert CN/serial matches the factory database.
- [ ] Partition survives OTA and factory reset.
- [ ] Private key not readable in a flash dump (DS or flash encryption in use).

## Checked

Checked against the esp_secure_cert_mgr repository (main, last commit 2026-08-21; idf_component.yml version 2.9.3) and ESP-IDF v6.1 docs.
Confirmed: the example partitions.csv line `esp_secure_cert, 0x3F, , 0xD000, 0x2000, encrypted` (0x3F is the type, not a subtype, now corrected); `esp_secure_cert_get_device_cert`, `esp_secure_cert_get_ca_cert`, `esp_secure_cert_get_priv_key`, `esp_secure_cert_get_ds_ctx` and the `esp_secure_cert_free_*` functions in esp_secure_cert_read.h; Kconfig symbol `ESP_SECURE_CERT_DS_PERIPHERAL`; configure_esp_secure_cert.py options `--target_chip`, `--ca-cert`, `--device-cert`, `--private-key`, `--priv_key_algo` (two values, e.g. RSA 2048), `--configure_ds`, `--skip_flash`, `--secure_cert_type` (default cust_flash_tlv) and `--sec_cert_part_offset` (default 0xD000); pip package name esp-secure-cert-tool; the tool README's development-only warning.

Method: documentation only; no commands were run.
