---
id: computing-software.firmware-embedded-development.zephyr.zephyr-sdk-installation
name: zephyr-sdk-installation
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-sdk, west-sdk-install, zephyr-sdk-install-dir, toolchain-setup, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Install and register the Zephyr SDK (toolchains, host tools, CMake package) via west sdk install or the setup script, pick versions matching Zephyr, and fix detection errors."
sources:
  - https://docs.zephyrproject.org/latest/develop/toolchains/zephyr_sdk.html
  - https://docs.zephyrproject.org/latest/develop/getting_started/index.html
  - https://docs.zephyrproject.org/latest/develop/west/zephyr-cmds.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/west_commands/sdk.py
  - https://github.com/zephyrproject-rtos/sdk-ng/blob/main/scripts/template_setup_posix
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr SDK installation

The Zephyr SDK bundles GNU and LLVM toolchains for each supported architecture (ARC, Arm, Microblaze,
MIPS, RISC-V, RX, SPARC, x86, Xtensa) plus host tools such as a custom QEMU and OpenOCD. The bundle
comes in three variants: `gnu` (GNU toolchains and host tools), `llvm` (LLVM/Clang and host tools) and
`minimal` (host tools only; toolchains are chosen and downloaded during setup).

## Recommended: west sdk
```bash
west sdk install                       # version detected from ${ZEPHYR_BASE}/SDK_VERSION unless --version is given
west sdk install -t arm-zephyr-eabi riscv64-zephyr-elf   # only some GNU toolchains (non-interactive)
west sdk list                          # installed SDKs, available releases and their toolchains
```
Other options from the west sdk command: `--version`, `--install-base`, `--install-dir`,
`--interactive`, `-l/--llvm`, `-T/--no-gnu-toolchains` and `-H/--no-hosttools`. Without `-t`, GNU
toolchains for all architectures are installed (several gigabytes). The Zephyr docs page spells the
toolchain option `--toolchains`; check `west sdk install -h` for your release.

## Manual
Download the bundle (and its checksum) from the sdk-ng releases page, extract it, and run the
setup script once:
```bash
tar xvf zephyr-sdk-<ver>_linux-x86_64_gnu.tar.xz -C ~/
cd ~/zephyr-sdk-<ver>
./setup.sh -t arm-zephyr-eabi -h -c    # -t GNU toolchain, -h host tools, -c register CMake package
sudo cp ~/zephyr-sdk-<ver>/hosttools/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
sudo udevadm control --reload
```
Running `./setup.sh` with no options prompts for each choice. Rerun setup if you move the SDK
directory. On Windows use the `.7z` bundle and `setup.cmd`; on macOS use the `macos-*` archive.
Recommended extraction locations on Linux: `$HOME`, `$HOME/.local`, `$HOME/.local/opt`,
`$HOME/bin`, `/opt`, `/usr/local`.

## Version matching
Zephyr's `SDK_VERSION` file names the recommended SDK version for that Zephyr version; the full
list of compatible pairs is the Zephyr SDK Version Compatibility Matrix in the sdk-ng wiki. Pin the
SDK in CI (container image or cached bundle) to the version developers use, because a toolchain
upgrade can introduce new compiler warnings.

## How the build finds it
- If no other toolchain is selected, the build system looks for the Zephyr SDK and uses its
  toolchain; `ZEPHYR_TOOLCHAIN_VARIANT=zephyr` enforces this.
- Outside the default locations, the SDK is found automatically only if registered in the CMake
  package registry by the setup script (`-c`); otherwise set `ZEPHYR_SDK_INSTALL_DIR`.
- `ZEPHYR_SDK_INSTALL_DIR` may also point to a directory holding several `zephyr-sdk-<version>`
  folders, and the build system picks the matching one.

## Common errors
| Error | Fix |
|---|---|
| CMake cannot find a package configuration file for "Zephyr-sdk" | run the setup script with `-c`, or set `ZEPHYR_SDK_INSTALL_DIR` |
| SDK older than the Zephyr tree expects | install the version in `SDK_VERSION` |
| Toolchain for an architecture is missing | rerun `setup.sh -t <toolchain>` or `west sdk install -t <toolchain>` |
| Stale build after SDK change | pristine build (`west build -p always`), since CMake caches settings |

## Verify
- [ ] `west sdk list` shows the expected installed version.
- [ ] `west build -b qemu_x86 samples/hello_world -t run` works on a clean shell.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2; SDK_VERSION file 1.0.1; sdk-ng v1.0.1). Confirmed bundle variants gnu/llvm/minimal, supported architectures, extraction locations, discovery rules and multi-SDK ZEPHYR_SDK_INSTALL_DIR (zephyr_sdk toolchain page), west sdk install/list and options including SDK_VERSION detection (scripts/west_commands/sdk.py), setup.sh -t/-l/-h/-c usage (sdk-ng template_setup_posix). Wrong in the draft: udev rules path is under hosttools/, the 4.0+ version gate and the dtc, GCC 12 to 14 and newer-SDK-works-with-older-Zephyr claims were unconfirmed (removed); the west docs page and the source differ on the toolchain option spelling (-t/--gnu-toolchains in source).
Method: documentation only; no commands were run.
