---
id: computing-software.firmware-embedded-development.bare-metal-programming.post-link-image-crc-patching
name: post-link-image-crc-patching
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [post-link-crc, srec-cat, image-checksum, firmware-integrity, build-pipeline, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Patch an image CRC and size into firmware after linking with a script and objcopy, then verify it at boot with the same CRC-32 parameters, including the 123456789 check value."
sources:
  - https://reveng.sourceforge.io/crc-catalogue/17plus.htm
  - https://sourceware.org/binutils/docs/binutils/objcopy.html
  - https://docs.python.org/3/library/zlib.html
  - https://srecord.sourceforge.net/man/man1/srec_input.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-link image CRC and metadata patching

**Goal:** the binary carries its own length and CRC, computed after linking, so a bootloader or
self-test can reject a corrupt or partially written image.

## Pipeline
1. Link to an ELF, then `arm-none-eabi-objcopy -O binary app.elf app.bin`.
2. Pad gaps with the value of erased flash: objcopy's `--gap-fill val` fills gaps between
   sections (by load address) with `val`, and `--pad-to address` pads the output up to a load
   address with the same value (zero by default). Erased flash usually reads 0xFF, so use
   `--gap-fill 0xFF` and compute the CRC over exactly the bytes you program.
3. A post-build script writes the image size and CRC into a header field at a known offset
   in the `.bin` (the offset comes from your linker script and header struct).
4. Flash the patched `.bin`, not the ELF: the ELF still holds the unpatched field. To fix the
   ELF too, `objcopy --update-section .fw_header=hdr.bin app.elf` replaces a section's contents
   with a file and adjusts the section size to the file size.

SRecord's `srec_cat` can post-process images through input filters (see the `srec_input`
manual for the filter list); check any filter name there before relying on it.

## Script pattern (Python)
```python
import struct, sys, zlib
bin_path, hdr_off = sys.argv[1], int(sys.argv[2], 0)
img = bytearray(open(bin_path, "rb").read())
struct.pack_into("<I", img, hdr_off + 8, len(img))   # image_size
struct.pack_into("<I", img, hdr_off + 12, 0)         # CRC field is zero while computing
struct.pack_into("<I", img, hdr_off + 12, zlib.crc32(img))
open(bin_path, "wb").write(img)
```
`zlib.crc32(data, value=0)` returns an unsigned 32-bit integer and `value` lets you continue a
running checksum. Run the script as a CMake `add_custom_command(TARGET ... POST_BUILD ...)` or
Makefile step.

## Match the algorithm on both sides
Write down polynomial, initial value, input and output reflection, final XOR, and which bytes
are covered, then give host and target the same ones. The common CRC-32 (named CRC-32/ISO-HDLC
in the RevEng catalogue) uses polynomial 0x04C11DB7, init 0xFFFFFFFF, reflected input and
output, final XOR 0xFFFFFFFF, and its check value for the ASCII string `123456789` is
0xCBF43926. Other catalogue entries share the polynomial but differ in the other parameters
(for example CRC-32/BZIP2 is unreflected, check 0xFC891918), so a polynomial match alone is not enough. A
hardware CRC peripheral has its own defaults; read its reference manual and set the
reflection and XOR options until it reproduces 0xCBF43926 for that string.

## Gotchas
- Compute the CRC with the CRC field treated as zero, or exclude the field, on both sides.
- A CRC only detects accidental corruption; use a signature for authenticity.

## Verify
- [ ] Host (`zlib.crc32(b"123456789")`) and target CRC routines both give 0xCBF43926.
- [ ] Recomputing over the flashed image with the CRC field zeroed matches the stored value.
- [ ] Flipping one byte in the image makes the boot check fail.

## Checked
Date: 2026-10-31.
Confirmed: CRC-32/ISO-HDLC and CRC-32/BZIP2 parameters and check values (RevEng 17-bit-plus
catalogue); objcopy `--gap-fill`, `--pad-to` default, `--update-section` behaviour (binutils
objcopy manual); `zlib.crc32(data, value=0)` signature and return type (Python zlib docs).
Removed as unconfirmed: the `srec_cat -crc32-l-e` command line and its equivalence to zlib,
pyelftools symbol lookup, STM32 hardware CRC defaults and HAL macro names, and the CMake variable name.
Method: documentation only; no commands were run.
