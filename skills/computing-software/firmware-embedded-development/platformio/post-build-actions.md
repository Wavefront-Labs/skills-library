---
id: computing-software.firmware-embedded-development.platformio.post-build-actions
name: post-build-actions
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [extra-scripts, addpostaction, addpreaction, firmware-bin, objcopy, image-signing, merge-bin, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Hook PlatformIO build targets with AddPreAction/AddPostAction: build a hex from the ELF, act on upload, buildprog and specific files, and sign or post-process firmware."
sources:
  - https://docs.platformio.org/en/latest/scripting/actions.html
  - https://docs.platformio.org/en/latest/scripting/launch_types.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Post-build actions in PlatformIO

**Goal:** artefacts that are ready to ship (signed, checksummed, converted, copied) straight out
of `pio run`, so CI and developers produce identical files.

## Hooking a target
`env.AddPreAction(target, callback)` and `env.AddPostAction(target, callback)` (a single callback
or a list). `target` can be a target name passed with `pio run --target`, a built-in target name
(`buildprog`, `size`, `upload`, `program`, `buildfs`, `uploadfs`, `uploadfsota`) or the path of a
file PlatformIO processes (ELF, HEX, BIN, OBJ, ...). Actions can only be applied to the global
construction environment.
```python
# platformio.ini: extra_scripts = post:extra_script.py
Import("env")

def post_program_action(source, target, env):
    program_path = target[0].get_abspath()
    print("Program path", program_path)
    # Use case: sign a firmware, do any manipulations with ELF, etc
    # env.Execute(f"sign --elf {program_path}")

env.AddPostAction("$PROGPATH", post_program_action)

def before_upload(source, target, env):
    print("before_upload")
    env.Execute("node --version")

env.AddPreAction("upload", before_upload)
env.AddPostAction("upload", lambda *a, **k: print("after_upload"))
```
Documented target forms: `buildprog`, `$PROGPATH`, `$BUILD_DIR/${PROGNAME}.elf`,
`$BUILD_DIR/${PROGNAME}.hex`, `$BUILD_DIR/spiffs.bin` (for example to compress HTML before an
image is built) and `$BUILD_DIR/src/main.cpp.o`. A callback receives `(source, target, env)`.

## Recipe: custom HEX from ELF
```python
env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-O", "ihex", "-R", ".eeprom",
        "$BUILD_DIR/${PROGNAME}.elf", "$BUILD_DIR/${PROGNAME}.hex"
    ]), "Building $BUILD_DIR/${PROGNAME}.hex")
)
```
`env.VerboseAction(command, message)` runs a command string with SCons variables and prints the
message.

## Other uses
- Signing or checksumming: call your signing tool from the callback, using the tool's own
  documentation for its flags; write the result to a new file rather than modifying a tracked
  one in place.
- Copy artefacts to a `dist/<env>` folder with the version in the file name.
- The `$PROGNAME` can be changed in a pre script with `env.Replace(PROGNAME=...)`.

## Gotchas
- Attach actions from a `post:` script: the build environment is fully constructed there (the
  default launch type when no prefix is given).
- Actions hang on a node, so they do not run when that target is up to date; use a custom target
  with `always_build=True` for "always run" tasks (see custom targets).
- `AddPreAction("upload", ...)` is the hook for "check something before flashing".
- Hook the exact path the platform produces; `pio run -v` shows the paths in use.

## Verify
- [ ] Clean build produces every expected artefact.
- [ ] CI uploads exactly those artefacts (no manual post-processing outside PlatformIO).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): scripting actions and
launch types pages. Confirmed: function signatures, accepted target kinds and the built-in
target list, the example hooks and VerboseAction usage, post-script semantics, global-environment
restriction. Removed as unconfirmed: the CRC-append example, the `checkprogsize` alias, the
MCUboot `imgtool sign` and ESP32 `esptool merge_bin` recipes (check those tools' own current
documentation), the "node under a different path" claim as fact, and the claim about SCons
re-evaluating modified files.
Method: documentation only; no commands were run.
