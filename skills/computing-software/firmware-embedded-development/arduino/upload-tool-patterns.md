---
id: computing-software.firmware-embedded-development.arduino.upload-tool-patterns
name: upload-tool-patterns
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [upload-pattern, platform-txt-tools, upload-use-1200bps-touch, upload-wait-for-upload-port, network-upload, programmer-upload, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Define upload recipes in an Arduino core: tools.<tool>.upload.pattern, verbose/quiet params, 1200-bps touch and port waiting, program/bootloader patterns, network upload."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/ArduinoCore-samd/blob/master/platform.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upload tool patterns

## Anatomy (platform.txt)
```properties
tools.bossac.path={runtime.tools.bossac-1.7.0-arduino3.path}
tools.bossac.cmd=bossac
tools.bossac.cmd.windows=bossac.exe
tools.bossac.upload.params.verbose=-i -d
tools.bossac.upload.params.quiet=
tools.bossac.upload.params.verify=-v
tools.bossac.upload.params.noverify=
tools.bossac.upload.pattern="{path}/{cmd}" {upload.verbose} --port={serial.port.file} -U {upload.native_usb} -i -e -w -v "{build.path}/{build.project_name}.bin" -R
```
(Copied from the SAMD core's `platform.txt`; the exact flags are bossac-specific.)
- Board selects the tool per protocol: `myboard.upload.tool.serial=bossac`, `myboard.upload.tool.network=...`,
  and `myboard.upload.tool.default=bossac` when no port address is given. The older `upload.tool=` form is
  equivalent to `upload.tool.default=`.
- `{upload.verbose}` expands to `params.verbose` or `params.quiet` depending on the user's verbose
  setting; `{upload.verify}` uses `params.verify` or `params.noverify` the same way.
- Port variables: `{upload.port.address}` (for example `/dev/ttyACM0`), `{upload.port.label}`,
  `{upload.port.protocol}`, `{upload.port.properties.<prop>}` (pluggable discovery). Backward-compatible:
  `{serial.port}` (same as the address) and `{serial.port.file}` (file part, serial protocol only).

## Bootloader entry helpers (boards.txt)
```properties
myboard.upload.use_1200bps_touch=true      # open port at 1200 baud, close -> bootloader
myboard.upload.wait_for_upload_port=true   # wait for re-enumerated port after the touch
```
For boards with native USB (such as the Leonardo or Zero), where the running sketch interprets a 1200 bps
open as the request to start the bootloader. `wait_for_upload_port` is only used together with
`use_1200bps_touch`.

## Other recipes
- `tools.<t>.program.pattern` — "Upload Using Programmer" (ISP/SWD), with `program.params.*`.
- `tools.<t>.erase.pattern` and `tools.<t>.bootloader.pattern` — "Burn Bootloader": the two actions run in
  sequence, `erase` first (typically erases flash and sets fuses from the board definition), then `bootloader`.
- `tools.<t>.upload.network_pattern` — upload over the network to `{upload.port.address}`.
- `upload.field.password=Password` with `upload.field.password.secret=true` asks the user for
  network upload credentials.

## Debugging an upload recipe
```sh
arduino-cli upload -b acme:samd:sense -p /dev/ttyACM0 -v --input-dir build
arduino-cli compile -b acme:samd:sense --show-properties     # inspect the expanded tool properties
```
Verbose output prints the expanded command; run it manually to isolate tool issues.

## Gotchas
- Quote paths in patterns (`"{path}/{cmd}"`); spaces in user names break unquoted commands.
- `.windows`/`.linux`/`.macosx` suffixes override any key per OS.
- `{runtime.tools.TOOLNAME.path}` and `{runtime.tools.TOOLNAME-TOOLVERSION.path}` are generated for the
  tools the platform depends on; the name and version must match the package index.

## Verify
- [ ] Upload works from IDE and CLI, verbose and quiet, on all three host OSes.
- [ ] Native-USB board can still be uploaded after a sketch that breaks its USB stack (bootloader entry documented for the board).

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 platform specification on master (commit 2026-10-22); ArduinoCore-samd platform.txt (latest commit 2026-09-10).

Confirmed: the bossac tool block (`tools.bossac.cmd`, `.cmd.windows`, `upload.params.verbose` and `quiet`, `upload.pattern` with `--port={serial.port.file}`) against the SAMD platform.txt, including the tool path version `bossac-1.7.0-arduino3`; `upload.tool.<protocol>` and `upload.tool.default` with the legacy `upload.tool`; `{upload.verbose}` and `{upload.verify}` from `params.*`; port properties `{upload.port.address}`, `{upload.port.label}`, `{upload.port.properties.*}`, `{serial.port}` and `{serial.port.file}`; `use_1200bps_touch` and `wait_for_upload_port`; `program`, `erase`, `bootloader` and `network_pattern` recipes; `upload.field.*` with `.secret`; OS suffixes `.linux`, `.windows`, `.macosx`. Removed claims no document covers: `upload.native_usb`, the "CLI 0.30+" gate, the espota example and the `grep` pipeline.

Method: documentation only; no commands were run.
