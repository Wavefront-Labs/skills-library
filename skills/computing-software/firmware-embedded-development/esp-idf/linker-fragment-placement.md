---
id: computing-software.firmware-embedded-development.esp-idf.linker-fragment-placement
name: linker-fragment-placement
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-build, linker-fragment, ldgen, iram-placement, section-placement, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Control where ESP-IDF code and data land (IRAM, flash, RTC memory, noinit) using linker fragment .lf files and ldgen mappings instead of hand-edited linker scripts."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/linker-script-generation.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/memory-types.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/app.lf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linker fragments

ESP-IDF generates its linker script with `ldgen`. To move code you add a fragment file to the
component instead of editing `.ld` files.

## Register a fragment
```cmake
idf_component_register(SRCS "dsp.c" "isr.c"
                       INCLUDE_DIRS "."
                       LDFRAGMENTS "linker.lf")
```

## Put a whole object or single functions in IRAM
```
[mapping:my_dsp]
archive: libmy_dsp.a
entries:
    isr (noflash)                 # all code and read-only data of isr.o into IRAM/DRAM
    dsp:fir_filter (noflash)      # one symbol from dsp.c (object:symbol)
    dsp:debug_dump (default)      # explicit default placement
```
Built-in schemes from `esp_system/app.lf`: `noflash` places text in `iram0_text` and rodata in `dram0_data`;
`noflash_text` moves only text and `noflash_data` only rodata; `rtc` places text, data, rodata and bss in RTC
memory (`rtc_text`, `rtc_data`, `rtc_bss`). `archive` is the library name as built (`libxxx.a`, for a component
usually `lib<component-name>.a`). Symbol-granularity entries have documented limitations; the docs recommend
grouping code and data into source files and using object granularity where possible.

## Conditional on Kconfig
```
[mapping:my_dsp]
archive: libmy_dsp.a
entries:
    if MY_DSP_IN_IRAM = y:
        dsp (noflash)
    else:
        * (default)
```

## Custom schemes and sections
```
[sections:my_buf]
entries:
    .my_buf+

[scheme:my_buf_rtc]
entries:
    my_buf -> rtc_data

[mapping:my_dsp_buf]
archive: libmy_dsp.a
entries:
    dsp (my_buf_rtc)              # a scheme only takes effect when a mapping uses it
```
A `sections` fragment lists input sections (a trailing `+` also matches `.name.*`); a `scheme` maps a sections
fragment to a target such as `iram0_text`, `dram0_data`, `rtc_text`, `rtc_data` or `rtc_bss`.
Prefer attributes for single variables (`RTC_DATA_ATTR`, `RTC_NOINIT_ATTR`, `EXT_RAM_BSS_ATTR`,
`DRAM_ATTR`); fragments are for whole objects or third-party code you cannot annotate.

## Checks
- Inspect the generated `sections.ld` (written under the esp_system component's build directory) to confirm the placement rule appeared.
- `idf.py size-files` before/after to see IRAM move.
- Check the link map file or `nm` output for the symbol and confirm its address falls in the IRAM range of your target.

## Pitfalls
- A mapping only affects what it names: a wrong archive or object name leaves the default placement, so verify with the map file.
- Code in IRAM that calls a flash function still crashes when the cache is disabled; follow the
  whole call chain (see iram-attr-and-cache-disabled-code).
- IRAM is scarce and also reduces the DRAM left for heap; keep only ISR and latency-critical code there.

## Verify
- [ ] Map file shows the target symbols in the intended region.
- [ ] Build fails loudly (link error) rather than silently when IRAM overflows.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/linker-script-generation.rst, memory-types.rst, components/esp_system/app.lf).
Confirmed: `LDFRAGMENTS` in `idf_component_register`; `[mapping:name]` with `archive:` and `entries:`; object, symbol (`object:symbol`) and `*` granularity; `noflash`, `rtc` and `default` schemes plus `noflash_text` and `noflash_data` from app.lf; `if CONFIG = y: ... else:` conditional syntax (Kconfig name without the CONFIG_ prefix); `[sections:...]` and `[scheme:...]` grammar; the symbol-granularity warning; generated `sections.ld` from `esp_system/ld/<target>/sections.ld.in`; `EXT_RAM_BSS_ATTR` needs `CONFIG_SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY`. Corrected: the custom scheme target `rtc_slow_data` (not a target in app.lf, use `rtc_data`) and the missing mapping that applies a custom scheme. Removed unconfirmed claims: silently ignored mismatched entries, the 0x4008xxxx ESP32 IRAM range and the 128 KB IRAM figure.

Method: documentation only; no commands were run.
