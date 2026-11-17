---
id: computing-software.firmware-embedded-development.platformio.pio-pkg-commands
name: pio-pkg-commands
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-pkg, pkg-install, pkg-update, pkg-outdated, pkg-list, pkg-search, package-management, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Manage PlatformIO packages with pio pkg: project vs global installs, list, outdated, update, uninstall, registry search, and replacing deprecated pio lib/platform commands."
sources:
  - https://docs.platformio.org/en/latest/core/userguide/pkg/index.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_install.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_search.html
  - https://docs.platformio.org/en/latest/core/migration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pio pkg commands

PlatformIO Core 6 unifies libraries, platforms and tools under `pio pkg`. The migration guide
marks `pio lib`, `pio platform` and `pio update` as deprecated in favour of `pio pkg`, and advises
against global libraries.

## Install
```sh
pio pkg install                                         # install what platformio.ini declares
pio pkg install -e esp32 -l "bblanchon/ArduinoJson@^6.19.2"   # custom library (saved to the project)
pio pkg install -p "platformio/atmelavr"                # development platform
pio pkg install -t "platformio/tool-openocd"            # tool
pio pkg install -g -t "platformio/tool-openocd"         # global storage
pio pkg install --no-save -l "owner/Lib"                # do not save to platformio.ini
```
With no `--library`, `--platform` or `--tool`, install covers: library dependencies from
`lib_deps`, the development platform and its dependencies, and tools from `platform_packages`.
Other options: `-d/--project-dir`, `--skip-dependencies` (ignore the package manifest's
dependencies), `--storage-dir`, `-f/--force`, `-s/--silent`. Global installs go to the platforms,
packages and global-library directories and the docs do not recommend global libraries; declare
`lib_deps` per project instead. Specs: `owner/name@version`, a requirement such as `@^6.19.2`,
a git URL, `file://` or `symlink://` folder, archive.

## Inspect and update
```sh
pio pkg list                         # packages per environment
pio pkg list --only-libraries -e esp32   # also --only-platforms, --only-tools, -g for global
pio pkg outdated                     # installed, wanted (by semver) and latest versions
pio pkg update                       # update project dependencies
pio pkg update -l "bblanchon/ArduinoJson"
pio pkg uninstall -l "owner/Lib"     # --no-save keeps platformio.ini unchanged
pio pkg search "header:Adafruit_Sensor.h"
pio pkg show bblanchon/ArduinoJson   # -t/--type resolves a name conflict
pio pkg exec -- openocd --help       # run a tool from an installed package
pio pkg exec -p tool-jlink -- JLinkGDBServer ...
```
`pio pkg search` takes full-text words or qualifiers: `type:`, `tier:`, `name:`, `keyword:`,
`category:`, `owner:`, `author:`, `framework:`, `platform:`, `header:`, `dependent:`,
`dependency:`; options `-p/--page` and `-s/--sort`. `pio pkg exec` also accepts
`--call '<cmd> [args]'`.

## Where things live
- Project libraries are installed to the `libdeps` directory (default `<workspace>/libdeps`).
- Platforms, tools and global libraries live under the core directory (default `~/.platformio`
  on Unix, `%HOMEPATH%\.platformio` on Windows; override with `core_dir` or
  `PLATFORMIO_CORE_DIR`).

## Reproducibility
- Use exact versions in release branches; `^` ranges are what the docs recommend for general
  dependencies.
- `pio pkg outdated` in a scheduled CI job reports drift without changing builds.
- `pio pkg pack` and `pio pkg publish` handle your own packages (see publishing skill).

## Verify
- [ ] `pio pkg list` output stored with release builds.
- [ ] Fresh CI runner installs identical versions (compare list output).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `pio pkg` command pages,
migration guide, `libdeps_dir` and `core_dir`. Confirmed: subcommands and options above, search
qualifiers, deprecation of `pio lib`, `pio platform`, `pio update`, storage locations and
defaults. Removed as unconfirmed: pinned example versions (`@7.2.0`, `@6.9.0`), CI cache advice,
"uninstall removes from lib_deps" (only `--no-save` is documented, implying it), and the
`~/.platformio/platforms` layout detail.
Method: documentation only; no commands were run.
