---
id: computing-software.firmware-embedded-development.esp-idf.memory-protection
name: memory-protection
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, esp-memprot, pmp, permission-control, iram-dram-split, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use ESP-IDF memory protection (memprot on S2/S3, PMS/PMP on C3/C6) to block execution from data RAM and writes to code RAM, and debug the faults it raises."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/fatal-errors.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/Kconfig
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-guides/memory-types.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory protection

Memory protection splits internal RAM into an executable IRAM region and a non-executable DRAM
region, then locks the split. It turns code injection (write shellcode into a buffer, jump to
it) into an immediate panic.

## Enable
```
CONFIG_ESP_SYSTEM_MEMPROT=y                  # default y where the chip supports it
# choice ESP_SYSTEM_MEMPROT_MODE: pick the mechanism for the chip
CONFIG_ESP_SYSTEM_MEMPROT_PMS=y              # Permission Control Module (PMS), chips with SOC_MEMPROT_SUPPORTED
CONFIG_ESP_SYSTEM_MEMPROT_PMP=y              # CPU Physical Memory Protection, RISC-V chips with an IRAM/DRAM split via PMP
CONFIG_ESP_SYSTEM_MEMPROT_PMS_LOCK=y         # PMS only, default y: settings cannot change until the next chip startup
```
The mode choice defaults to TEE if the Trusted Execution Environment is enabled, otherwise PMP or PMS depending
on the chip. Before ESP-IDF v6.0 the options were named `ESP_SYSTEM_MEMPROT_FEATURE` and `ESP_SYSTEM_PMP_IDRAM_SPLIT`
(per the v6.0 migration guide); check menuconfig for the current names. The feature splits ROM, RAM and flash into data and instruction segments
with Read/Execute permission for the instruction part and Read/Write for the data part, effective on all access
through the IRAM0 and DRAM0 buses.

## What it blocks
- Writing to instruction RAM after the program is loaded.
- Executing code from data RAM (heap, static `.data` and `.bss`).
When the fault occurs, the panic handler reports the address of the fault and the type of memory access
("Memory Protection Fault" in the panic output).

## Things that break
- Code that copies functions into RAM to run them (custom loaders, JIT, some interpreters) or self-modifying code.
  Allocating memory with `MALLOC_CAP_EXEC` is not possible while the feature is enabled (since v6.0 the macro is not
  even defined, so using it is a compile error); the ESP-IDF docs say
  applications relying on dynamic loading or self-modifying code may disable `CONFIG_ESP_SYSTEM_MEMPROT`, which should
  be a recorded risk decision for that product.
- Patched IRAM functions.

## Relationship to other features
Memory protection complements Secure Boot (who can run code) and flash encryption (who can
read it); it limits what a memory-corruption bug can do at runtime. Combine with stack
smashing protection and heap poisoning in development.

## Verify
- [ ] Test build that jumps into a DRAM buffer panics with a memory protection fault.
- [ ] Production sdkconfig has the feature and lock enabled (or documented reason why not).
- [ ] Debugging workflow (breakpoints) still usable on development builds.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/fatal-errors.rst "Memory Protection Fault" section, components/esp_system/Kconfig and the v6.0 system migration guide).
Confirmed: `CONFIG_ESP_SYSTEM_MEMPROT` (default y, depends on chip support), the PMS/PMP/TEE mode choice, `CONFIG_ESP_SYSTEM_MEMPROT_PMS_LOCK` (PMS only, default y), the Read/Execute versus Read/Write split, `MALLOC_CAP_EXEC` being unavailable when enabled, and the fatal-errors description of blocked accesses. Corrected: the pre-6.0 option names `ESP_SYSTEM_MEMPROT_FEATURE`, `ESP_SYSTEM_MEMPROT_FEATURE_LOCK` and `ESP_SYSTEM_PMP_IDRAM_SPLIT` (replaced in v6.0, confirmed by the v6.0 migration guide) and the advice to use `MALLOC_CAP_EXEC` as a workaround. Removed unconfirmed claims: exact fault message strings, RTC fast memory rules on S3 and the debugger breakpoint behaviour. The security.html source page link was dropped because it was not read.

Method: documentation only; no commands were run.
