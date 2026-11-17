---
id: computing-software.firmware-embedded-development.zephyr.troubleshooting-devicetree-errors
name: troubleshooting-devicetree-errors
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [devicetree-troubleshooting, dt-n-undefined, device-dt-get-undefined, zephyr-dts, devicetree-errors, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Decode Zephyr devicetree build errors like undefined __device_dts_ord_N or DT_N_... macros: check zephyr.dts, binding match, status, driver Kconfig, and overlay names."
sources:
  - https://docs.zephyrproject.org/latest/build/dts/troubleshooting.html
  - https://docs.zephyrproject.org/latest/build/dts/howtos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting devicetree errors

## Step 0: pristine build, then look at the final tree
Try a pristine build directory first: devicetree outputs are created during CMake configuration
and are not always regenerated when an input changes. Then inspect `build/zephyr/zephyr.dts` (the
final merged devicetree) and `build/zephyr/include/generated/zephyr/devicetree_generated.h`.
The optional DT Doctor diagnostics tool is enabled with `-DZEPHYR_SCA_VARIANT=dtdoctor`.
Unlike Kconfig symbols, `<devicetree.h>` must be included explicitly (other headers may include
it transitively, but that is not guaranteed).

## `undefined reference to '__device_dts_ord_N'`
`DEVICE_DT_GET(NODE_ID)` used a valid node identifier, but no driver allocated a `struct device`
for that node. Check:
1. The node has `status = "okay"` (or no `status`) in `zephyr.dts`. The ordinal `N` maps to a node
   in the "Node dependency ordering (ordinal and path)" list at the top of
   `devicetree_generated.h`. Enable it in an overlay (`&i2c0 { status = "okay"; };`) and do a
   pristine build.
2. A driver that allocates devices for the node's `compatible` is compiled in: find its Kconfig
   option in the drivers' `CMakeLists.txt` (for example `zephyr_library_sources_ifdef(CONFIG_X ...)`)
   and make sure it is `y` in `build/zephyr/.config`. Often it turns on automatically once the
   node is enabled; otherwise set it in `prj.conf`, watching for unmet Kconfig dependencies.

## Undeclared `DT_...` macros and wrong names
- In C, devicetree names are lower-cased with special characters converted to underscores
  (`DT_PATH(soc, i2c_1234000)`, `clock_frequency`). In overlays, use normal DTS spelling
  (`&{/soc/i2c@12340000/} { clock-frequency = <115200>; };`).
- Check the node identifier with `#if !DT_NODE_EXISTS(DT_NODELABEL(my_serial))` and `#error`.
  If the node exists, check that the property exists, that the node has a matching binding, and
  that the binding defines the property.
- Missing binding: the node's `compatible` is absent, mistyped, or has no matching binding. If
  the binding file is outside `zephyr/dts`, you may need `DTS_ROOT`.
- `DT_INST_*` macros need `DT_DRV_COMPAT` defined to the lower-case-and-underscores compatible.
- Long compiler messages from macro expansion: build with
  `-DCONFIG_COMPILER_TRACK_MACRO_EXPANSION=n`; to read the expanded result enable
  `CONFIG_COMPILER_SAVE_TEMPS=y`, which writes `foo.c.i` for each source file.

## Overlay not applied
- Without `DTC_OVERLAY_FILE`, the build looks in the application configuration directory for
  `socs/<SOC>_<BOARD_QUALIFIERS>.overlay`, then `boards/<BOARD>.overlay` (plus
  `boards/<BOARD>_<revision>.overlay`); if none exist it tries `<BOARD>.overlay`, then
  `app.overlay`.
- Setting `DTC_OVERLAY_FILE` replaces that search, and its value is stored in the CMake cache for
  later builds. `EXTRA_DTC_OVERLAY_FILE` adds files and takes precedence over the others.
- Files with relative paths come from the application configuration directory; only absolute
  paths are taken from elsewhere. Shields also add overlays.
- The configuration phase prints `-- Found devicetree overlay: <path>` for each overlay it uses;
  if yours is absent it was not picked up.

## Runtime: `device_is_ready()` false
The device exists but its driver init failed or has not run. This is a runtime problem, not the
link-time error above: check the driver's own logging and the node's bus, address and pin
configuration.

## Verify
- [ ] Node present with `okay` status and the right compatible in `zephyr.dts`.
- [ ] Driver and subsystem Kconfigs `=y` in `.config`.
- [ ] CMake log shows the expected overlays.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the undefined __device_dts_ord_N causes and ordinal lookup, pristine-build advice, DT Doctor option, name-conversion rules, DT_NODE_EXISTS check, missing-binding advice, DT_DRV_COMPAT, CONFIG_COMPILER_SAVE_TEMPS and CONFIG_COMPILER_TRACK_MACRO_EXPANSION (build/dts/troubleshooting page), and the overlay search order, DTC_OVERLAY_FILE and EXTRA_DTC_OVERLAY_FILE behaviour and the Found devicetree overlay message (build/dts/howtos page). Wrong in the draft: the node ordinal is found in the Node dependency ordering list, not by searching for DT_N_..._ORD. Removed the dtc/edtlib error-message table because the exact messages are not in the docs.
Method: documentation only; no commands were run.
