---
id: computing-software.firmware-embedded-development.zephyr.board-yml-hardware-model-v2
name: board-yml-hardware-model-v2
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [board-porting, hwmv2, board-yml, board-qualifiers, soc-cpucluster-variant, board-revision, board-target-string, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Describe a Zephyr board with hardware model v2: board.yml, board target strings with SoC/cluster/variant qualifiers, revisions, and the file naming that follows from them."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/utils/board_v1_to_v2.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board definition with hardware model v2

**Goal:** a board directory in the current hardware model (introduced shortly after Zephyr 3.6.0)
that Zephyr recognises, with targets for every SoC/core and variant the board supports.

## Directory and board.yml
```
boards/acme/sensor_node/
  board.yml
  board.cmake
  Kconfig.sensor_node            # selects the SoC
  Kconfig.defconfig              # board-level defaults (optional)
  sensor_node.dts                # <board>_<qualifiers>.dts, one per target
  sensor_node_defconfig          # <board>_<qualifiers>_defconfig, one per target
  sensor_node.yaml               # twister metadata
```
```yaml
# board.yml
board:
  name: sensor_node
  full_name: ACME Sensor Node
  vendor: acme
  socs:
    - name: nrf52840
```
```
# Kconfig.sensor_node  (selects the SoC; the BOARD_* symbol type is created by the build system)
config BOARD_SENSOR_NODE
	select SOC_NRF52840_QIAA
```

## Board target strings
`<board>[@<revision>][/<soc>[/<cpucluster>[/<variant>]]]`, e.g.
`nrf5340dk/nrf5340/cpuapp/ns`, `sensor_node@2.0.0`. The SoC can be omitted when the board has one
single-core SoC (use `//` to skip it when qualifiers follow). Build with
`west build -b sensor_node`. Board qualifiers are normalized for file names by replacing `/` with
`_`: `nrf5340dk_nrf5340_cpuapp_ns.dts`, `nrf5340dk_nrf5340_cpuapp_ns_defconfig`.

## Variants and revisions
- Variants (`ns` for TrustZone non-secure, `xip`, ...) are declared under `socs: - name: ...
  variants:` in board.yml, each with its own DTS/defconfig.
- Revisions: `revision: {format: major.minor.patch, default: "1.0.0", revisions: [{name:
  "1.0.0"}, {name: "2.0.0"}]}` (formats: `major.minor.patch`, `letter`, `number`, `custom`;
  `exact: true` rejects unlisted revisions). Revision adjustments are extra files applied on top of
  the base ones: `<board>_<qualifiers>_<revision>.overlay` and
  `<board>_<qualifiers>_<revision>_defconfig`, e.g. `sensor_node_nrf52840_2_0_0.overlay`.

## Migrating from HWMv1
The previous hardware model is obsolete (its documentation is in Zephyr v3.6.0 and earlier).
Zephyr ships a conversion script, `scripts/utils/board_v1_to_v2.py`; review its output, make
`Kconfig.<board>` select the SoC, and rename files to the target-based names.

## Verify
- [ ] `west boards | grep sensor_node` lists it; `west build -b sensor_node samples/hello_world` builds.
- [ ] Every declared target (core/variant/revision) builds in CI.

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, post-4.4; latest release v4.4.2): doc/hardware/porting/board_porting.rst and the scripts/utils/board_v1_to_v2.py link it gives.
Confirmed: the hardware model introduced shortly after Zephyr 3.6.0; board target grammar `<board>[@<revision>][/<soc>[/<cpucluster>][/<variant>]]` and the `//` rule for omitting the SoC; `/` to `_` normalization in file names; `board.yml` structure (`board:` with `name`, `full_name`, `vendor`, `socs`, `variants`, `revision` with `format`, `default`, `exact`, `revisions`); `<board>_<qualifiers>_<revision>.overlay` and `_defconfig`; `Kconfig.<board>` selecting the SoC; the conversion script.

Method: documentation only; no commands were run.
