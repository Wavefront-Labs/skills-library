---
id: computing-software.firmware-embedded-development.platformio.library-json-build-options
name: library-json-build-options
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [library-json-build, library-json, srcfilter, includedir, libarchive, extrascript, flags, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make a library build itself correctly under PlatformIO: library.json build fields (flags, srcFilter, includeDir, srcDir, libArchive, libLDFMode, extraScript) with examples."
sources:
  - https://docs.platformio.org/en/latest/manifests/library-json/fields/build/index.html
  - https://docs.platformio.org/en/latest/manifests/library-json/fields/build/extrascript.html
  - https://docs.platformio.org/en/latest/manifests/library-json/fields/build/flags.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_archive.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# library.json build options

A library's `library.json` `build` object (optional) holds advanced settings, options and flags
for the build system.

## Example
```json
{
  "name": "AcmeDsp",
  "version": "2.1.0",
  "frameworks": "*",
  "platforms": ["ststm32", "nordicnrf52", "espressif32"],
  "build": {
    "srcDir": ".",
    "srcFilter": "+<*> -<examples> -<test>",
    "includeDir": ".",
    "flags": ["-DACME_USE_FPU", "-I include", "-I drivers"],
    "unflags": "-std=gnu++11",
    "libArchive": false,
    "libLDFMode": "chain+",
    "libCompatMode": "strict",
    "extraScript": "extra_script.py"
  }
}
```

## Fields
- `srcDir` (default `src`): base path for library sources. `.` builds all sources in the library
  root and subfolders recursively.
- `includeDir` (default `include`): base path searched for headers. The LDF picks a library only
  when a project or dependent library includes a header located in `includeDir` or `srcDir`.
  Extra header paths go in `flags` with `-I`.
- `srcFilter`: string or array, paths relative to `srcDir`, same syntax as `build_src_filter`.
  Needed when examples and tests live inside the source tree.
- `flags` / `unflags`: extra build flags, and base flags set by the platform to remove. `-I` paths
  are relative to the directory holding `library.json`.
- `libArchive`: `true` by default (objects are archived into a `.a`); `false` links object files
  directly, which helps when you must override `weak` symbols defined in the framework or other
  libraries. The project-wide equivalent is `lib_archive = no`.
- `libLDFMode`, `libCompatMode`: per-library LDF mode and compatibility mode.
- `builder`: overrides the default `PlatformIOLibBuilder`; supported are `PlatformIOLibBuilder`,
  `ArduinoLibBuilder` and `MbedLibBuilder`.
- `extraScript`: a script launched before the build of the library. Documented capabilities: read
  `CPPDEFINES` and set private `CPPPATH` and `SRC_FILTER` for this library; pass flags to other
  dependencies with `env.GetLibBuilders()`; use `projenv` for project `src` files and
  `DefaultEnvironment()` for the global environment (project sources and frameworks). Actions can
  only be attached to the global environment.

## Overriding from the project
The project cannot edit a dependency's `library.json`. Options: fork it, keep a modified copy in
the project `lib` folder, or use project-level equivalents such as `lib_ldf_mode`,
`lib_compat_mode` and `lib_archive`.

## Verify
- [ ] `pio run -v` shows the library compiled with its flags and only intended sources.
- [ ] Interrupt handlers defined in the library override the weak defaults (check the map file).
- [ ] `pio pkg pack` accepts the manifest (the docs name it as a validator).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `library.json` build field
pages, `lib_archive`. Confirmed: field names, types and defaults, relative path rules,
`libArchive` weak-symbol purpose, `builder` values, extraScript capabilities, validation via
`pio pkg pack`. Removed as unconfirmed: the srcFilter example with `arm/` paths, "defines here do
not reach the project's sources" (the docs show flags can be passed on explicitly), the
`BoardConfig().get("build.cpu")` and `LIBPATH` snippet and the claim that archives drop weak
overrides (only the documented purpose is kept).
Method: documentation only; no commands were run.
