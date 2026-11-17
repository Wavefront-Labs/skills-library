---
id: computing-software.firmware-embedded-development.zephyr.extra-conf-file-and-file-suffix
name: extra-conf-file-and-file-suffix
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [extra-conf-file, file-suffix, conf-file, build-variants, overlay-config, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build debug/release/test variants of a Zephyr app with EXTRA_CONF_FILE, EXTRA_DTC_OVERLAY_FILE and FILE_SUFFIX instead of copying prj.conf, and know how CONF_FILE differs."
sources:
  - https://docs.zephyrproject.org/latest/develop/application/index.html#file-suffixes
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html#the-initial-configuration
  - https://docs.zephyrproject.org/latest/build/sysbuild/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXTRA_CONF_FILE and FILE_SUFFIX

## EXTRA_CONF_FILE: add fragments
```bash
west build -b nrf52840dk/nrf52840 app -- -DEXTRA_CONF_FILE="debug.conf;usb-console.conf"
```
- Fragments are "mixed in" while `CONF_FILE` stays at its default (`prj.conf`).
- Separate several files with semicolons or spaces. Files are taken from the application
  configuration directory unless the path is absolute.
- Companion: `-DEXTRA_DTC_OVERLAY_FILE=debug.overlay` adds devicetree overlays while
  `DTC_OVERLAY_FILE` stays at its default.

## CONF_FILE: replace the base
`-DCONF_FILE=prj_release.conf` names the application configuration instead of `prj.conf`
(the docs list `boards/<BOARD>.conf` merging only for the case where `CONF_FILE` is not set).
Use only when the base genuinely differs; otherwise you duplicate settings.

## FILE_SUFFIX: switch every file at once
```bash
west build -b nrf52840dk/nrf52840 app -- -DFILE_SUFFIX=release
```
The suffix is appended to Kconfig fragment and board overlay names; if the suffixed file does not
exist, Zephyr falls back to the name without the suffix:
```
app/
  prj.conf              prj_release.conf
  boards/nrf52840dk_nrf52840.overlay   boards/nrf52840dk_nrf52840_release.overlay
```
With `FILE_SUFFIX=release` this picks `prj_release.conf` and the `_release` overlay; a board with no
`_release` overlay uses its plain overlay. Under sysbuild the suffix applies to every image, or to
one image with `-D<image>_FILE_SUFFIX=<suffix>`.

## Choosing
| Need | Mechanism |
|---|---|
| Add a few options (logging, test hooks) | `EXTRA_CONF_FILE` |
| Several orthogonal toggles | multiple fragments in `EXTRA_CONF_FILE` |
| Whole parallel variant across conf + overlays | `FILE_SUFFIX` |
| Reusable across apps | a snippet (`-S`) |

## Twister / CI
```yaml
tests:
  app.release:
    extra_args: FILE_SUFFIX=release
  app.debug:
    extra_args: EXTRA_CONF_FILE=debug.conf
```

## Gotchas
- Values given with `-D` are stored in the CMake cache of an existing build directory; use a
  separate build directory per variant, or `west build -p` (`--pristine`) when switching.
- Quote semicolon-separated lists in the shell.

## Verify
- [ ] `build/zephyr/.config` contains the options from the expected fragments per variant.
- [ ] `.config` diff between variants contains only intended differences.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed against the application development page (CONF_FILE, EXTRA_CONF_FILE, EXTRA_DTC_OVERLAY_FILE, FILE_SUFFIX fallback rule and example), the Kconfig setting page (initial configuration) and the sysbuild page (FILE_SUFFIX and <image>_FILE_SUFFIX), plus twister extra_args. Removed the Zephyr 3.6 gate, OVERLAY_CONFIG deprecation, suffixed board .conf, snippet suffix and prj_<board>.conf claims, which the docs do not state.
Method: documentation only; no commands were run.
