---
id: computing-software.firmware-embedded-development.zephyr.inspecting-the-merged-dotconfig
name: inspecting-the-merged-dotconfig
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [dotconfig, merged-config, menuconfig, guiconfig, kconfig-fragments, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find out why a Zephyr Kconfig option has its value: read build/zephyr/.config, trace fragment merge order, use menuconfig symbol info, and save minimal configs."
sources:
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html
  - https://docs.zephyrproject.org/latest/build/kconfig/menuconfig.html
  - https://docs.zephyrproject.org/latest/build/kconfig/tracing.html
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting the merged .config

`prj.conf` is input; `build/zephyr/.config` is what the build actually used.

## Sources of the initial configuration
The initial configuration merges three sources:
1. The board's `<board>_defconfig`
2. CMake cache entries prefixed `CONFIG_` (for example `-DCONFIG_FOO=y`)
3. The application configuration: `CONF_FILE` if set, otherwise `prj.conf` (merged with
   `boards/<BOARD>.conf` when that exists), plus any `EXTRA_CONF_FILE` fragments

If a symbol is set both in `<board>_defconfig` and in the application configuration, the
application value wins. An `socs/<SOC>_<BOARD_QUALIFIERS>.conf` fragment, if present, is applied
after the main application configuration and before board fragments.

Warnings like `CONFIG_X was assigned the value y but got the value n` mean dependencies are not
met; that's the most common reason an option "won't turn on". They are only printed unless
`-DKCONFIG_WARNING_AS_ERROR=y` is set.

## Checking values
```bash
grep -E "CONFIG_(LOG|SHELL)=" build/zephyr/.config
grep "# CONFIG_ASSERT is not set" build/zephyr/.config
```
Options with unmet dependencies don't appear at all (not even "is not set").

## Interactive inspection
```bash
west build -t menuconfig     # or guiconfig
```
- `/` jumps to a symbol by name; if it is not visible, show-all mode turns on (`A` toggles it off).
- `?` on a symbol shows its help, direct dependencies, defaults and the symbols currently
  y-selecting or y-implying it. This answers "who selected this?".
- Changes made here go to `zephyr/.config`; make a setting permanent in a `*.conf` file.

## Saving and tracing
- `D` in menuconfig saves a minimal configuration file listing only symbols that differ from
  their defaults; copy the relevant lines into `prj.conf` or a fragment (do not commit `.config`).
- `west build -t traceconfig` writes a file in the build directory that details how each symbol
  got its final value. Run it on a pristine build: an existing `.config` pins every setting.
- `west build -t hardenconfig` reports security-relevant recommendations.

## Diffing two builds
```bash
diff <(grep ^CONFIG_ buildA/zephyr/.config | sort) <(grep ^CONFIG_ buildB/zephyr/.config | sort)
```

## Gotchas
- Assigning a symbol with unsatisfied dependencies directly in `.config` is ignored and
  overwritten when the build reconfigures. As long as `.config` is newer than the board and
  application configuration files, it is reused instead of re-merged.
- `CONFIG_FOO=n` in a fragment is spelled `# CONFIG_FOO is not set` in `.config`; both forms are
  accepted in fragments.
- Sysbuild builds one `.config` per image (under `<build>/<image>/zephyr`). The main application
  uses the targets unprefixed; other images (and sysbuild itself) use an image prefix such as
  `mcuboot_menuconfig` or `sysbuild_menuconfig`.

## Verify
- [ ] Every option you rely on confirmed in `.config`, not just in `prj.conf`.
- [ ] No "assigned ... but got" warnings in the CMake log (or build with `KCONFIG_WARNING_AS_ERROR=y`).

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the initial-configuration sources and precedence (Kconfig setting page), menuconfig keys and the minimal-config D key (menuconfig page), the traceconfig target and pristine-build note (tracing page), sysbuild per-image targets (sysbuild page) and the y-selecting/y-implying symbol info text (scripts/kconfig/menuconfig.py). Removed the incorrect 5-step merge order and the savedefconfig target, which the docs do not list.
Method: documentation only; no commands were run.
