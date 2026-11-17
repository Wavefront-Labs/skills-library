---
id: computing-software.firmware-embedded-development.bootloader-development.validating-application-before-jump
name: validating-application-before-jump
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [app-validation, bootloader-architecture, image-integrity, stack-pointer-check, erased-flash-detection, firmware-embedded-development]
level: practitioner
status: draft
description: "Decide in the bootloader whether an application image is safe to start: erased-flash check, initial SP and reset vector sanity, header magic, length and CRC/signature."
sources:
  - https://docs.mcuboot.com/design.html
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.st.com/resource/en/application_note/an4657-stm32-inapplication-programming-iap-using-the-usart-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating the application before jumping

Jumping into a half-written or corrupt image produces a HardFault loop with no way back except a
debugger. The bootloader must refuse invalid images and stay in update mode instead.

## Check layers (cheapest first)
```c
#define APP_BASE   0x08008000u
#define RAM_START  0x20000000u
#define RAM_END    0x20020000u

static bool app_plausible(void) {
    const uint32_t *vt = (const uint32_t *)APP_BASE;
    uint32_t sp = vt[0], reset = vt[1];
    if (sp == 0xFFFFFFFFu && reset == 0xFFFFFFFFu) return false;         /* erased flash */
    if (sp < RAM_START || sp > RAM_END || (sp & 0x7u)) return false;      /* SP in RAM, 8-byte aligned */
    if ((reset & 1u) == 0) return false;                                  /* Thumb bit set */
    if (reset < APP_BASE || reset >= APP_BASE + APP_MAX_SIZE) return false;
    return true;
}
static bool app_valid(void) {
    const fw_header_t *h = (const fw_header_t *)(APP_BASE + HDR_OFFSET);
    if (!app_plausible() || h->magic != FW_MAGIC) return false;
    if (h->image_size == 0 || h->image_size > APP_MAX_SIZE) return false;
    return crc32_image(APP_BASE, h) == h->crc32;                          /* or verify a signature */
}
```
1. **Erased check** (all 0xFF): no app installed.
2. **Vector sanity**: initial MSP inside RAM (an RTOS app may point it at the top of RAM: allow
   `== RAM_END`), reset handler inside the app region with the Thumb bit.
3. **Header magic + length**: guards against a different product's image.
4. **Integrity**: CRC32 (accidental corruption) or ECDSA/Ed25519 signature (authenticity, see
   secure boot). Cover the whole image, not just the vector table.
5. **Update-complete marker**: write a "valid" flag or the header **last**, after all data is
   programmed and verified, so a power loss mid-update leaves an invalid image.

## Cost of a full CRC on every boot
CRC32 of 256 KB at 64 MHz in software is ~10-20 ms; with the hardware CRC unit ~1-2 ms. Usually
fine; for very fast boot requirements, verify fully after an update and on a periodic schedule,
and use a cheap check on normal boots.

## If invalid
Stay in the bootloader: start the update transport (UART, USB DFU, BLE), blink an error pattern,
and log the reason (no image, bad CRC, bad version) for diagnostics. Never loop resetting.

## Verify
- [ ] Erased app region: bootloader stays in update mode.
- [ ] Image with one flipped byte: rejected; correct image: boots.
- [ ] Power-cut during an update (test rig cutting power at random points): device always recovers to the bootloader or the old image.
