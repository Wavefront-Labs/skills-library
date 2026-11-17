---
id: computing-software.firmware-embedded-development.platformio.build-middlewares
name: build-middlewares
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [extra-scripts, build-middleware, addbuildmiddleware, per-file-flags, exclude-file, replace-node, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use PlatformIO build middlewares (AddBuildMiddleware) to change flags for specific files, exclude or replace sources from frameworks, without forking packages."
sources:
  - https://docs.platformio.org/en/latest/scripting/middlewares.html
  - https://docs.platformio.org/en/latest/scripting/launch_types.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PlatformIO build middlewares

**Goal:** per-file control over how framework, library and project sources compile: different
flags for one file, dropping a framework file, or swapping in a patched copy.

## API
```python
Import("env")

def middleware(env, node):
    # node: SCons File node for one source about to be compiled
    # return the node unchanged, a new node built with custom variables, or None to skip it
    return node

env.AddBuildMiddleware(middleware, "*/path/pattern*.c")   # pattern optional
```
`pattern` is a Unix shell-style wildcard (fnmatch) matched against the node path; if it is omitted
the callback runs for every file node added to the build. Middlewares run in order of
registration. If one returns `None` (ignores the node), the later middlewares in the chain are
skipped automatically. A middleware can only be added from a `pre:` extra script.

## Recipes
**Per-file macros and flags** (pass SCons variables as keyword arguments to `env.Object()`; run
`pio run -t envdump` to list the variables):
```python
def extra_http_configuration(env, node):
    if "http" not in node.name:      # node.name, node.get_path(), node.get_abspath()
        return node
    return env.Object(
        node,
        CPPDEFINES=env["CPPDEFINES"] + [("HTTP_HOST", "device.local"), ("HTTP_PORT", 8080)],
        CCFLAGS=env["CCFLAGS"] + ["-fno-builtin-printf"],
    )

env.AddBuildMiddleware(extra_http_configuration)
```

**Exclude sources** (for example all assembly files):
```python
env.AddBuildMiddleware(lambda env, node: None, "*.S")
```

**Replace a framework file with a patched copy:**
```python
def replace_node_with_another(env, node):
    return env.File("path/to/patched/RtosTimer.cpp")

env.AddBuildMiddleware(replace_node_with_another, "framework-mbed/rtos/RtosTimer.cpp")
```
Note the upstream version in a comment: a framework update can make the patch stale silently.

## Gotchas
- Excluding a file that something else needs gives link errors, which is the point: read them.
- Middlewares are invisible in `platformio.ini`; leave a comment there pointing to the script.

## Verify
- [ ] `pio run -v` shows the modified flags on exactly the targeted files.
- [ ] A clean build after a framework update still applies (pattern still matches).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19), scripting/middlewares page.
Confirmed: the `env.AddBuildMiddleware(callback, pattern)` signature, fnmatch pattern semantics,
optional pattern, registration order, None-stops-the-chain rule, pre-script-only rule, the
`env.Object(node, VAR=...)` and `env.File(...)` forms, `node.name`/`get_path()`/`get_abspath()`.
Removed as unconfirmed: the -O3 and -w recipes and the GCC flag-order remark, the library
directory pattern, and the Windows backslash remark.
Method: documentation only; no commands were run.
