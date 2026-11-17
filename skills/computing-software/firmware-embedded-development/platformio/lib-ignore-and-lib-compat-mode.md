---
id: computing-software.firmware-embedded-development.platformio.lib-ignore-and-lib-compat-mode
name: lib-ignore-and-lib-compat-mode
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [lib-ignore, lib-compat-mode, ldf, library-conflict, framework-bundled-libraries, platformio-ini, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Stop PlatformIO from building the wrong libraries: lib_ignore for bundled or conflicting libs, lib_compat_mode off/soft/strict, and reading the LDF dependency graph."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_ignore.html
  - https://docs.platformio.org/en/latest/librarymanager/ldf.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_compat_mode.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_ldf_mode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lib_ignore and lib_compat_mode

## Symptoms that call for these
- Link errors "multiple definition of" because two libraries provide the same code.
- A library that does not support your platform gets compiled because a header name matched.
- The build pulls in a library you do not use because a header in a dependency matched.

## lib_ignore
Specifies libraries the Library Dependency Finder (LDF) should ignore. Use the library **name**,
not the folder name: the names appear between `<` and `>` in the "Dependency Graph" printed by the
build. Single-line (comma-separated) and multi-line forms are allowed:
```ini
[env:myenv]
lib_ignore = AsyncMqttClient, DNSServer
; or
lib_ignore =
    AsyncMqttClient
    ESP Async WebServer
```

## lib_compat_mode
If a library has a manifest (`library.json`, `library.properties` or `module.json`), the LDF
checks its compatibility with the build environment:
- `off`: no checks (the docs do not recommend it).
- `soft` (default): checks compatibility with the `framework` of the environment.
- `strict`: checks compatibility with both the `framework` and the `platform`.
Use `strict` to keep wrong-platform libraries out of multi-platform projects. Prefer fixing a
library's manifest over `off`.

## See what the LDF did
```sh
pio run -e myenv -v        # prints "Dependency Graph" (names between < >, with versions)
pio pkg list -e myenv      # resolved packages and libraries
```
The build prints a line like `LDF MODES: FINDER(chain+) COMPATIBILITY(soft)`. `lib_ldf_mode`
values: `chain` (default), `deep`, `chain+`, `deep+`, `off`. `chain` and `deep` do not evaluate
`#ifdef`/`#if` conditions, `chain+` and `deep+` do. `off` builds only libraries named in manifests
or `lib_deps`.

## Gotchas
- `lib_ignore` does not remove an `#include` from your code; including a header from an ignored
  library fails the build.
- Ignoring a library that a dependency needs breaks that dependency, often only at link time.
- LDF storage priority: project `lib` directory, project `libdeps` directory, global core `lib`
  directory, then libraries built into frameworks and SDKs.

## Verify
- [ ] Dependency graph lists exactly the intended libraries per env.
- [ ] No duplicate-symbol errors in a clean build.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `lib_ignore`,
`lib_compat_mode`, `lib_ldf_mode` and the LDF guide. Confirmed: name-not-folder rule and syntax,
compat mode values and default, LDF modes and default, conditional evaluation per mode, storage
priority. Removed as unconfirmed: the WiFi/SD/BluetoothSerial examples, "names are case
sensitive", "applies to framework-bundled libraries" as a separate rule, and the setting
`"platforms": "*"` tip. Corrected: `soft` checks only the framework (the draft described
architectures), and `strict` checks framework and platform.
Method: documentation only; no commands were run.
