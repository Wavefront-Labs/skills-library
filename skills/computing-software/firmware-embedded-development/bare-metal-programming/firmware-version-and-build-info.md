---
id: computing-software.firmware-embedded-development.bare-metal-programming.firmware-version-and-build-info
name: firmware-version-and-build-info
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [firmware-version-info, superloop, git-describe, build-id, semantic-version, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Embed a version, git describe string and GNU build-id in firmware so every binary and crash report maps to exact source."
sources:
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://git-scm.com/docs/git-describe
  - https://interrupt.memfault.com/blog/gnu-build-id-for-firmware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding firmware version and build info

Every field report, crash dump and OTA decision needs "which exact build is this?". Answer it
with three items: a version number for humans and update logic, a git description, and the
GNU build-id that identifies the linked ELF.

## Git description
```sh
git describe --tags --dirty --always --abbrev=12
```
- `--tags` uses lightweight tags too, `--always` falls back to the abbreviated commit name when
  no tag is reachable, `--abbrev=<n>` sets the hash length (the default varies with repository
  size), and `--dirty` appends `-dirty` when the working tree has local modifications.
- Generate a header from this output at build time (CMake `execute_process` plus
  `configure_file`, a Makefile rule, or a script) and refresh it every build, not only at
  configure time. Fail CI if a release artefact contains `-dirty`.

## GNU build-id
```sh
-Wl,--build-id=sha1
```
- GNU ld's `--build-id[=style]` creates a `.note.gnu.build-id` note. Styles are `uuid` (128
  random bits), `sha1` (160-bit), `md5` and `xx` (128-bit). The `sha1`, `md5` and `xx` styles give
  the same id for an identical output file. It is an identifier, not a checksum of the contents.
- Plain `-Wl,--build-id` also works. Dump it with `readelf -n app.elf`.
- Bare-metal images discard the note unless the linker script keeps it. The Memfault article
  shows this pattern, which places the note in the ROM region and exports a symbol:
```ld
.note.gnu.build-id : { PROVIDE(g_note_build_id = .); KEEP(*(.note.gnu.build-id)) } > FLASH
```
- The note layout is `namesz` (4), `descsz` (20 for sha1), `type` (3), then the name `GNU\0`, then
  the id bytes, so skip 16 bytes of header to reach the id. Print it at boot and in crash
  reports and compare with `readelf -n`.

## Version in a fixed header
Put the numeric version in an image header the bootloader reads so update logic can compare
versions without parsing strings. Pick one fixed encoding, such as one byte each for major,
minor and patch, and document it next to the header struct.

## Verify
- [ ] The git description string appears in the binary and in the boot log.
- [ ] The boot-log build-id equals the `readelf -n` output for the same ELF.
- [ ] A release build is not `-dirty`.

## Checked
Date: 2026-10-31.
Confirmed in the git-describe manual: `--tags`, `--always`, `--abbrev=<n>`, `--dirty` behaviour.
Confirmed in the GNU ld options page: `--build-id[=style]`, the style list and bit sizes, the
identical-output property, and that it is not a checksum. Confirmed in the Memfault article:
the `readelf -n` workflow, the linker-script `KEEP`/`PROVIDE` pattern, note field sizes
(namesz 4, descsz 20, type 3).
Removed as unconfirmed: the CMake snippet, the claim about `__DATE__`/`__TIME__`, MCUboot, BLE,
USB and telemetry exposure lists, and the symbol-server statement.
Method: documentation only; no commands were run.
