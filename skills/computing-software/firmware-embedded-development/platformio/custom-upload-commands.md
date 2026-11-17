---
id: computing-software.firmware-embedded-development.platformio.custom-upload-commands
name: custom-upload-commands
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [custom-upload, upload-command, uploadcmd, upload-protocol-custom, replace-uploader, mcumgr-upload, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Upload with your own tool in PlatformIO: upload_protocol = custom with upload_command, build variables, and adjusting UPLOADCMD from an extra script."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/upload/upload_command.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/upload/upload_protocol.html
  - https://docs.platformio.org/en/latest/frameworks/espidf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom upload commands

## Simple: upload_command
`upload_command` overrides the platform's upload command. It requires `upload_protocol = custom`;
you can pass the full command, or mix it with `upload_flags`. Build variables (project folders
and other runtime configuration) can be used; list them with `pio run --target envdump`. A
platform's default command typically looks like `some-flash-bin-tool $UPLOADERFLAGS $SOURCE`,
where `$SOURCE` is replaced by the built firmware binary.
```ini
[env:program_via_AVR_ISP]
platform = atmelavr
framework = arduino
board = uno
upload_protocol = custom
upload_flags =
    -C
    ${platformio.packages_dir}/tool-avrdude/avrdude.conf
    -p
    atmega328p
    -P
    $UPLOAD_PORT
    -b
    115200
    -c
    stk500v1
upload_command = avrdude $UPLOAD_FLAGS -U flash:w:$SOURCE:i
```
Another documented example uses a vendor tool shipped as a package:
```ini
[env:custom_st_flash]
platform = ststm32
framework = stm32cube
board = bluepill_f103c6
upload_protocol = custom
upload_command = ${platformio.packages_dir}/tool-stlink/st-flash write $SOURCE 0x8000000
```
Notes: `${platformio.packages_dir}` points to the packages directory. Each flag goes on its own
line in `upload_flags`. Default upload commands live in the platform's `builder/main.py`.

## Script: adjust the upload command
An extra script can modify the build variable the platform uses. The ESP-IDF page documents
appending a flag to the platform's command:
```python
# force_upload.py  (platformio.ini: extra_scripts = force_upload.py)
Import("env")
env.Append(UPLOADCMD=" ".join(["$UPLOADCMD", "--force"]))
```
For other behaviour (multi-step flows, signing), see build-system hooks: `env.AddPreAction` and
`env.AddPostAction` on the `upload` target, and custom targets. Signed-image tools such as
`imgtool` and `mcumgr` have their own documentation; check their current flags there before
wiring them in.

## Gotchas
- `upload_protocol = custom` is required for `upload_command`; otherwise the platform's uploader
  runs.
- A failing command should exit non-zero so `pio run -t upload` fails in CI.
- The tool must be on PATH or referenced via `${platformio.packages_dir}`.

## Verify
- [ ] `pio run -t upload -v` shows the custom command and fails when the tool fails.
- [ ] Device boots the uploaded image.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `upload_command`,
`upload_protocol`, `upload_flags` pages, scripting actions page and the ESP-IDF flash-encryption
example. Confirmed: the `custom` protocol requirement, `$UPLOADERFLAGS`, `$SOURCE`,
`$UPLOAD_PORT`, `$UPLOAD_FLAGS`, `${platformio.packages_dir}`, the avrdude and st-flash examples,
`env.Append(UPLOADCMD=...)`. Removed as unconfirmed: STM32CubeProgrammer, pyOCD, nrfjprog,
mcumgr and imgtool commands and flags, `env.Replace(UPLOADCMD=<python function>)`, the
`upload_to_cloud` source link that does not exist (the docs page there only links an example
repository) and the Windows quoting advice.
Method: documentation only; no commands were run.
