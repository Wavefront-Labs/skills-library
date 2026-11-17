---
id: computing-software.firmware-embedded-development.platformio.extra-configs-and-sysenv
name: extra-configs-and-sysenv
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platformio-ini, extra-configs, sysenv, interpolation, secrets-management, build-flags, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Split platformio.ini with extra_configs, inject secrets and CI values with ${sysenv.VAR}, and use value interpolation so per-developer settings stay out of git."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/generic/extra_configs.html
  - https://docs.platformio.org/en/latest/projectconf/interpolation.html
  - https://docs.platformio.org/en/latest/envvars.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_flags.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extra_configs and sysenv

## Splitting the config
`extra_configs` takes a single path or a list of paths to extra configuration files (any file
name) with the same format and rules as `platformio.ini`. Unix shell-style wildcards (`*`, `?`,
`[seq]`, `[!seq]`) are allowed. If a group and option pair is declared in an extra file and was
declared in the base file, the extra file's value overwrites it.
```ini
; platformio.ini
[platformio]
extra_configs =
    envs/*.ini            ; one file per board family
    secrets.ini           ; keep out of git, see below

[env]
framework = arduino
build_flags = -D BASE_FLAG
```
```ini
; envs/esp32.ini
[env:esp32-dev]
platform = espressif32
board = esp32dev
build_flags = ${env.build_flags} -D BOARD_DEV
```
A custom section (here `[secrets]`) is injected into an environment via `${secrets.option}`. The
section names `platformio` and `env` are reserved; `extra` and `custom` are suggested names.

## Secrets and per-machine settings
```ini
; secrets.ini (in .gitignore), with a committed secrets.ini.example
[secrets]
wifi_ssid = homelab
upload_port = /dev/ttyUSB1
```
```ini
[env:esp32-dev]
build_flags = ${env.build_flags} -D WIFI_SSID_ID=1
upload_port = ${secrets.upload_port}
```
Credentials compiled into firmware are extractable from the binary: fine for a dev Wi-Fi, not for
production keys (provision those at manufacture instead).

## Environment variables: ${sysenv.NAME}
`${sysenv.<name>}` embeds an operating-system environment variable (the docs example is
`${sysenv.HOME}`). The docs recommend keeping sensitive data in environment variables and warn
that on Unix, special characters (`$`, `&`, `~` and others) in a variable used for preprocessor
directives must be escaped when it is exported. Use interpolation rather than the
`PLATFORMIO_BUILD_FLAGS` variable when flags contain such characters.

PlatformIO also reads `PLATFORMIO_*` environment variables that set the matching option, for
example `PLATFORMIO_BUILD_FLAGS` (`build_flags`), `PLATFORMIO_UPLOAD_PORT` (`upload_port`) and
`PLATFORMIO_UPLOAD_FLAGS`.

## Interpolation reference
- `${section.option}`: value from another section (`${env.build_flags}`, `${extra.lib_deps}`).
- `${this.option}`: value from the current section (`${this.board}`).
- `${this.__env__}`: current environment name (section must start with `env:`).
- `${platformio.<option>}`: for example `${platformio.packages_dir}`, `${platformio.build_dir}`.
- `${sysenv.NAME}`: operating-system environment variable.
- Built-in `${PROJECT_DIR}`, `${PROJECT_HASH}` and `${UNIX_TIME}`.
- Interpolation spans multiple levels, allows several per value, and applies only to option
  values.

## Quoting string macros
To turn a macro argument into a C string, wrap the value in double quotes and escape them; the
documented form encloses the whole flag in single quotes to prevent shell evaluation:
```ini
build_flags =
    '-D MYSTRING="Text is \\"Quoted\\""'
```
Check the result with `pio project config` (parsed configuration) or a verbose build.

## Verify
- [ ] A fresh clone without `secrets.ini` fails with a clear message or builds with defaults.
- [ ] `pio project config` shows the merged result you expect for each env.
- [ ] CI injects version information through environment variables and the binary reports it.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `extra_configs`,
interpolation, `envvars` and `build_flags` pages. Confirmed: extra_configs wildcard rules and
override rule, reserved sections, the interpolation syntax table, `${sysenv.<name>}`, the Unix
escaping warning, `PLATFORMIO_BUILD_FLAGS` and `PLATFORMIO_UPLOAD_PORT`, `\\"` quoting form.
Removed as unconfirmed: file processing order, "an undefined sysenv variable expands to an empty
string", the `static_assert` advice, the pinned `espressif32@6.9.0` version, and that the
`PLATFORMIO_*` variables "add to" options (the docs only say they set the option).
Method: documentation only; no commands were run.
