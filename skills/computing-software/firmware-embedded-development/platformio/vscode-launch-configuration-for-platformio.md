---
id: computing-software.firmware-embedded-development.platformio.vscode-launch-configuration-for-platformio
name: vscode-launch-configuration-for-platformio
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-launch-json, launch-json, platformio-debug-type, vscode-debug, prelaunchtask, svdpath, platformio, firmware-embedded-development]
level: practitioner
status: draft
description: "Understand and customise the VS Code launch.json PlatformIO IDE generates: platformio-debug type, PIO Debug vs skip-pre-debug vs without-uploading, svdPath, and per-env configs."
sources:
  - https://docs.platformio.org/en/latest/integration/ide/vscode.html#debugging
  - https://docs.platformio.org/en/latest/plus/debugging.html
  - https://code.visualstudio.com/docs/editor/debugging
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VS Code launch configuration for PlatformIO

## Generated file
PlatformIO IDE regenerates `.vscode/launch.json` on project changes (unless you remove the
auto-generated marker comment). Typical entries:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "platformio-debug",
      "request": "launch",
      "name": "PIO Debug",
      "executable": "${workspaceFolder}/.pio/build/nucleo_f401re/firmware.elf",
      "projectEnvName": "nucleo_f401re",
      "toolchainBinDir": "${userHome}/.platformio/packages/toolchain-gccarmnoneeabi/bin",
      "internalConsoleOptions": "openOnSessionStart",
      "svdPath": "${userHome}/.platformio/platforms/ststm32/misc/svd/STM32F40x.svd",
      "preLaunchTask": { "type": "PlatformIO", "task": "Pre-Debug" }
    },
    { "type": "platformio-debug", "request": "launch", "name": "PIO Debug (skip Pre-Debug)", "...": "no preLaunchTask" },
    { "type": "platformio-debug", "request": "launch", "name": "PIO Debug (without uploading)", "loadMode": "manual" }
  ]
}
```
- **PIO Debug** — builds (Pre-Debug task), uploads per `debug_load_mode`, starts GDB.
- **skip Pre-Debug** — no build; uses the existing ELF (fast restarts when you know nothing
  changed).
- **without uploading** — attaches and loads symbols only.

## Customising safely
- Settings that should apply everywhere belong in `platformio.ini` (`debug_tool`, `debug_init_break`,
  `debug_extra_cmds`, `debug_svd_path`) because the IDE regenerates launch.json.
- To keep a hand-edited launch.json, delete the "AUTOMATICALLY GENERATED FILE" header comment; PIO
  stops overwriting it. Then maintain env names and paths yourself.
- Multiple envs: the debug config follows the selected/default env (`default_envs` or the env
  switcher in the status bar). Add explicit configs per env (`projectEnvName`) for boards you debug
  often.
- `debug_svd_path = svd/custom.svd` in platformio.ini sets the peripheral view source.

## Using Cortex-Debug instead
Possible for advanced features (live watch, RTT decoders): `"type": "cortex-debug"`, executable from
`.pio/build/<env>/firmware.elf`, `"servertype": "openocd"` with the same configs PIO uses, and a
preLaunchTask running `pio run -e <env>`. You then manage server paths yourself.

## Verify
- [ ] F5 on the intended env builds, flashes and stops at the init breakpoint.
- [ ] Peripheral view shows registers from the configured SVD.
