---
id: computing-software.firmware-embedded-development.zephyr.build-output-artefacts
name: build-output-artefacts
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-build-output, zephyr-elf, zephyr-hex, zephyr-dts-final, build-directory-layout, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find and use what a Zephyr build produces: zephyr.elf/hex/bin/signed images, the merged .config, zephyr.dts, generated headers, map files, and the sysbuild layout."
sources:
  - https://docs.zephyrproject.org/latest/build/cmake/index.html
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/Kconfig.zephyr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build output artefacts

## Single-image build (`build/`)
| Path | What |
|---|---|
| `build/zephyr/zephyr.elf` | final image with symbols; use for debugging, `addr2line`, size tools |
| `build/zephyr/zephyr.hex` / `.bin` | flashable images (`CONFIG_BUILD_OUTPUT_HEX` is off by default, `CONFIG_BUILD_OUTPUT_BIN` defaults to y; the base name follows `CONFIG_KERNEL_BIN_NAME`) |
| `build/zephyr/zephyr.signed.bin/.hex` | MCUboot-signed image when `CONFIG_BOOTLOADER_MCUBOOT=y` |
| `build/zephyr/zephyr.uf2` | with `CONFIG_BUILD_OUTPUT_UF2=y` |
| `build/zephyr/zephyr.map` | linker map: symbol addresses and section sizes |
| `build/zephyr/zephyr.stat` | `readelf -e` output of the ELF (`CONFIG_OUTPUT_STAT`, default y) |
| `build/zephyr/zephyr.lst` | disassembly (`CONFIG_OUTPUT_DISASSEMBLY=y`) |
| `build/zephyr/.config` | final merged Kconfig |
| `build/zephyr/zephyr.dts` | final merged devicetree (after overlays) |
| `build/zephyr/include/generated/zephyr/devicetree_generated.h` | DT macros the code sees |
| `build/zephyr/include/generated/zephyr/autoconf.h` | `CONFIG_*` macros |
| `build/zephyr/runners.yaml` | runner configuration for `west flash/debug` |
| `build/compile_commands.json` | for clangd / IDE indexing |
| `build/zephyr/linker.cmd` | generated linker script |

`devicetree_generated.h` lives under `include/generated/zephyr/`; check your build tree for the
exact location of the other generated headers in your release.

## Sysbuild (`west build --sysbuild`)
Each image gets its own subdirectory:
```
build/
  mcuboot/zephyr/zephyr.hex
  <app-name>/zephyr/zephyr.signed.hex
  merged_<NORMALIZED_BOARD_TARGET>.hex   # with SB_CONFIG_MERGED_HEX_FILES; one per board target
  domains.yaml         # which images exist; west flash/debug use it (with runners.yaml)
```

## Typical uses
- Debug a missing node: grep `zephyr.dts`, not your overlay.
- Confirm an option is really on: grep `build/zephyr/.config`, not `prj.conf`.
- CI artefacts to keep: `zephyr.elf` (for crash decoding), the flashable images, `.config`,
  `zephyr.dts`, and the map file.
- Footprint: `west build -t rom_report` / `ram_report` (with sysbuild, `-d build/<image>`).

## Gotchas
- `zephyr.bin` has gaps filled when sections are far apart (e.g. external flash), producing huge
  files; use hex for those layouts.
- Re-using a build directory for a different board needs `-p` (`--pristine=auto` detects some cases; `west config build.pristine auto|always|never`).
- Generated files are regenerated each build; never edit them.

## Verify
- [ ] CI uploads elf + image + `.config` + `zephyr.dts` per build.
- [ ] Release images can be traced to the exact `.elf` used for crash decoding.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/build/cmake/index.rst, doc/build/sysbuild/index.rst, doc/develop/west/build-flash-debug.rst, Kconfig.zephyr and CMakeLists.txt.
Confirmed: `zephyr.dts`, `zephyr.dts.pre`, `devicetree_generated.h` path, `autoconf.h`, `.config`, `linker.cmd`, `compile_commands.json`; `CONFIG_BUILD_OUTPUT_HEX` (default off), `CONFIG_BUILD_OUTPUT_BIN` (default y), `CONFIG_KERNEL_BIN_NAME`, `CONFIG_OUTPUT_STAT`, `CONFIG_OUTPUT_DISASSEMBLY`, `CONFIG_BUILD_OUTPUT_UF2` exists, binary files always gap-filled; `.map` generation; signed images when MCUboot signing applies; sysbuild per-image directories (`build/mcuboot`), `domains.yaml`/`runners.yaml`, `SB_CONFIG_MERGED_HEX_FILES` with `merged_<NORMALIZED_BOARD_TARGET>.hex`; `rom_report`; `--pristine` and `build.pristine`.

Method: documentation only; no commands were run.
