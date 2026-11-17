---
id: computing-software.firmware-embedded-development.esp-idf.ulp-riscv-and-lp-core
name: ulp-riscv-and-lp-core
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-sleep, ulp-riscv, lp-core, ulp-coprocessor, ulp-shared-variables, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Program the ESP32-S3 ULP RISC-V coprocessor or the ESP32-C6 LP core in C to sample sensors while the main CPU sleeps and wake it only when needed."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ulp-risc-v.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32c6/api-reference/system/ulp-lp-core.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ULP RISC-V and LP core

The ESP32-S3 has a ULP RISC-V coprocessor and the ESP32-C6 has an LP core. Both run small C
programs while the main CPU stays in a low-power mode. Check the page for your chip: other
chips are covered by their own chip-specific pages.

## ULP RISC-V (S3)
- 32-bit fixed-point core (RV32IMC): no floating-point hardware. It reaches `RTC_SLOW_MEM` and
  the RTC_CNTL, RTC_IO and SARADC registers.
- Put the ULP sources in a directory such as `ulp/` and call `ulp_embed_binary` after
  `idf_component_register`:
```cmake
idf_component_register()
set(ulp_app_name ulp_${COMPONENT_NAME})
set(ulp_sources "ulp/ulp_c_source_file.c")
set(ulp_exp_dep_srcs "ulp_c_source_file.c")
ulp_embed_binary(${ulp_app_name} "${ulp_sources}" "${ulp_exp_dep_srcs}" TYPE riscv)
```
  The third argument lists the component sources that include the generated header, so it
  exists before they compile. `TYPE riscv` is needed if both FSM and RISC-V types are selected.
- menuconfig: enable `CONFIG_ULP_COPROC_ENABLED`, select `CONFIG_ULP_COPROC_TYPE_RISCV`, and set
  `CONFIG_ULP_COPROC_RESERVE_MEM` big enough for the ULP code and data (the largest program if
  there are several).
- Main side: reference the embedded blob, then load and start it:
```c
extern const uint8_t bin_start[] asm("_binary_ulp_app_name_bin_start");
extern const uint8_t bin_end[]   asm("_binary_ulp_app_name_bin_end");
ESP_ERROR_CHECK(ulp_riscv_load_binary(bin_start, (bin_end - bin_start)));
ESP_ERROR_CHECK(ulp_riscv_run());
```
- A timer starts the program; set the period with `ulp_set_wakeup_period()`. The program runs
  until `RTC_CNTL_COCPU_DONE` is written or a trap occurs; then the core powers down and the
  timer restarts.
- Global ULP variables appear in the generated header with the `ulp_` prefix (use `PREFIX` in
  `ulp_embed_binary` when embedding several programs). They live in `.bss`/`.data`, which are
  initialised on load, so reading them from the main CPU before the first ULP run may give
  undefined behaviour.
- Peripheral access: RTC I2C needs `ulp_riscv_i2c_master_init()` from the main core before
  sleeping; see the page for the other peripherals and for the software lock API
  (`ulp_riscv_lock_acquire()`, `ulp_riscv_lock_release()`).
- Debugging: JTAG and printf are not available. Write state to a shared variable and read it
  from the main CPU; the page notes that keeping the main CPU awake can mask power-domain bugs.

## LP core (C6)
- RV32 core with the M, A and C extensions, an interrupt controller and a debug module that
  supports JTAG. It reaches LP SRAM and LP peripherals while the HP system sleeps.
- Same embedding scheme; load with `ulp_lp_core_load_binary`, start with `ulp_lp_core_run`:
```c
ulp_lp_core_cfg_t cfg = {
    .wakeup_source = ULP_LP_CORE_WAKEUP_SOURCE_LP_TIMER,
    .lp_timer_sleep_duration_us = 10000,
};
ESP_ERROR_CHECK(ulp_lp_core_run(&cfg));
```
- `CONFIG_ULP_COPROC_RUN_FROM_HP_MEM` moves most of the code to HP SRAM, but then the LP core
  cannot keep running in Deep-sleep. Keep the default LP-memory mode for deep-sleep use.

## Waking the main CPU and current draw
Use the wake-up APIs documented on the same pages for your chip and measure the resulting
current; it depends on the wake period and the run time per period.

## Verify
- [ ] Main CPU wakes only when the threshold is crossed.
- [ ] Shared variable values survive across main-CPU sleep cycles.

## Checked
2026-10-31. Confirmed against the ESP-IDF ULP RISC-V (ESP32-S3) and ULP LP core (ESP32-C6)
programming guides: `ulp_embed_binary` usage, the Kconfig options named, blob symbols,
load/run functions, `ulp_set_wakeup_period`, the program flow, variable prefix and init
behaviour, no JTAG on the ULP RISC-V, JTAG on the LP core, LP core config fields, and the HP
memory option. Removed: ESP32-S2 and P4 coverage, current-draw figures, a fixed reserve-memory
value, the `REQUIRES ulp` argument, sleep-wakeup API calls and ULP helper function names that
the pages fetched did not show.
Method: documentation only; no commands were run.
