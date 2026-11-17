---
id: computing-software.firmware-embedded-development.bootloader-development.bootloader-application-handoff-data
name: bootloader-application-handoff-data
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader-architecture, bootloader-app-handoff, noinit-ram, magic-word, shared-ram, boot-flags, enter-bootloader-request, boot-info, firmware-embedded-development]
level: advanced
status: draft
description: "Pass data between bootloader and application across resets: no-init RAM blocks with magic and CRC, backup registers, and versioned boot-info structs."
sources:
  - https://docs.mcuboot.com/design.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-Type.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bootloader-to-application handoff data

**Goal:** a reliable channel for "app requests firmware update mode", "bootloader tells app
which slot/version booted and why", and reset-reason history.

## Channels
| Channel | Survives | Use |
|---|---|---|
| No-init SRAM section | software/watchdog reset, not power loss | request flags, boot info, crash logs |
| RTC backup registers (STM32 `RTC->BKPxR`) | resets and VBAT-backed power loss | small flags; needs backup domain write access |
| Flash/NVS record | everything | rare persistent settings (wears flash) |
| Image trailer (MCUboot) | everything | update state, confirmation flag |

## No-init RAM block
Reserve the same address in **both** linker scripts, outside `.data`/`.bss` so neither
startup code zeroes it:
```ld
/* both bootloader and app */
MEMORY { RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 128K - 256
         SHARED (rw) : ORIGIN = 0x2001FF00, LENGTH = 256 }
SECTIONS { .shared (NOLOAD) : { KEEP(*(.shared)) } > SHARED }
```
```c
typedef struct {
    uint32_t magic;        /* 0xB007DA7A */
    uint16_t version;      /* struct layout version */
    uint16_t len;
    uint32_t request;      /* e.g. ENTER_DFU */
    uint32_t boot_count;
    uint32_t crc;          /* over all fields above */
} handoff_t;
__attribute__((section(".shared"))) volatile handoff_t g_handoff;
```

## Rules
- **Magic + CRC + version** on every read. At power-on the RAM holds random data; one magic
  word alone matches by chance and also survives a half-written update.
- **Consume and clear**: the reader clears the request after acting on it, otherwise a
  watchdog reset during DFU loops back into DFU forever.
- **Version the struct** and only append fields; bootloaders outlive many app versions.
- Reserve the block at the **top or bottom of RAM away from the stack**; the app's stack
  growing into it corrupts the handoff silently. Shrink the app's RAM region accordingly.
- With ECC RAM (STM32H7/G4 SRAM with parity, some L-series), reading uninitialised RAM after
  power-on can raise an ECC/parity fault: the bootloader must initialise the block on a
  power-on reset (check RCC reset flags) before anything reads it.
- Zephyr/MCUboot provide a standard "shared data" TLV area (`MCUBOOT_DATA_SHARING`) and
  `boot_request_upgrade()`/image trailer flags; prefer those when using MCUboot.

## Verify
- [ ] App sets ENTER_DFU and resets: bootloader enters DFU once; next reset boots the app.
- [ ] Cold power-on with random RAM never triggers a request (fuzz with a pattern fill).
- [ ] Map files of both images show the shared block at the same address and size.
