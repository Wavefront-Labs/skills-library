---
id: computing-software.firmware-embedded-development.platformio.scons-construction-environments
name: scons-construction-environments
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [construction-environment, scons, import-env, projenv, defaultenvironment, envdump, extra-scripts, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "PlatformIO SCons construction environments in extra scripts: env vs projenv vs DefaultEnvironment, PRE vs POST reach, envdump inspection, and key variables."
sources:
  - https://docs.platformio.org/en/latest/scripting/construction_environments.html
  - https://docs.platformio.org/en/latest/scripting/launch_types.html
  - https://scons.org/doc/production/HTML/scons-user/ch07.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Construction environments

PlatformIO builds with SCons. Each build step uses a **construction environment**: a dictionary of
variables (CPPDEFINES, CCFLAGS, LINKFLAGS, LIBS, paths) plus builder methods.

## Which env is which
```python
Import("env")              # the current "global" environment: platform, framework, libraries
Import("env", "projenv")   # projenv: only in POST scripts; used to compile your src/ files
```
- **PRE scripts** (`extra_scripts = pre:x.py`) run before the platform's main script: changes to
  `env` affect everything built afterwards (framework, libraries, project).
- **POST scripts** run after the PRE scripts and the platform's main script, when the environment is
  fully constructed; `projenv` is available and flags set on it apply to project sources.
- A library's `library.json` `extraScript` runs before that library builds; build actions can only be
  applied to the global construction environment there.

## Inspecting
```sh
pio run -e myenv -t envdump > env.txt     # every variable and value
pio run -e myenv -v                         # final compiler command lines
```
In a script: `print(env.Dump())`, `env.subst("$BUILD_DIR")`, `env.get("CPPDEFINES")`.

## Useful variables and helpers
- `$BUILD_DIR`, `$PIOENV`, `$PROGNAME`, `$PIOFRAMEWORK`, `$UPLOAD_PORT`.
- `env.GetProjectOption("custom_fw_version")` reads any `custom_*` option from platformio.ini.
- `env.BoardConfig().get("build.mcu")` reads the board manifest.
- `env.IsIntegrationDump()` and `COMMAND_LINE_TARGETS` let scripts skip heavy work during IDE
  indexing or for particular targets.

## Pattern: change only project sources
```python
Import("env", "projenv")
projenv.Append(CCFLAGS=["-Werror", "-Wconversion"])   # strict for your code, not vendor libs
```

## Gotchas
- Flags passed to the global environment in a PRE script also reach `projenv`; to affect every
  build step, use a PRE script or `build_flags`, not `projenv`.
- Scripts run during IDE "Rebuild IntelliSense" too; avoid slow network calls or file writes
  unless the target is a real build.

## Verify
- [ ] `envdump` confirms flags land in the intended environment.
- [ ] Strict warnings apply to `src/` only (vendor library builds unaffected).

## Checked
2026-11-01. Confirmed in the platformio-docs repo (scripting/launch_types.rst, construction_environments.rst,
manifests/library-json/fields/build/extrascript.rst, middlewares.rst): PRE and POST semantics, `projenv` only in POST,
`envdump`, `env.Dump()`, `GetProjectOption`, `BoardConfig`, `IsIntegrationDump`, `COMMAND_LINE_TARGETS`, the listed
variables. Removed the `DefaultEnvironment()` identity claim, library-clone claims, `$PROJECT_SRC_DIR`, `$SIZETOOL`,
`$CC`, `$OBJCOPY`, `$PIOPLATFORM`, `IsCleanTarget`, and the "POST is default" claim.
Method: documentation only; no commands were run.
