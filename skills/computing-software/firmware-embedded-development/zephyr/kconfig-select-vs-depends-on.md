---
id: computing-software.firmware-embedded-development.zephyr.kconfig-select-vs-depends-on
name: kconfig-select-vs-depends-on
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [kconfig-select, kconfig-depends-on, kconfig-imply, reverse-dependency, unmet-direct-dependencies, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose between select, imply and depends on in Zephyr Kconfig: reverse-dependency pitfalls, unmet-dependency warnings, dependency loops, and Zephyr's guidelines."
sources:
  - https://docs.zephyrproject.org/latest/build/kconfig/tips.html
  - https://docs.zephyrproject.org/latest/build/kconfig/menuconfig.html
  - https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# select vs depends on

## Semantics
| Keyword | Meaning | Respects target's dependencies |
|---|---|---|
| `depends on X` | this symbol is invisible/n unless X | n/a |
| `select X` | force X to y when this is y | **No** |
| `imply X` | default X to y when this is y; user can still set X=n | Yes |

## The select hazard
```kconfig
config MY_DRIVER
    bool "My driver"
    select FOO_LIB              # FOO_LIB depends on GPIO
```
If `GPIO=n`, `select` still forces `FOO_LIB=y` and Kconfig warns:
```
warning: FOO_LIB (defined at ...) has direct dependencies GPIO with value n,
but is currently being y-selected by the following symbols:
```
`select` is safe only for symbols with no dependencies of their own, or whose dependencies the
selector also has. A later change to the selected symbol's dependencies then needs every
(direct or indirect) selector updated, and chains of symbols selecting each other should be
avoided.

## Zephyr guidelines (Kconfig tips page)
- Avoid selecting symbols with prompts or dependencies; prefer `depends on`. If `depends on`
  makes configuration files bloated, add a Kconfig default for the most common value. Rare
  exceptions: two simple symbols defined next to each other in the same `if`.
- Select simple helper symbols (no prompt, no dependencies) freely, for example a
  `CPU_HAS_FPU`-style capability symbol that a SoC selects.
- Exception: buses such as I2C and SPI (and MFD). Drivers on these buses use `select` so the
  bus driver is enabled automatically when a device on the bus is enabled in devicetree
  (`select SPI` in an SPI ADC driver).
- `imply` is like `select` but respects dependencies and does not force a value: a SoC can
  `imply USB_KEYBOARD` to turn it on by default while the user can still turn it off.

## Dependency loops
Kconfig stops with a `Dependency loop` error that prints each symbol's definition in the loop
and any select- or imply-related dependencies. Break the loop by turning one edge into a
different relationship (often `select` into `depends on`) or by restructuring the symbols.

## Debugging why a symbol is y
In `menuconfig`, `?` on the symbol lists the symbols currently y-selecting and y-implying it,
plus its direct dependencies. `west build -t traceconfig` (on a pristine build) writes a file
that details how each symbol got its value.

## Visibility
`depends on` also hides the prompt. If a user can't find an option in menuconfig, its dependency
is n; search with `/` (which turns on show-all mode for hidden symbols; `A` toggles it off).

## Verify
- [ ] No "y-selected" warnings in the CMake/Kconfig output.
- [ ] Every `select` target is promptless or has no unmet dependencies (bus drivers excepted).
- [ ] User-visible features use `depends on`.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the select recommendations, bus exception and imply semantics (Kconfig tips page), the y-selected warning text and Dependency loop error (scripts/kconfig/kconfiglib.py), and the symbol-info wording and show-all mode (menuconfig docs and script). Removed the I2C_BITBANG example (replaced with a neutral symbol), the invented recursive-dependency message text and the Selected by / Implied by labels.
Method: documentation only; no commands were run.
