---
id: computing-software.firmware-embedded-development.bare-metal-programming.fixed-address-custom-sections
name: fixed-address-custom-sections
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fixed-address-section, linker-script, section-attribute, image-header, keep, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Place a firmware header, config block, shared struct or calibration table at a fixed flash/RAM address with section attributes and ld script rules that GC cannot drop."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html
  - https://sourceware.org/binutils/docs/ld/Input-Section-Keep.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-Address.html
  - https://sourceware.org/binutils/docs/ld/MEMORY.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-Type.html
  - https://sourceware.org/binutils/docs/ld/File-Commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Placing objects at fixed addresses with custom sections

**Use cases:** an image header right after the vector table that a bootloader reads, a
calibration block written at the factory, a mailbox struct shared between bootloader and app or
between two cores, a version string at a known offset for production tools.

## Pattern
```c
typedef struct {
    uint32_t magic;          /* 0x46574844 'FWHD' */
    uint32_t version;
    uint32_t image_size;     /* patched post-link */
    uint32_t crc32;          /* patched post-link */
} fw_header_t;

__attribute__((section(".fw_header"), used))
const fw_header_t g_fw_header = { 0x46574844u, FW_VERSION, 0, 0 };
```
```ld
MEMORY {
  FLASH (rx) : ORIGIN = 0x08008000, LENGTH = 478K
  CALIB (r)  : ORIGIN = 0x0807F800, LENGTH = 2K
}
SECTIONS {
  .isr_vector : { KEEP(*(.isr_vector)) } > FLASH
  .fw_header 0x08008200 : { KEEP(*(.fw_header)) } > FLASH   /* fixed VMA */
  .text : { *(.text*) } > FLASH
  .calib (NOLOAD) : { KEEP(*(.calib)) } > CALIB              /* reserved, not in the image */
}
```
- `used` makes the compiler emit an unreferenced variable; `KEEP()` stops `--gc-sections`
  discarding the section. You need both (GCC's `retain` attribute also protects against linker
  garbage collection, with Binutils 2.36 or later).
- An address written after the output section name (`.fw_header 0x08008200`) sets its VMA exactly.
- `NOLOAD` marks a section not loadable, so it is not loaded into memory when the program runs.
  Use it for regions whose content is written elsewhere (factory calibration, shared RAM), and
  check with `objdump -h` that the section lacks the LOAD flag before relying on a programmer to
  leave the calibration page alone.
- Give fixed blocks their own MEMORY region and size the code region so it ends before them: ld
  errors when the sections directed to a region do not fit, but it does not check that two MEMORY
  regions you defined overlap each other.

## Shared RAM between bootloader and application
Both link scripts must agree on the address. Put the region in a shared include:
```ld
INCLUDE shared_memory.ld        /* your file: defines SHARED (rw) : ORIGIN = 0x2001FF00, LENGTH = 256 */
.shared (NOLOAD) : { KEEP(*(.shared)) } > SHARED
```
and remove that range from each image's RAM region so neither zeroes it in `.bss` init.

## Alternatives and why not
- `*(volatile fw_header_t *)0x08008200` pointer casts: fine for reading, but nothing reserves
  the space and the linker may place code there.
- The GCC `section` attribute only names a section; the address comes from the linker script.

## Verify
- [ ] `arm-none-eabi-objdump -h app.elf` shows `.fw_header` at the exact VMA.
- [ ] `arm-none-eabi-objdump -s -j .fw_header app.elf` shows the magic bytes.
- [ ] Building with `-Wl,--gc-sections -flto` still keeps the section.
- [ ] Flashing the app leaves the calibration page unchanged (read it back with the programmer).

## Checked
2026-11-08. Confirmed in the GCC manual (`section`, `used` and `retain` attributes) and the GNU ld manual
(Output Section Address, MEMORY Command, Output Section Type NOLOAD, Input Section and Garbage Collection,
INCLUDE). Fixed: the example FLASH region of 480K ran into the CALIB region at 0x0807F800, now 478K. Removed: the
quoted ld error text, the claim that the ELF contains no bytes for NOLOAD, and the Arm Compiler `at`/armclang
remark (not in the cited pages). The objdump commands in the checklist were not checked against a manual.
Method: documentation only; no commands were run.
