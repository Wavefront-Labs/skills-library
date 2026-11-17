---
id: computing-software.firmware-embedded-development.zephyr.migrating-boards-to-hwmv2
name: migrating-boards-to-hwmv2
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [hwmv2-migration, board-conversion, convert-board-script, board-yml-migration, zephyr-3-7-upgrade, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Migrate an out-of-tree Zephyr board and SoC from the pre-3.6 hardware model to HWMv2: the conversion script, Kconfig.board rewrite, file renames, and new target names."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/v4.3.0/scripts/utils/board_v1_to_v2.py
  - https://docs.zephyrproject.org/latest/releases/migration-guide-3.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating boards to HWMv2

Hardware model v2 (HWMv2) was introduced shortly after Zephyr 3.6.0 and is the only model from
3.7.0 onwards; the project chose not to keep backwards compatibility. Out-of-tree boards from
older releases fail with errors like `No board named 'x' found` or Kconfig `BOARD_X` undefined.

## What changed
| v1 | v2 |
|---|---|
| `boards/<arch>/<board>/` | `boards/<vendor>/<board>/` |
| `Kconfig.board` with `config BOARD_X bool "..." depends on SOC_Y` | `board.yml` + `Kconfig.<board>` with `select SOC_Y` |
| Board name only (`nrf5340dk_nrf5340_cpuapp`) | Target string (`nrf5340dk/nrf5340/cpuapp`) |
| Old SoC definitions | SoC tree described by `soc.yml` plus `Kconfig.soc` (see the SoC porting guide) |
| `Kconfig.defconfig` `if BOARD_X` | still wrapped in `if BOARD_<NAME>` |

## Convert with the script
```bash
python $ZEPHYR_BASE/scripts/utils/board_v1_to_v2.py \
    --board-root <repo> -b widget -g acme -v acme -s nrf52840
```
`scripts/utils/board_v1_to_v2.py` ships in Zephyr 3.7 to 4.3 (it is absent from 4.4 and main, so use
a 4.3 checkout of the script). Required arguments: `-b/--board`, `-g/--group` (the folder that
groups boards), `-v/--vendor`, `-s/--soc`; `-n/--new-board` renames, `--variants` handles variants,
`--board-root` points at an out-of-tree board root. It writes `board.yml` and `Kconfig.<board>`, but
its own documentation says it is not a complete migration tool (multi-core SoCs in particular), so
review the output and finish by hand.

## Manual pieces
`board.yml`:
```yaml
board:
  name: widget
  vendor: acme
  revision:                       # only if the board had revisions
    format: letter
    default: B
    revisions: [{name: A}, {name: B}]
  socs:
    - name: nrf52840
```
`Kconfig.widget`:
```kconfig
config BOARD_WIDGET
    select SOC_<SOC_SYMBOL>      # the Kconfig symbol of the SoC your board uses
```
Then rename the DTS, defconfig and yaml files to `<board>_<normalized qualifiers>` (qualifiers with
`/` replaced by `_`, e.g. `widget_nrf52840.dts`), as the board porting guide describes.

## Update the rest of the repo
- App overlays/confs: `boards/<old>.overlay` -> normalized new names.
- CI scripts and `west build -b` invocations: new target strings.
- C code using `CONFIG_BOARD_<OLD>` symbols: the build system defines `BOARD_<board>` and
  `BOARD_<normalized board target>` symbols (for example `CONFIG_BOARD_WIDGET` and
  `CONFIG_BOARD_WIDGET_NRF52840`).
- `sample.yaml`/`testcase.yaml` `platform_allow` lists.
- Sysbuild files referencing board names.

## Verify
- [ ] `west boards | grep widget` (or `west boards -n widget`) lists the board.
- [ ] Pristine builds of every app/variant succeed with new targets.
- [ ] `.config` and `zephyr.dts` identical (modulo symbol names) to a pre-migration build.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the board porting guide: the new hardware model arrived shortly after 3.6.0 and applies from 3.7.0, with no backwards compatibility and the option of copying the 3.6.0 SoC definition; `board.yml` schema (name, vendor, revision format/default/revisions, socs); `Kconfig.<board>` containing `config BOARD_X` with `select SOC_...` and no type, with `BOARD_<board>` and `BOARD_<normalized board target>` built by the build system; qualifier normalisation (`/` becomes `_` in file names); board target format; `west boards -n/--name`. Confirmed in the 4.2.0 script source: its arguments and the fact that it writes `board.yml` and `Kconfig.<board>`; it exists in v3.7.0 to v4.3.0 and returns 404 from v4.4.0 and main.
Wrong claims fixed: "3.7 removed v1" (v1 was replaced by v2 in 3.7); the script needs `-g/--group` and is no longer in current Zephyr; removed the claimed `soc_v1_to_v2.py` (not found in the tree), the twister `identifier:` remark and the unconfirmed old SoC layout.

Method: documentation only; no commands were run.
