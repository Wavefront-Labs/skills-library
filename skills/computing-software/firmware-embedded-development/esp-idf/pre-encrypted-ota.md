---
id: computing-software.firmware-embedded-development.esp-idf.pre-encrypted-ota
name: pre-encrypted-ota
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, pre-encrypted-ota, esp-encrypted-img, rsa-ota-encryption, firmware-confidentiality, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Ship firmware encrypted end to end with ESP-IDF pre-encrypted OTA (esp_encrypted_img): key generation, image encryption, decrypt callbacks and key protection."
sources:
  - https://github.com/espressif/idf-extra-components/blob/master/esp_encrypted_img/README.md
  - https://github.com/espressif/idf-extra-components/blob/master/esp_encrypted_img/include/esp_encrypted_img.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_https_ota/include/esp_https_ota.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-encrypted OTA

TLS protects the image in transit; pre-encrypted OTA keeps it encrypted on the server and CDN
too, so a leaked bucket doesn't leak firmware.

## Scheme
The image is encrypted with a random AES-GCM key, which is wrapped with an RSA-3072 public key.
The device holds the RSA private key and unwraps it during download. The component also supports
ECIES-P256, where the device key is derived from an HMAC key in eFuse; the header is 512 bytes in
both schemes.

## Keys and image
```bash
python esp_enc_img_gen.py --generate_rsa_key     # or: openssl genrsa -out rsa_key/private.pem 3072
# encrypt the built app with the PUBLIC key
python esp_enc_img_gen.py encrypt build/app.bin rsa_pub_key.pem app_encrypted.bin
```
`esp_enc_img_gen.py` ships with the `esp_encrypted_img` component. `--generate_rsa_key` writes
`rsa_pub_key.pem` and `rsa_priv_key.pem`; encryption takes the public key, the device needs the
private key. Keep the private key out of the repository; CI needs only the public key.

## Device side
Enable `CONFIG_ESP_HTTPS_OTA_DECRYPT_CB=y` so `esp_https_ota` calls the decrypt callback.
```yaml
# main/idf_component.yml
dependencies:
  espressif/esp_encrypted_img: "*"
```
```c
#include "esp_encrypted_img.h"
static esp_decrypt_handle_t dec;
static esp_err_t decrypt_cb(decrypt_cb_arg_t *args, void *ud) {
    pre_enc_decrypt_arg_t in = { .data_in = args->data_in, .data_in_len = args->data_in_len };
    esp_err_t e = esp_encrypted_img_decrypt_data(dec, &in);
    if (e != ESP_OK && e != ESP_ERR_NOT_FINISHED) return e;
    args->data_out = in.data_out; args->data_out_len = in.data_out_len;
    return ESP_OK;
}
esp_decrypt_cfg_t cfg = { .rsa_priv_key = (char *)rsa_start, .rsa_priv_key_len = rsa_end - rsa_start };
dec = esp_encrypted_img_decrypt_start(&cfg);
esp_https_ota_config_t ota = { .http_config = &http, .decrypt_cb = decrypt_cb };
/* after esp_https_ota_perform loop */
ESP_ERROR_CHECK(esp_encrypted_img_decrypt_end(dec));    /* verifies the GCM tag */
```

## Protecting the private key
An embedded key in a plaintext app can be dumped from flash. Combine with flash encryption,
or store the key in an encrypted NVS / esp_secure_cert partition, or use the Digital Signature (DS) peripheral where supported (the component has an RSA-with-DS
option, which needs the key provisioned through esp_secure_cert), or use the ECIES scheme with an
HMAC-derived device key. Pre-encrypted OTA is confidentiality only; authenticity still comes from Secure Boot
signatures.

## Verify
- [ ] A tampered byte in the encrypted file makes `decrypt_end` fail and OTA abort.
- [ ] Plain (unencrypted) image is rejected.
- [ ] Private key absent from the git history and CI logs.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in the esp_encrypted_img README and esp_encrypted_img.h (idf-extra-components, component version 2.7.1) and esp_https_ota.h: RSA-3072 and ECIES-P256 schemes, 512-byte header, esp_enc_img_gen.py commands (encrypt takes the public key; --generate_rsa_key), esp_decrypt_cfg_t.rsa_priv_key and rsa_priv_key_len, pre_enc_decrypt_arg_t fields, decrypt_start / decrypt_data / decrypt_end, ESP_ERR_NOT_FINISHED, DS option, decrypt_cb under CONFIG_ESP_HTTPS_OTA_DECRYPT_CB. Fixed: encryption uses the public key, not the private key; the script path under managed_components was unconfirmed. Removed the pinned component version.

Method: documentation only; no commands were run.
