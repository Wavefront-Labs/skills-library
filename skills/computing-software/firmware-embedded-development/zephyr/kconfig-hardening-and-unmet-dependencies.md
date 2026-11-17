---
id: computing-software.firmware-embedded-development.zephyr.kconfig-hardening-and-unmet-dependencies
name: kconfig-hardening-and-unmet-dependencies
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [kconfig, kconfig-hardening, hardenconfig, unmet-dependencies, assigned-but-got, menuconfig, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Fix Zephyr Kconfig 'assigned the value y but got n' warnings by tracing unmet dependencies, and audit a release config with the hardenconfig target and its profiles."
sources:
  - https://docs.zephyrproject.org/latest/build/kconfig/menuconfig.html
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html
  - https://docs.zephyrproject.org/latest/build/kconfig/tracing.html
  - https://docs.zephyrproject.org/latest/security/hardening-tool.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kconfig hardening and unmet dependencies

## The warning
```
warning: BT_NUS (defined at ...) was assigned the value 'y' but got the value 'n'.
Check these unsatisfied dependencies: BT_PERIPHERAL (=n), BT (=n).
```
An assignment to a symbol whose dependencies are not satisfied is ignored and only printed by
default (assignments to undefined symbols abort the build). Set
`-DKCONFIG_WARNING_AS_ERROR=y` (for example in CI) to make every Kconfig warning fatal, so a
`prj.conf` line that does not take effect stops the build instead of silently doing nothing.

## Tracing it
1. Read the "unsatisfied dependencies" list. Each `(=n)` symbol needs enabling, or is itself
   blocked further down.
2. `west build -t menuconfig`, press `/`, search the symbol (show-all mode turns on if it is
   hidden), then `?` on it: shows direct dependencies, defaults, which symbols currently
   y-select or y-imply it, and where it is defined.
3. Common causes:
   - Missing devicetree node: `DT_HAS_<COMPAT>_ENABLED` is n because no node with that
     compatible is `status = "okay"` for this board. Fix the overlay, not Kconfig.
   - Symbol has no prompt (invisible): assignments in `.conf` files have no effect on it; enable
     the thing that selects it, or set its default in the board's `Kconfig.defconfig`.
   - Feature not supported by the board/SoC (for example `FPU` depends on `HAS_FPU`).
4. `build/zephyr/.config` is the final merged result. `west build -t traceconfig` writes a file in
   the build directory showing how each symbol got its value; run it on a pristine build because
   an existing `.config` pins all settings.

## Hardening audit
```bash
west build -b <board> app -t hardenconfig
```
The hardening tool compares the build's Kconfig options with the hardening database (curated by
the Zephyr Security Working Group) and prints a table with Name, Current, Recommended, Check
result and Rationale. Options not applicable to the target (for example MPU protections without an
MPU, or symbols with no visible prompt) are not reported. It also flags enabled options that
select `EXPERIMENTAL`, `DEPRECATED` or `NOT_SECURE`.

Controls (CMake variables after `--`, or environment variables of the same name):

| Variable | Effect |
|---|---|
| `HARDENCONFIG_PROFILE` | Profile to check: `base` or `strict` (default `strict`; `strict` also removes debug, tracing and shell features) |
| `HARDENCONFIG_SHOW_ALL` | Also list passing and non-applicable options |
| `HARDENCONFIG_STRICT` | Exit non-zero if any check fails (CI gate) |
| `HARDENCONFIG_JSON` | Also write results as JSON to this path |
| `HARDENCONFIG_EXTRA_SOURCES` | Semicolon-separated extra hardening database files |

Rules live in `scripts/kconfig/hardening.yaml` and per-subsystem `hardening.yaml` fragments.
Not every recommendation fits a product; go row by row and record why each mismatch is accepted
(for example check against `base` if you keep logging or shell in production).

## Release config hygiene
- Keep a release fragment (`-DEXTRA_CONF_FILE=prj_release.conf`) that turns off shell and debug
  features.
- Run `hardenconfig` with `HARDENCONFIG_STRICT` in CI on the release build and keep an approved
  baseline of accepted mismatches.

## Verify
- [ ] Release build is free of Kconfig warnings (or built with `KCONFIG_WARNING_AS_ERROR=y`) and `hardenconfig` output matches the approved baseline.
- [ ] Every `prj.conf` line takes effect (`grep` it in `build/zephyr/.config`).
- [ ] No test or debug-only symbols in the release `.config`.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the assigned-but-got warning text and that it is not fatal by default (scripts/kconfig/kconfig.py and the Kconfig setting page, KCONFIG_WARNING_AS_ERROR), the menuconfig keys, traceconfig, and the hardening tool page (profiles base and strict, HARDENCONFIG_* variables, hardening.yaml database). Wrong in the draft: the claim that these warnings abort the build by default, the hardened.csv database (now hardening.yaml), and unconfirmed symbol lists, which were removed.
Method: documentation only; no commands were run.
