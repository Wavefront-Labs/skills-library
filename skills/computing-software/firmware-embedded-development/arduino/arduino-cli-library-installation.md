---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-library-installation
name: arduino-cli-library-installation
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-lib-install, lib-install, lib-search, git-url-install, zip-install, library-priority, multiple-libraries-found, arduino-cli, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Install and manage Arduino libraries with arduino-cli: search, pinned versions, git/zip installs, upgrades, deps, and resolving 'Multiple libraries were found' priority conflicts."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/sketch-build-process.md
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/lib/install.go
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/lib/search.go
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/lib/check_deps.go
  - https://github.com/arduino/arduino-cli/blob/master/docs/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library installation with arduino-cli

## Everyday commands
```sh
arduino-cli lib update-index
arduino-cli lib search bme280 --names       # names only; search covers name, sentence, paragraph
arduino-cli lib install "<name>@<version>"                # pin versions in CI
arduino-cli lib install "<name>" --no-deps                # skip dependency install
arduino-cli lib list --all                                # includes built-in (platform and IDE) libraries
arduino-cli lib upgrade                                    # all; or name
arduino-cli lib uninstall "Adafruit BME280 Library"
arduino-cli lib deps "Adafruit BME280 Library"             # show dependency tree
```
Dependencies declared in the library's `library.properties` (`depends=`) install automatically
unless `--no-deps`.

## Non-registry sources
Requires `library.enable_unsafe_install: true` (or `ARDUINO_LIBRARY_ENABLE_UNSAFE_INSTALL=true`):
```sh
arduino-cli lib install --git-url https://github.com/me/MyLib.git#<ref>
arduino-cli lib install --zip-path ./MyLib.zip
```
Libraries land in the `libraries` folder of the user directory (sketchbook). Alternatively compile with `--library ./path/to/lib`
or `--libraries ./libs` to use libraries from the repo without installing.

## Library resolution and "Multiple libraries were found"
When several libraries contain the file named by an `#include`, the builder applies these rules in order until one decides:
1. A library given with `compile --library` wins.
2. An architecture-compatible library beats an incompatible one.
3. A library whose library name and folder name both match the include wins.
4. Better library-name or folder-name match (exact, then `-main`/`-master` suffix, prefix, suffix, contains).
5. A library optimized for the architecture beats one that is only compatible (`architectures=*`).
6. Location priority: `--libraries` paths, then the user directory `libraries`, then platform-bundled, then referenced-platform-bundled, then IDE built-in (`directories.builtin.libraries`).
7. Closest folder-name match, then alphanumeric folder order.
Use verbose compile output to see which library was chosen. Fix conflicts by removing duplicates,
renaming the folder to match the header, or passing `--library` explicitly.

## Reproducibility
- Pin every library version in CI or use a `sketch.yaml` profile (`libraries:` with versions) and
  `arduino-cli compile --profile`.
- `arduino-cli compile --only-compilation-database` gives `compile_commands.json` for IDE tooling.

## Gotchas
- `lib search` text matching is broad; use `--names` and exact names in quotes for install.
- Two libraries providing the same header are resolved by the rules above; check which one was used rather than assuming.

## Verify
- [ ] Verbose CI logs show exactly the pinned library versions.
- [ ] No unintended duplicate libraries are resolved in a clean build.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on master (commit 2026-10-22).

Confirmed: `lib install` takes `NAME[@VERSION]`, flags `--no-deps`, `--no-overwrite`, `--git-url` (with `#<ref>`), `--zip-path`, `--install-in-builtin-dir`; `lib search --names`; `lib list --all`; `lib deps`; `library.enable_unsafe_install` gates git and zip installs; the library-resolution rules and location priority from the sketch build process page; `compile --library`, `--libraries`, `--only-compilation-database`. Fixed: the priority list was incomplete and misordered. Removed unconfirmed claims: pinned example versions, `lib list --fqbn`, the "Used / Not used" output lines and the "Multiple libraries" message text.

Method: documentation only; no commands were run.
