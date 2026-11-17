---
id: computing-software.firmware-embedded-development.stm32.hardware-crypto-and-rng
name: hardware-crypto-and-rng
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, stm32-hw-crypto, stm32-rng, aes-gcm, hash-peripheral, pka, mbedtls-alt, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use STM32 hardware RNG, AES/CRYP, HASH and PKA peripherals through HAL or as mbedTLS/CMOX accelerators: clocking, error handling, data formats and what they don't protect."
sources:
  - https://www.st.com/resource/en/application_note/an4230-stm32-microcontrollers-random-number-generation-validation-using-the-nist-statistical-test-suite-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an5156-introduction-to-stm32-microcontrollers-security-stmicroelectronics.pdf
  - https://www.st.com/en/embedded-software/x-cube-cryptolib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware crypto and RNG

Availability varies by part number: e.g. on F4 only F415/417/437/439 have CRYP and HASH; L4
"x6" variants (L486, L4A6) have AES; L5/U5/H5 add PKA (SAES on U5/H5). Check the datasheet
before designing around a peripheral.

## True RNG
```c
RNG_HandleTypeDef hrng = { .Instance = RNG };
HAL_RNG_Init(&hrng);
uint32_t r;
if (HAL_RNG_GenerateRandomNumber(&hrng, &r) != HAL_OK) {
    /* HAL_RNG_ERROR_SEED / CLOCK: health failure -> re-init RNG, retry, then fail closed */
}
```
- Needs a 48 MHz-class clock (HSI48, PLL Q or MSI with LSE PLL-mode). A clock error (CECS) or
  seed error (SECS) means output must not be used; the HAL reports it and you must reinitialise.
- Treat it as an **entropy source**: seed a DRBG (mbedTLS `mbedtls_ctr_drbg` with
  `mbedtls_hardware_poll` returning RNG words) rather than using raw words directly for keys.
  Newer series (U5, H5) have NIST SP 800-90B configuration values in the RM; use them.

## AES (CRYP/AES peripheral)
```c
CRYP_HandleTypeDef hcryp = { .Instance = AES };
hcryp.Init.DataType   = CRYP_DATATYPE_8B;        /* byte swapping for byte arrays */
hcryp.Init.KeySize    = CRYP_KEYSIZE_256B;
hcryp.Init.pKey       = (uint32_t *)key_words;   /* key as 32-bit words, big-endian order */
hcryp.Init.Algorithm  = CRYP_AES_GCM_GMAC;
hcryp.Init.pInitVect  = (uint32_t *)iv_words;    /* GCM: 96-bit IV + counter */
hcryp.Init.Header     = (uint32_t *)aad; hcryp.Init.HeaderSize = aad_words;
HAL_CRYP_Init(&hcryp);
HAL_CRYP_Encrypt(&hcryp, (uint32_t *)pt, len_words, (uint32_t *)ct, 100);
HAL_CRYPEx_AESGCM_GenerateAuthTAG(&hcryp, (uint32_t *)tag, 100);
```
Byte order and word-size units (`Size` in words vs bytes, depending on HAL version and
`DataWidthUnit`) are the classic bugs. Always test against published vectors (NIST CAVP) first.
Use DMA (`HAL_CRYP_Encrypt_DMA`) for large buffers.

## HASH and PKA
- HASH: `HAL_HASHEx_SHA256_Start(&hhash, in, len, digest, timeout)`; HMAC variants exist.
- PKA (L5/U5/H5/WB): ECDSA verify/sign, RSA modular exponentiation:
  `HAL_PKA_ECDSAVerif(&hpka, &in, timeout)` then `HAL_PKA_ECDSAVerif_IsValidSignature`.
  Speeds up secure-boot signature checks a lot.

## Using them from libraries
- mbedTLS: enable `MBEDTLS_AES_ALT`, `MBEDTLS_SHA256_ALT`, `MBEDTLS_ECDSA_VERIFY_ALT` with
  ST's alt implementations (shipped in STM32Cube MCU packages' mbedTLS middleware).
- X-CUBE-CRYPTOLIB (CMOX): ST's library with hardware acceleration where available.
- PSA Crypto / TF-M on TrustZone parts drives these peripherals from the secure world.

## Limits
Hardware AES makes crypto fast; it doesn't protect keys loaded from flash in plaintext. Use
SAES with hardware-unique keys (U5/H5), secure storage in the TrustZone world, or wrapped keys.
Side-channel resistance differs between AES and SAES; check the RM for your threat model.

## Verify
- [ ] Known-answer tests (NIST vectors) pass for each mode used, in CI on target.
- [ ] RNG error injection (stop its clock) is detected and handled, not silently ignored.
- [ ] Peripheral availability confirmed for the exact part number on the BOM.

## Checked

2026-10-31: Confirmed `HAL_RNG_Init`/`HAL_RNG_GenerateRandomNumber` and the RNG seed/clock error flags (stm32l4xx_hal_rng.h); the CRYP API `CRYP_DATATYPE_8B`, `CRYP_KEYSIZE_256B`, `CRYP_AES_GCM_GMAC`, `HAL_CRYP_Init`, `HAL_CRYP_Encrypt`, `HAL_CRYP_Encrypt_DMA` and `HAL_CRYPEx_AESGCM_GenerateAuthTAG` (stm32g4xx_hal_cryp.h/_ex.h); `HAL_HASHEx_SHA256_Start` and the HMAC variants (stm32f4xx_hal_hash_ex.h); the PKA API `HAL_PKA_ECDSAVerif` and `HAL_PKA_ECDSAVerif_IsValidSignature` (stm32u5xx_hal_pka.h); and the mbedTLS integration points `MBEDTLS_AES_ALT`, `MBEDTLS_SHA256_ALT`, `MBEDTLS_ECDSA_VERIFY_ALT`, `mbedtls_hardware_poll` and `mbedtls_ctr_drbg_*` from Mbed-TLS v2.28.9. Fixed the series scoping (PKA on L5/U5/H5; SAES on U5/H5).

Method: documentation only; no commands were run.
