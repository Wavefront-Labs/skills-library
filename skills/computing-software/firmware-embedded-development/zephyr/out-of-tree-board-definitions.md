---
id: computing-software.firmware-embedded-development.zephyr.out-of-tree-board-definitions
name: out-of-tree-board-definitions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [board-porting, out-of-tree-board, board-root, zephyr-module-yml, shield-definition, custom-soc, extending-boards, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep a product's custom Zephyr boards (and shields) outside the Zephyr tree: BOARD_ROOT, module.yml board_root, board extensions and keeping them building across upgrades."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://docs.zephyrproject.org/latest/develop/application/index.html
  - https://docs.zephyrproject.org/latest/develop/modules.html
  - https://docs.zephyrproject.org/latest/hardware/porting/shields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-tree board definitions

**Goal:** product hardware definitions live in your repository, versioned with your app, and
upstream Zephyr stays unmodified.

## Making Zephyr find them
Directory structure must mirror Zephyr's: `<root>/boards/<vendor>/<board>/...` (and
`<root>/soc/...`, `<root>/dts/bindings/...` if needed).
- Per build: `west build -b sensor_node app -- -DBOARD_ROOT=<path to the root>` (relative paths are
  relative to the application directory).
- In app CMake (before `find_package(Zephyr)`): `list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/..)`;
  an absolute path is required there.
- Best: make the repo a **Zephyr module**:
  ```yaml
  # zephyr/module.yml
  build:
    settings:
      board_root: .
      dts_root: .
      soc_root: .
  ```
  and list the repo in the west manifest; every app in the workspace then sees the boards.

## Shields for add-on hardware
Daughter boards (display, sensor shield) are shields: a folder under `boards/shields/<name>/` with
`Kconfig.shield`, `Kconfig.defconfig` and `<name>.overlay`, activated with `--shield <name>` in
`west build`. Keep the base board unaware of optional add-ons.

## Board extensions
Extend an **existing** board with new variants from your own repository, with `board.yml`
`extend:` instead of copying the whole board (the folder then holds `plank_<new-qualifiers>_defconfig`
and `.dts`, and optionally `board.cmake`, `Kconfig`, `Kconfig.<board>`, `Kconfig.defconfig`):
```yaml
board:
  extend: nrf52840dk
  variants:
    - name: product
      qualifier: nrf52840
```

## Keeping it working across upgrades
- Base your board on the closest upstream board and diff against it when upgrading Zephyr:
  upstream changes (pinctrl, clock bindings, HWMv2) must be ported to your copy.
- Run Twister on your boards in CI (`west twister -T <tests> -A <board root> -p sensor_node`; `-A` is
  `--board-root`).
- Out-of-tree SoC support (rare) needs `soc.yml` and SoC Kconfig; see the SoC porting guide.

## Verify
- [ ] `west boards -n sensor_node` lists the board (with the repo registered as a module);
      the build works from a clean workspace.
- [ ] CI builds every app for every in-repo board after a Zephyr version bump.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the application, board porting, shields and modules docs: custom board folder under `boards/<vendor>/`, `-DBOARD_ROOT` (relative to the application directory) and setting `BOARD_ROOT` in CMakeLists.txt before `find_package(Zephyr)` with an absolute path; module.yml settings `board_root`, `dts_root`, `soc_root`; shield files and `--shield`; board extensions via `extend:` with `variants` and `qualifier`, limited to new variants (file list from the guide); twister `-A/--board-root`; `west boards -n`.
Removed or fixed: board extensions can add variants, not revisions or defconfig-only fragments, and the "Zephyr 4.0+" version gate was not found in the release notes; `west boards` has no `--board-root` option in 4.4.2; the `$PWD/..` path example.

Method: documentation only; no commands were run.
