---
id: computing-software.firmware-embedded-development.esp-idf.digital-signature-and-hmac-peripherals
name: digital-signature-and-hmac-peripherals
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, esp-ds-peripheral, esp-hmac, hardware-key-protection, mtls-device-key, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Protect device private keys on supported ESP32 chips with the RSA Digital Signature (DS) and HMAC peripherals: eFuse key burning, encrypted key blobs and TLS use."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/ds.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/hmac.rst
  - https://github.com/espressif/esp_secure_cert_mgr/blob/main/README.md
  - https://github.com/espressif/esp_secure_cert_mgr/blob/main/tools/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Digital signature and HMAC peripherals

The DS peripheral performs RSA private-key operations with a key that the CPU never sees in
plaintext. An HMAC key in eFuse (read-protected) derives the AES key that decrypts the RSA key
blob inside the hardware. Availability depends on the chip (the DS and HMAC pages gate it by target); the original ESP32 has neither.

## Provisioning flow
1. Generate per-device RSA key (on host or device) and certificate.
2. Generate a random 256-bit HMAC key; burn it to a free eFuse key block with purpose
   `HMAC_DOWN_DIGITAL_SIGNATURE` (key purpose value 7), configured so software cannot read it back.
3. Encrypt the RSA key parameters with the HMAC-derived key into a DS ciphertext blob
   (the `esp_secure_cert_mgr` tool `configure_esp_secure_cert.py` does this with `--configure_ds`).
4. Store the blob plus certificate in the `esp_secure_cert` partition.
```bash
configure_esp_secure_cert.py -p PORT --keep_ds_data_on_host --efuse_key_id 1 --ca-cert ca.pem \
    --device-cert dev.pem --private-key dev.key --target_chip esp32s3 --configure_ds
```
eFuse burning is irreversible; dry-run on a dev board and record which key block you use.

## TLS with DS
```c
#include "esp_secure_cert_read.h"
esp_ds_data_ctx_t *ds = esp_secure_cert_get_ds_ctx();
esp_tls_cfg_t cfg = { .clientcert_buf = cert, .clientcert_bytes = cert_len, .ds_data = ds };
/* or esp_mqtt_client_config_t.credentials.authentication.ds_data = ds */
```
With `CONFIG_ESP_TLS_USE_DS_PERIPHERAL=y`, signing during the TLS handshake goes through the peripheral. Outside ESP-TLS, `CONFIG_MBEDTLS_HARDWARE_RSA_DS_PERIPHERAL` and the PSA Crypto RSA_DS driver expose it for signing and decryption.

## HMAC peripheral alone
`esp_hmac_calculate(HMAC_KEY0, msg, len, out)` computes HMAC-SHA256 with an eFuse key whose purpose is `HMAC_UP` (value 8, HMAC generated for software use); the PSA `psa_mac_compute` path is documented for the same mode. Use it for device authentication challenges or to protect the NVS encryption key (`CONFIG_NVS_SEC_KEY_PROTECT_USING_HMAC`) without an nvs_keys partition. A key with purpose `HMAC_DOWN_JTAG` (6) or `HMAC_DOWN_ALL` (5) is used with `esp_hmac_jtag_enable` to re-enable soft-disabled JTAG.

## Limits
- DS performs plain RSA signing with a fixed message length: the input is normally a hash of the real message padded to the required length (see the DS page; the maximum RSA size is chip-specific). ECDSA keys use the separate ECDSA peripheral on chips that have one.
- The HMAC key block must be read-protected so software cannot read the key back; verify with `espefuse summary`.

## Verify
- [ ] `espefuse summary` shows the key block purpose and read protection.
- [ ] mTLS connection succeeds; flash dump contains no plaintext private key.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the DS and HMAC pages, esp_hmac.h and the esp_secure_cert_mgr READMEs: DS uses an HMAC-derived key to decrypt stored RSA parameters, 256-bit HMAC key in an eFuse block, key purpose values (HMAC_UP 8, HMAC_DOWN_DIGITAL_SIGNATURE 7, HMAC_DOWN_JTAG 6, HMAC_DOWN_ALL 5), esp_hmac_calculate and esp_hmac_jtag_enable, configure_esp_secure_cert.py flags, esp_secure_cert partition, CONFIG_ESP_TLS_USE_DS_PERIPHERAL and CONFIG_NVS_SEC_KEY_PROTECT_USING_HMAC. Removed unconfirmed chip list, RSA size limits and DS timing; added the PSA paths.
Method: documentation only; no commands were run.
