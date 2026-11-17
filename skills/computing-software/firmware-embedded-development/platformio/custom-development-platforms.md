---
id: computing-software.firmware-embedded-development.platformio.custom-development-platforms
name: custom-development-platforms
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-boards, custom-platform, platform-json, platform-py, scons-builder, platform-fork, platformio, firmware-embedded-development]
level: sme
status: docs-checked
description: "Create or fork a PlatformIO development platform (platform.json, platform.py, SCons builder, boards) to support a new MCU, toolchain or framework version, and pin it in projects."
sources:
  - https://docs.platformio.org/en/latest/platforms/creating_platform.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/platform.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_install.html
  - https://github.com/platformio/platform-atmelavr/blob/develop/platform.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom development platforms

A **platform** tells PlatformIO which toolchain, frameworks, upload tools and boards exist for
a chip family. You need your own when the official one lacks your MCU, lags behind a framework
release, or you must pin patched toolchains.

## Fork before you write
Most needs are met by forking an official platform (for example `platformio/platform-ststm32` or
`platform-espressif32`) and changing a few files. The official platform repositories are the
documented best examples: look at their `builder` folder for main and framework scripts.

## Anatomy
```
platform-acme/
├── platform.json        # manifest: name, version, frameworks, packages
├── platform.py          # optional Python hooks (see the official platforms)
├── builder/
│   ├── main.py          # SCons: compiler flags, link, objcopy, upload targets
│   └── frameworks/      # per-framework build scripts
└── boards/
    └── acme_board.json  # board definitions (MCU, f_cpu, flash/RAM, upload/debug tools)
```
`platform.json` (excerpt, following the documented format):
```json
{
  "name": "acme",
  "title": "ACME MCUs",
  "description": "ACME development platform",
  "version": "1.0.0",
  "frameworks": { "acme-sdk": { "package": "framework-acme-sdk", "script": "builder/frameworks/acme_sdk.py" } },
  "packages": {
    "toolchain-gccarmnoneeabi": { "type": "toolchain", "owner": "platformio", "version": ">=1.40803.0,<1.40805.0" },
    "framework-acme-sdk": { "type": "framework", "optional": true, "version": "~1.10607.0" },
    "tool-direct-vcs-url": { "type": "uploader", "optional": true, "version": "https://github.com/user/repo.git" }
  }
}
```
Package `type` values seen in the docs example are `toolchain`, `framework` and `uploader`;
`optional` packages are installed only when a project needs them; a package `version` can be a
semver range or a VCS URL.

`platform.py` subclasses `PlatformBase` (the official platforms import it with
`from platformio.public import PlatformBase`) and overrides
`configure_default_packages(self, variables, targets)`, where `variables.get("pioframework", [])`
lists the frameworks selected by the project. Copy from an official platform rather than writing it
from scratch.

`builder/main.py` is a SCons script. The documented template uses
`env = DefaultEnvironment()`, `env.Replace(CC=..., UPLOADER=..., UPLOADCMD="$UPLOADER $SOURCES")`,
`env.Append(...)` for flags and `BUILDERS`, `target_elf = env.BuildProgram()`, an `ElfToBin`
builder, and `upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")` followed by
`AlwaysBuild(upload)`.

## Using it
```ini
[env:acme]
platform = https://github.com/acme/platform-acme.git#v1.0.0   ; git URL with branch, tag or commit
; platform = file:///local/path/to/platform-acme               ; local folder
board = acme_board
framework = acme-sdk
```
`pio pkg install -p <specification>` installs a platform; pinning a version (or a git tag/commit)
makes builds repeatable. Boards can also be added without a custom platform by putting JSON files
in the project's `boards` directory (see custom-board-definitions-and-partition-tables), which is
all most projects need.

## Maintenance
- Pin every package version in `platform.json`.
- Track upstream: merge new official releases into the fork periodically.
- Custom packages can be uploaded to the PlatformIO Registry with `pio pkg publish`
  (`--type` sets the package type) or kept in a private git repository.

## Verify
- [ ] Fresh machine: `pio run -e acme` installs the platform and packages from pins and builds.
- [ ] Upload and debug targets work for the custom board.
- [ ] Platform version or tag recorded in each product's `platformio.ini`.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19) and the platform-atmelavr and
platform-espressif32 `platform.py` files. Confirmed: the `platform.json` manifest shape, the
`main.py` template, platform specification forms (git URL with `#ref`, `file://`),
`pio pkg install -p`, `pio pkg publish --type`, `PlatformBase` import and
`configure_default_packages` hook with `pioframework`. Removed as unconfirmed: the pioarduino
fork reference, specific toolchain/OpenOCD version numbers, `pio pkg publish --type platform` as a
literal command, the "`~` ranges can pull new builds" remark and the `env.ElfToBin` claim as an
API.
Method: documentation only; no commands were run.
