---
id: computing-software.firmware-embedded-development.bootloader-development.porting-mcuboot
name: porting-mcuboot
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcuboot-porting, mcuboot, bootutil, flash-map-backend, mcuboot-config-h, boot-go, image-trailer, crypto-backend, bare-metal-bootloader, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Port MCUboot to a new OS or bare-metal platform: mcuboot_config.h, the flash_area API backend, crypto and logging hooks, sector layout limits, calling boot_go and chain-loading."
sources:
  - https://docs.mcuboot.com/PORTING.html
  - https://docs.mcuboot.com/design.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/samples/mcuboot_config/mcuboot_config.template.h
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/bootutil/include/bootutil/bootutil.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Porting MCUboot to a new platform

**Goal:** use MCUboot's `bootutil` library (image validation, swap, rollback) on a platform
without an existing port (custom bare-metal, an RTOS other than the existing ports, a new SoC).

## What you provide
The porting guide's requirements: a configuration file, a flash API (minimum write size, and
read/write/erase of sectors), and a cryptographic library already available on the target (MCUboot
bundles none; supported are Mbed TLS, or tinycrypt together with Mbed TLS).
1. **`mcuboot_config/mcuboot_config.h`**. Start from
   `samples/mcuboot_config/mcuboot_config.template.h` (Zephyr and Mynewt have examples):
```c
#define MCUBOOT_SIGN_EC256              /* exactly one signature type: MCUBOOT_SIGN_RSA or MCUBOOT_SIGN_EC256 */
#define MCUBOOT_USE_MBED_TLS            /* or MCUBOOT_USE_TINYCRYPT */
#define MCUBOOT_VALIDATE_PRIMARY_SLOT   /* check the primary slot signature on every boot */
/* upgrade mode: default is swap with rollback; one of MCUBOOT_OVERWRITE_ONLY, MCUBOOT_DIRECT_XIP, MCUBOOT_RAM_LOAD */
#define MCUBOOT_IMAGE_NUMBER 1
#define MCUBOOT_MAX_IMG_SECTORS 128     /* template default: maximum sectors per image slot */
#define MCUBOOT_USE_FLASH_AREA_GET_SECTORS   /* if your flash map supports flash_area_get_sectors() */
#define MCUBOOT_WATCHDOG_FEED() do { /* feed the watchdog */ } while (0)
```
   The template also has `MCUBOOT_HW_KEY` / `MCUBOOT_BUILTIN_KEY`, `MCUBOOT_ENCRYPT_*` and
   `MCUBOOT_CPU_IDLE()`; the watchdog macro matters if a long swap would otherwise trip the watchdog.
2. **Logging**: if `MCUBOOT_HAVE_LOGGING` is on the platform defines `MCUBOOT_LOG_MODULE_REGISTER`,
   `MCUBOOT_LOG_MODULE_DECLARE` and `MCUBOOT_LOG_ERR/WRN/INF/DBG`.
3. **Flash map**: each flash region has a unique `uint8_t` ID (examples: bootloader 0, primary
   1, secondary 2, scratch 3; second image 5 and 6; numbers depend on your system). You supply
   the `flash_area` getters (`flash_area_get_id`, `_get_device_id`, `_get_off`, `_get_size`) and
   the API `flash_area_open/close/read/write/erase`, `flash_area_align`,
   `flash_area_erased_val`, `flash_area_get_sectors`, `flash_area_get_sector`,
   `flash_area_id_from_image_slot`, `flash_area_id_from_multi_image_slot`,
   `flash_area_id_to_multi_image_slot` and `flash_device_base`.
   `flash_area_get_sector()` offsets are relative to the start of the flash area, not the device.
   MCUboot may open the same flash area several times (nested `flash_area_open`), so
   `flash_area_close` should only fully deinitialise at an open count of 0.
4. **Crypto**: Mbed TLS uses `calloc`/`free`, so the RTOS must provide them; hook them with
   `mbedtls_platform_set_calloc_free()`. Public keys come from `imgtool getpub -k <key.pem>`.

## Main
`boot_go(struct boot_rsp *rsp)` (in `boot/bootutil/loader.c`) runs the bootloader's management
functions and returns an initialised `boot_rsp` locating the image to run. In current source
the struct has `br_hdr` (pointer to the image header), `br_flash_dev_id` and `br_image_off`
(the PORTING page still shows `br_flash_id` and `br_image_addr`; follow the header you build).
```c
struct boot_rsp rsp;
if (boot_go(&rsp) != 0) { /* recovery or halt */ }
/* locate the image from rsp, de-initialise peripherals and interrupts, then branch to it */
```
See `jump-from-bootloader-to-application` for clean handoff.

## Layout constraints
- Slot sizes: the maximum image size is `image-slot-size - image-trailer-size` for overwrite;
  for swap-using-move the design doc gives `(N-1) * slot-sector-size - image-trailer-sectors-size`.
  See the design doc for the trailer layout and formulas.
- Swap-using-scratch is required when slots have different or non-uniform sector sizes
  (Zephyr readme); the Zephyr swap-using-offset mode needs all sectors in both slots to be the
  same size (Kconfig).
- Report the real minimum write size through `flash_area_align` and the erased value through
  `flash_area_erased_val`; wrong values corrupt trailers.

## Verify
- [ ] An image signed with `imgtool sign` boots; an unsigned or tampered image is refused.
- [ ] Upgrade with the test flag, reset without confirming: the revert happens.
- [ ] Reset at random points during a swap (power-fail test) and confirm the device recovers.

## Checked
2026-10-31. Confirmed against the MCUboot porting page (requirements, `boot_go`, flash map IDs and API list, nested
open note, Mbed TLS calloc/free), the `mcuboot_config.template.h` (macro names, defaults), `bootutil.h` (`boot_rsp`
fields), the MCUboot design doc (maximum image size formulas) and the Zephyr readme/Kconfig (scratch and offset
sector rules). Removed: `MCUBOOT_SIGN_ED25519` (not in the template), the `wdt_feed` call, STM32L4 alignment
examples, `bootutil_keys[]`, the `sim/` cargo tests mention, the "malloc-free" claim and the Cortex-M register
details.
Method: documentation only; no commands were run.
