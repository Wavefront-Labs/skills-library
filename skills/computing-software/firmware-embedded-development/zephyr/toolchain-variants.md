---
id: computing-software.firmware-embedded-development.zephyr.toolchain-variants
name: toolchain-variants
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [toolchain-variant, zephyr-toolchain-variant, gnuarmemb, llvm-toolchain, cross-compile, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build Zephyr with a non-default toolchain via ZEPHYR_TOOLCHAIN_VARIANT (zephyr, gnuarmemb, cross-compile, iar, host/gnu, host/llvm, xcc) and handle the differences."
sources:
  - https://docs.zephyrproject.org/latest/develop/toolchains/index.html
  - https://docs.zephyrproject.org/latest/develop/toolchains/gnu_arm_embedded.html
  - https://docs.zephyrproject.org/latest/develop/toolchains/other_x_compilers.html
  - https://docs.zephyrproject.org/latest/develop/toolchains/iar_arm_toolchain.html
  - https://docs.zephyrproject.org/latest/develop/toolchains/host.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/lib/libc/picolibc/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toolchain variants

Selected with the `ZEPHYR_TOOLCHAIN_VARIANT` environment variable or CMake variable. CMake
caches settings in an existing build directory, so use a pristine build (`west build -p always`)
or a fresh build directory when switching.

| Variant | Extra variable | Use |
|---|---|---|
| `zephyr` (default) | `ZEPHYR_SDK_INSTALL_DIR` (optional) | Zephyr SDK; best tested |
| `gnuarmemb` | `GNUARMEMB_TOOLCHAIN_PATH` | GNU Arm Embedded toolchain (`arm-none-eabi`), Arm targets only |
| `cross-compile` | `CROSS_COMPILE=/path/prefix-` | any GNU-based cross toolchain whose binaries share one directory and prefix (not officially supported) |
| `iar` | `IAR_TOOLCHAIN_PATH` (and `IAR_LMS_BEARER_TOKEN` for cloud licences) | IAR Arm Toolchain v9.70 or newer; the Zephyr SDK must also be installed; limited feature set (minimal libc only, no C++, no TrustedFirmware) |
| `host/gnu`, `host/llvm` | none | reuse the host gcc or clang (for example non-MCU x86 builds on Linux) |
| `xcc`, `xt-clang` | `XTENSA_TOOLCHAIN_PATH`, `XTENSA_CORE`, `TOOLCHAIN_VER` | Cadence Tensilica Xtensa compilers |
| `oneApi` | `ONEAPI_TOOLCHAIN_PATH` | Intel oneAPI |
| `armclang` | `ARMCLANG_TOOLCHAIN_PATH`, `ARMLMD_LICENSE_FILE` | Arm Compiler 6 |

Other variants in `cmake/toolchain/` include `arcmwdt`, `hexagon`, `tricore` and `xc32`. The Zephyr
SDK also ships an `llvm` bundle variant (LLVM/Clang plus host tools); see the SDK page for how
it is selected.

```bash
export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
export GNUARMEMB_TOOLCHAIN_PATH=<path-to>/gnu_arm_embedded
west build -p always -b nucleo_f429zi samples/hello_world
```
Or per-build: `west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=host/llvm`.

## Differences that bite
- **C library:** the default is picolibc (`CONFIG_PICOLIBC`). Its source is the module
  (`CONFIG_PICOLIBC_USE_MODULE`) by default for toolchains other than the Zephyr SDK, and the
  toolchain's own copy (`CONFIG_PICOLIBC_USE_TOOLCHAIN`) when the toolchain provides it or a full
  C++ library is required. Newlib is selected explicitly or when a full libc is required.
- **Warnings:** different compilers flag different issues; projects with
  `CONFIG_COMPILER_WARNINGS_AS_ERRORS` may need fixes per toolchain.
- **Linker:** the `host/llvm` Kconfig has `LLVM_USE_LD` and `LLVM_USE_LLD` options; IAR and Arm
  Compiler 6 use their own linkers through Zephyr's CMake linker script generator, and some GNU
  ld template features are not fully supported.
- **Subsystems:** some Zephyr code relies on GNU intrinsics and may not fully work with `iar` or
  `armclang`.
- **Sanitizers:** `native_sim` supports Address Sanitizer via `CONFIG_ASAN`.

## CI matrix
Build the main targets with the SDK, plus one job with the alternate toolchain used in
production (for example `gnuarmemb` or `iar`). Pin exact toolchain versions.

## Verify
- [ ] `build/CMakeCache.txt` shows the intended `ZEPHYR_TOOLCHAIN_VARIANT` and compiler path.
- [ ] Each toolchain in the CI matrix builds pristine and passes the same tests.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the variants and their environment variables (toolchains pages: gnu_arm_embedded, other_x_compilers, iar_arm_toolchain, host, intel_oneapi_toolkit, arm_compiler_6, cadence_xcc), the cmake/toolchain variant directory list, and picolibc source selection and default libc (lib/libc/Kconfig, lib/libc/picolibc/Kconfig). Wrong in the draft: the host variants are host/gnu and host/llvm (not host), picolibc comes from the module for non-SDK toolchains rather than newlib, the IAR 4.1+ gate was unsupported (docs say IAR v9.70 or newer, minimal libc only, no C++), and the standalone llvm variant is not in cmake/toolchain. Removed the pinned GNU Arm version string.
Method: documentation only; no commands were run.
