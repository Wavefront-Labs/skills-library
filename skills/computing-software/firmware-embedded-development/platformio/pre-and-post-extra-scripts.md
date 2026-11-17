---
id: computing-software.firmware-embedded-development.platformio.pre-and-post-extra-scripts
name: pre-and-post-extra-scripts
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [extra-scripts, pre-script, post-script, scons, import-env, projenv, build-version-injection, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write PlatformIO extra_scripts that run before or after the platform's build script: inject version macros, tweak flags, and know which environment object to touch."
sources:
  - https://docs.platformio.org/en/latest/scripting/launch_types.html
  - https://docs.platformio.org/en/latest/scripting/construction_environments.html
  - https://docs.platformio.org/en/latest/scripting/actions.html
  - https://docs.platformio.org/en/latest/scripting/examples/custom_program_name.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PlatformIO pre and post extra scripts

**Goal:** customise the build with small Python (SCons) scripts instead of forking the platform
or hand-editing generated files.

## Declaring
```ini
[env:board]
extra_scripts =
    pre:scripts/version.py
    post:scripts/rename_firmware.py
    other_post_script.py        ; no prefix: treated as post:
```
- `pre:` runs before the platform's main build script: useful to pre-generate source files,
  patch existing ones, pass flags to the global build environment and add middlewares.
  `projenv` is not available.
- `post:` runs after the pre scripts and the main script: the environment is fully constructed
  (flags, platform targets, dependent libraries, `projenv`). Useful for actions, modifying default
  flags or extending the build workflow.
- Library `library.json` can also launch a script with `extraScript`.

## Environments inside the script
```python
Import("env")               # the global environment (DefaultEnvironment()) for ini scripts
Import("env", "projenv")    # post scripts only: projenv builds the project's src folder
```
- `DefaultEnvironment()` is used for platform and framework build scripts, actions, upload tools
  and the LDF.
- `projenv` is isolated for project sources; `build_src_flags` go to `projenv`, not to the global
  environment. Flags added to the global environment from a PRE script also affect `projenv`.
- In a library's `extraScript`, `Import("env")` refers to the library's isolated environment; use
  `env = DefaultEnvironment()` for the global one.

## Example: inject a version
```python
# scripts/version.py  (pre:)
import subprocess
Import("env")
try:
    ver = subprocess.check_output(["git", "describe", "--tags", "--always", "--dirty"],
                                  text=True).strip()
except Exception:
    ver = "unknown"
env.Append(CPPDEFINES=[("FW_VERSION", env.StringifyMacro(ver))])
```
`env.StringifyMacro()` is used in the docs for string-valued defines. A global define that changes
on every commit rebuilds everything that sees it.

## Useful env APIs (from the documented examples)
- `env.GetProjectOption("custom_option")` reads a `custom_*` key from `platformio.ini`.
- `env.Replace(PROGNAME="firmware_%s" % version)` renames the output firmware.
- `env.Execute("cmd")` runs a command now; `env.Dump()` prints the whole environment, handy for
  finding a variable's name.
- `env.Execute("$PYTHONEXE -m pip install pkg1 pkg2")` installs extra Python packages (the docs
  show a guarded form).

## Gotchas
- PlatformIO re-executes extra scripts in a service stage to collect integration data for IDE
  plugins. To run code only for build targets, start the script with:
  ```python
  Import("env")
  if env.IsIntegrationDump():
      Return()
  ```
- Keep scripts fast and free of side effects outside build actions.

## Verify
- [ ] `pio run -v` shows the injected define on project compile lines.
- [ ] A clean build and an incremental one both produce the expected version.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): launch types,
construction environments, actions and example pages. Confirmed: pre/post semantics and the
default prefix, `projenv` availability and flag propagation rules, library-script environment,
`IsIntegrationDump`, `StringifyMacro`, `GetProjectOption`, `PROGNAME`, `Execute` and `Dump`.
Removed as unconfirmed: `env.subst` guidance, the "write a generated version.c" advice, the
"pip import guard" wording beyond the documented form, and path-separator remarks.
Method: documentation only; no commands were run.
