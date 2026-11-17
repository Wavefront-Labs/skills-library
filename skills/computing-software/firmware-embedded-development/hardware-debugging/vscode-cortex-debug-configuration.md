---
id: computing-software.firmware-embedded-development.hardware-debugging.vscode-cortex-debug-configuration
name: vscode-cortex-debug-configuration
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [cortex-debug, vscode, launch-json, servertype, svdfile, swo-config, rtt-config, live-watch, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure VS Code Cortex-Debug launch.json for OpenOCD, J-Link, pyOCD or ST-LINK: servertype, svdFile, SWO and RTT config, attach vs launch, live watch."
sources:
  - https://github.com/Marus/cortex-debug/wiki
  - https://github.com/Marus/cortex-debug/blob/master/debug_attributes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VS Code Cortex-Debug

Attribute names and meanings below come from the extension's `debug_attributes.md`. IntelliSense in `launch.json`
shows defaults for each attribute.

## Minimal launch config
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug (OpenOCD)",
      "type": "cortex-debug",
      "request": "launch",
      "servertype": "openocd",
      "cwd": "${workspaceFolder}",
      "executable": "build/app.elf",
      "configFiles": ["<your-interface>.cfg", "<your-target>.cfg"],
      "svdFile": "${workspaceFolder}/svd/<your-chip>.svd",
      "runToEntryPoint": "main"
    }
  ]
}
```
- `servertype` options: `jlink`, `openocd`, `pyocd`, `pe`, `stlink`, `stutil`, `qemu`, `bmp` and `external`. The
  server executable in PATH is used unless `serverpath` overrides it.
- `external` needs `gdbTarget` (a `hostname:port` or serial port) for a server you start yourself.
- `configFiles` are OpenOCD `-f` files; `searchDir` is the `-s` list (defaults to `cwd`); `openOCDLaunchCommands`
  adds `-c` commands after the config files load.
- J-Link: `device`, `interface` (defaults to SWD; also used for ST-LINK and BMP), `serialNumber` when several probes are
  attached, `ipAddress` for networked J-Links, `jlinkscript`. PyOCD: `boardId`, `targetId`. ST-LINK: `stlinkPath`.
- `runToEntryPoint` runs to the start of the given function on launch/restart/reset (not attach); `breakAfterReset`
  is ignored when it is used.
- `svdFile` feeds the XPERIPHERALS window provided by the `mcu-debug.peripheral-viewer` extension.
- Toolchain: `armToolchainPath`, `gdbPath`, `objdumpPath` (with `nm` alongside) and `toolchainPrefix` (default
  `arm-none-eabi`) override the user settings per configuration.

## Launch vs attach
`"request": "attach"` skips flashing; `preAttachCommands`, `postAttachCommands` and `overrideAttachCommands` are the
attach-only hooks. For launch there are `preLaunchCommands`, `postLaunchCommands` and `overrideLaunchCommands`
(replaces the default flash and launch sequence; the manual prefers the pre/post hooks). Reset has
`preResetCommands`, `postResetCommands` and `overrideResetCommands`. `loadFiles` programs different files than
`executable`; `symbolFiles` loads symbols from other ELFs.

## Trace and logs
```json
"swoConfig": { "enabled": true, "cpuFrequency": 168000000, "swoFrequency": 2000000,
  "source": "probe", "decoders": [{ "type": "console", "port": 0, "label": "ITM0" }] },
"rttConfig": { "enabled": true, "address": "auto",
  "decoders": [{ "label": "RTT", "port": 0, "type": "console" }] }
```
- `swoConfig.cpuFrequency` is the target CPU frequency in Hz and `swoFrequency` the SWO frequency in Hz; `source` is
  `probe` or a serial device. Use your real clock values.
- `rttConfig.address` is where to search for the RTT control block; `"auto"` uses the address from the ELF.
  RTT is supported with J-Link and OpenOCD.

## Other features
- `liveWatch`: `enabled` and `samplesPerSecond`; the manual says live watch only applies to OpenOCD.
- `rtos`: for J-Link, names such as FreeRTOS or Zephyr (or a plugin path); for OpenOCD, `auto` (recommended) or a
  named RTOS.
- `hardwareBreakpoints` and `hardwareWatchpoints` can force hardware-only use and set limits, but the manual warns
  against it except to work around gdb-server or hardware issues.
- `numberOfProcessors` and `targetProcessor` select a core on multi-core devices.

## Gotchas
- `executable` is the path for symbols and program information; check it if GDB reports no symbol table.
- Use `serialNumber` when several J-Link or ST-LINK probes are connected.

## Verify
- [ ] F5 flashes, runs to `main`, and the peripheral view is populated from the SVD.
- [ ] SWO or RTT console prints the boot banner.

## Checked
Method: docs-checked 2026-11-09 against the Cortex-Debug debug_attributes.md (read in full) and the repository wiki landing page (fetched). Removed unconfirmed claims: specific interface/target config names, `preLaunchTask` and toolchain path examples, "core is halted on attach", live watch support for J-Link (the manual says OpenOCD only), extension v1.x gdbPath note, gdb-multiarch, ST-LINK_gdbserver via CubeCLT.
