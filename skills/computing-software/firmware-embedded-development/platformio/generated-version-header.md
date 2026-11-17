---
id: computing-software.firmware-embedded-development.platformio.generated-version-header
name: generated-version-header
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [build-version-header, git-describe, firmware-version, version-h, pre-script, reproducible-version, platformio, firmware-embedded-development]
level: practitioner
status: draft
description: "Embed version info in PlatformIO firmware: a pre script generating version.h from git describe, only rewriting on change, CI overrides, and reading it at runtime."
sources:
  - https://docs.platformio.org/en/latest/scripting/actions.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_flags.html#built-in-variables
  - https://git-scm.com/docs/git-describe
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generated version headers

## Pre script
```python
# scripts/version.py   (extra_scripts = pre:scripts/version.py)
Import("env")
import os, subprocess, datetime

def git(*args):
    try:
        return subprocess.check_output(["git", *args], cwd=env.subst("$PROJECT_DIR"),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""

ver = os.environ.get("FW_VERSION") or git("describe", "--tags", "--always", "--dirty") or "0.0.0-unknown"
sha = git("rev-parse", "--short=10", "HEAD") or "nogit"
content = f"""#pragma once
#define FW_VERSION "{ver}"
#define FW_GIT_SHA "{sha}"
#define FW_ENV "{env['PIOENV']}"
"""
path = os.path.join(env.subst("$PROJECT_DIR"), "include", "version_gen.h")
old = open(path).read() if os.path.exists(path) else ""
if old != content:                       # rewrite only on change: avoids full rebuilds
    with open(path, "w") as f:
        f.write(content)
```
Add `include/version_gen.h` to `.gitignore`.

## Use
```c
#include "version_gen.h"
printf("fw %s (%s) env %s\n", FW_VERSION, FW_GIT_SHA, FW_ENV);
```
Also put the version in BLE DIS, MCUboot image header (`imgtool --version`), ESP `esp_app_desc`
(via `PROJECT_VER` for ESP-IDF framework), and log/telemetry.

## Choices
- `git describe --tags --dirty` gives `v1.4.2-3-gabc1234-dirty`: unique per commit and flags local
  changes. CI release jobs set `FW_VERSION=1.4.2` explicitly from the tag.
- Avoid build timestamps in the header: they change every build, break reproducibility and force
  recompiles. If needed, add the timestamp only in release CI.
- A simpler static alternative: `build_flags = !python scripts/print_version_flags.py` (PIO runs the
  command and uses its output as flags; `!` prefix). Changing flags recompiles everything, so the
  header approach is lighter for big projects.

## Gotchas
- Shallow CI clones have no tags: `git describe` falls back to the sha; fetch tags
  (`fetch-depth: 0` in actions/checkout).
- The script runs during IDE IntelliSense rebuilds too; it is cheap, keep it that way.
- Version string length matters on small targets if stored repeatedly; keep it once in flash.

## Verify
- [ ] Two builds of the same commit produce identical binaries (no timestamp drift).
- [ ] Release artefact reports the tag version at boot.
