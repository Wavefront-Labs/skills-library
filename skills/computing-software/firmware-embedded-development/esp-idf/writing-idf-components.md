---
id: computing-software.firmware-embedded-development.esp-idf.writing-idf-components
name: writing-idf-components
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-py, idf-component, idf-component-register, requires, priv-requires, extra-component-dirs, component-kconfig, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Structure ESP-IDF code as components: idf_component_register, REQUIRES vs PRIV_REQUIRES, component Kconfig, EXTRA_COMPONENT_DIRS and linking prebuilt libraries."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/build-system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing ESP-IDF components

**Goal:** reusable modules with explicit dependencies, so builds are fast and a missing
include is a build error in the right place.

## Layout
```
project/
  CMakeLists.txt          # include($ENV{IDF_PATH}/tools/cmake/project.cmake) + project()
  main/                   # the "main" component
  components/
    sensor/
      CMakeLists.txt
      Kconfig             # optional: component config options shown in menuconfig
      include/sensor.h    # public headers
      sensor.c
      priv/sensor_regs.h
```
```cmake
# components/sensor/CMakeLists.txt
idf_component_register(
    SRCS "sensor.c"
    INCLUDE_DIRS "include"
    PRIV_INCLUDE_DIRS "priv"
    REQUIRES public_dep          # used in public headers
    PRIV_REQUIRES private_dep)   # used only in .c files
```

## REQUIRES vs PRIV_REQUIRES
- `REQUIRES`: dependency appears in your **public** headers; it propagates to anyone who
  requires you.
- `PRIV_REQUIRES`: used only in sources. Keeps the dependency graph small.
- The component named `main` is special: it automatically requires all other components in
  the build, so it needs no `REQUIRES`/`PRIV_REQUIRES`. Every other component must list its
  dependencies.
- `PRIV_INCLUDE_DIRS` are added to the include path of this component's own sources only.

## Component Kconfig
A `Kconfig` file next to `CMakeLists.txt` adds settings to the configuration menu for the
component; start from one of the Kconfig files shipped with ESP-IDF. Use `Kconfig.projbuild`
only for options that must appear at the top level of menuconfig; the guide prefers plain
`Kconfig`.

## Other placement
- Components outside `components/`: set `EXTRA_COMPONENT_DIRS` (relative or absolute paths)
  in the project `CMakeLists.txt` before `project()`.
- Prebuilt library: `add_prebuilt_library(target_name lib_path [REQUIRES ...] [PRIV_REQUIRES ...])`,
  where `lib_path` may be relative to the component directory; link it to the component
  target. It must be built for the same target and a matching configuration as the project.
- A component with the same name in a higher-precedence location overrides another (see
  `COMPONENT_SOURCE` in the guide): handy for patches, dangerous on upgrades; prefer
  upstream fixes.

## Verify
- [ ] `idf.py build` succeeds after removing a component from `REQUIRES` only if it truly
      wasn't used (catches over-declared deps).

## Checked
2026-10-31. Confirmed on the ESP-IDF Build System guide: `idf_component_register` arguments,
REQUIRES semantics, the special `main` component, component `Kconfig` and `Kconfig.projbuild`,
`EXTRA_COMPONENT_DIRS`, `add_prebuilt_library` signature and caveat, component override
precedence. Removed: the claim that IDF v5 stopped `main` depending on every component
(the guide says it requires all of them), the v5.3 driver split and component names, the
`idf.py size-components` check, and the `sdkconfig.h` usage example, none of which the guide
confirms.
Method: documentation only; no commands were run.
