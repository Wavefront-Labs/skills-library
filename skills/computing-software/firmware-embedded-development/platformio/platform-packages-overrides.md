---
id: computing-software.firmware-embedded-development.platformio.platform-packages-overrides
name: platform-packages-overrides
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [platform-packages, toolchain-override, framework-version, pioarduino, custom-framework-fork, platform-version-pinning, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Swap toolchains and frameworks with platform_packages: replace platform packages by name using versions, Git URLs or local folders, pin the platform, and the pitfalls."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/platform_packages.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/platform.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# platform_packages overrides

A development platform pins specific packages (toolchain, framework, tools). `platform_packages`
configures custom packages per build environment and can override a platform's default packages
by using the same name. Specifications follow `pio pkg install` (see its package specifications).

## Examples (from the PlatformIO documentation)
```ini
[env:override_default_toolchain]
platform = atmelavr
platform_packages =
  ; use GCC AVR 5.0+
  toolchain-gccarmnoneeabi@>1.50000.0

[env:override_framework]
platform = espressif8266
platform_packages =
  ; use upstream Git version
  framework-arduinoespressif8266 @ https://github.com/esp8266/Arduino.git

[env:external_package]
platform = ststm32
platform_packages =
  ; latest openOCD from PlatformIO Package Registry
  tool-openocd
  ; source code of ST-Link
  tool-stlink-source @ https://github.com/texane/stlink.git
```
Package spec forms: `name`, `owner/name@version`, a semver requirement, a repository URL with
optional `#tag`, `#branch` or `#commit`, `[<name>=]file://<folder>` (a copy),
`[<name>=]symlink://<folder>`, or an archive URL. The package name must match the package the
platform declares: see `pio pkg list -e <env>` for the names in use. (The first example above is
as published in the docs; check the package name against your platform before copying it.)

## Platform pinning first
Pin the platform (`platform = platformio/espressif32@~6.1.0` style, or a git URL with a tag or
commit) before overriding packages. The docs strongly recommend pinning, and an unpinned
`platform` can change which package versions a build expects, conflicting with your override.
Examples of platform forms: `owner/name@^x.y.z` (recommended), `@~x.y.z` (bug fixes only),
`@x.y.z` (exact), a git URL, a git URL with `#branch` or `#commit`.

## When people use it
- Testing a framework bug fix from a Git branch before release.
- A newer or patched compiler or tool.
- Replacing a whole platform with a fork by using its repository URL as `platform`.

## Pitfalls
- Platform build scripts are written for specific framework versions; a very different framework
  version can fail with missing files or wrong flags. Prefer a matching platform release.
- Toolchain major upgrades change warnings and code size, and can affect precompiled libraries.
- Package names can differ between platform versions; check with `pio pkg list`.
- CI caches keyed only on the platform version will not see a changed `platform_packages` line;
  include `platformio.ini` in the cache key.

## Verify
- [ ] `pio pkg list -e <env>` shows the overridden versions or URLs.
- [ ] Clean build from an empty core directory succeeds in CI.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `platform_packages`,
`platform` and `pio pkg install` pages. Confirmed: override-by-name behaviour, the three example
configurations, specification forms and platform pinning forms and recommendation. Removed as
unconfirmed: the ESP32 framework Git tag and `toolchain-xtensa-esp32` version examples, the
`~/` path interpolation example, the pioarduino zip URL, GCC version remarks and the toolchain
rename example.
Method: documentation only; no commands were run.
