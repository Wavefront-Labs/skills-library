---
id: computing-software.firmware-embedded-development.platformio.modifying-build-flags-programmatically
name: modifying-build-flags-programmatically
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [env-append, env-replace, cppdefines, ccflags, linkflags, buildsrcfilter, extra-scripts, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Change build flags from PlatformIO extra scripts: env.Append/Prepend/Replace on CPPDEFINES, CCFLAGS, LINKFLAGS, LIBS, removing flags, and per-file flags via middleware."
sources:
  - https://docs.platformio.org/en/latest/scripting/examples/extra_linker_flags.html
  - https://docs.platformio.org/en/latest/scripting/construction_environments.html
  - https://scons.org/doc/production/HTML/scons-man.html#lbAH
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modifying flags programmatically

`build_flags` in platformio.ini covers static cases. Use a script when flags depend on git state,
board config, environment variables or file lists.

## Append, prepend, replace
```python
# scripts/flags.py  (extra_scripts = pre:scripts/flags.py)
Import("env")
import os

env.Append(
    CPPDEFINES=[("FW_BUILD_ENV", env.StringifyMacro(env["PIOENV"])), "USE_LOGGING"],
    CCFLAGS=["-Wall", "-Wextra"],                 # C and C++
    CFLAGS=["-std=gnu11"],                        # C only
    CXXFLAGS=["-std=gnu++17", "-fno-exceptions"],# C++ only
    LINKFLAGS=["-Wl,--print-memory-usage", "-Wl,-Map,${BUILD_DIR}/firmware.map"],
    CPPPATH=["$PROJECT_DIR/generated"],
    LIBPATH=["$PROJECT_DIR/lib/bin"], LIBS=["acmedsp"],
)
env.Prepend(CPPPATH=["$PROJECT_DIR/overrides"])   # search before framework headers

if os.environ.get("CI"):
    env.Append(CPPDEFINES=["CI_BUILD"])
```
- `CPPDEFINES` tuples become `-DNAME=VALUE`; `env.StringifyMacro()` quotes strings correctly.
- `env.Replace(VAR=...)` replaces a variable entirely (e.g. `UPLOADCMD`).

## Removing flags
```python
for var in ("CCFLAGS", "CXXFLAGS", "LINKFLAGS"):
    env[var] = [f for f in env.get(var, []) if f not in ("-Os", "-std=gnu++11")]
```
Or `build_unflags` in the ini for static removal.

## Per-file flags with build middleware
```python
def strict(env, node):
    if "src/drivers/" in node.get_path():
        return env.Object(node, CCFLAGS=env["CCFLAGS"] + ["-Werror"])
    return node
env.AddBuildMiddleware(strict)               # or env.AddBuildMiddleware(fn, "*/drivers/*")
```
Middleware can also skip files (`return None`) or replace them.

## PRE vs POST
Flags for everything (framework + libraries + project): PRE script on `env`. Project sources only:
POST script on `projenv` (see construction environments).

## Gotchas
- Appending to `CCFLAGS` a flag that is C++-only (`-fno-rtti`) warns for C files; use `CXXFLAGS`.
- `-D` with spaces/quotes in `build_flags` is fragile; prefer `CPPDEFINES` in scripts.
- Verify with `pio run -v` (command lines) or `-t envdump`.

## Verify
- [ ] Verbose build shows the intended flags on the intended files only.
- [ ] Clean build reproduces identical flags in CI and locally.

## Checked
2026-11-01. Confirmed in the platformio-docs repo (scripting/middlewares.rst, construction_environments.rst,
launch_types.rst, projectconf build_flags.rst): `env.AddBuildMiddleware(callback, pattern)` including returning
`None` to skip a node and PRE-only registration, `projenv` for POST scripts, `env.StringifyMacro`, `PIOENV`,
`CPPDEFINES` and `$BUILD_DIR`, `pio run -t envdump`. Removed a garbled gotcha about duplicate appends.
Method: documentation only; no commands were run.
