---
id: computing-software.firmware-embedded-development.zephyr.soc-porting
name: soc-porting
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [soc-porting, soc-yml, soc-kconfig, soc-dtsi, soc-family-series, zephyr, firmware-embedded-development]
level: sme
status: docs-checked
description: "Add a new SoC to Zephyr under hardware model v2: soc.yml family/series/soc hierarchy, Kconfig.soc and defconfig, the SoC dtsi, early init hooks, and linker/MPU setup."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/soc_porting.html
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://docs.zephyrproject.org/latest/develop/modules.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/platform/hooks.h
  - https://docs.zephyrproject.org/latest/releases/migration-guide-4.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SoC porting

Usually you add a new **SoC variant** to an existing family (e.g. another STM32 part); a brand-new
architecture is a much larger job. Work out-of-tree first (a module with `soc_root`, SoCs under `<soc_root>/soc`), upstream later.

## Directory layout (HWMv2)
```
soc/<vendor>/<soc-name>/            # any folder structure is allowed in a local repository
  soc.yml  soc.h  CMakeLists.txt  Kconfig.soc      # mandatory
  Kconfig  Kconfig.defconfig                        # optional
dts/<arch>/<vendor>/<soc>.dtsi
```
Family and series trees (`soc/<vendor>/<family>/<series>/...`) are common upstream. The
`<vendor>` folder must match `dts/bindings/vendor-prefixes.txt` when contributing to Zephyr.

## soc.yml
```yaml
family:
  - name: acme_m
    series:
      - name: acme_m4
        socs:
          - name: acme_m4x1
          - name: acme_m4x2
            cpuclusters:          # only for multi-core parts
              - name: cpuapp
              - name: cpunet
```

## Kconfig.soc (selection symbols, no prompts)
```kconfig
config SOC_FAMILY_ACME_M
    bool
config SOC_FAMILY
    default "acme_m" if SOC_FAMILY_ACME_M

config SOC_SERIES_ACME_M4
    bool
    select SOC_FAMILY_ACME_M
config SOC_ACME_M4X1
    bool
    select SOC_SERIES_ACME_M4
config SOC
    default "acme_m4x1" if SOC_ACME_M4X1
```
`Kconfig.soc` must not select anything outside the SoC Kconfig tree; `Kconfig` selects the
architecture and hardware support, for example `select ARM`, `select CPU_CORTEX_M4`,
`select CPU_HAS_FPU`, `select CPU_CORTEX_M_HAS_SYSTICK` (symbols that exist in `arch/`).
`Kconfig.defconfig` holds SoC defaults inside `if SOC_<NAME>` ... `endif`, for example `NUM_IRQS`,
and the system timer choice (`CORTEX_M_SYSTICK` or a SoC timer driver).

## Devicetree
`<soc>.dtsi` (under `dts/<ARCH>/<VENDOR>/`, included by every board using the SoC) describes the
`chosen` settings, `cpus`, and the `soc` node with memory, buses and peripherals; start from the
architecture `<arch>.dtsi` if one exists. The Arm NVIC node requires `reg` and
`arm,num-irq-priority-bits`. Multi-cluster SoCs use one `<soc>_<cluster>.dtsi` per cluster.

## Code
- `soc.c`: SoC hooks declared in `zephyr/platform/hooks.h`, enabled by Kconfig, for example
  `soc_early_init_hook()` (`CONFIG_SOC_EARLY_INIT_HOOK`), `soc_prep_hook()` (`CONFIG_SOC_PREP_HOOK`)
  and `soc_reset_hook()` (`CONFIG_SOC_RESET_HOOK`), for clock trees, cache enable, errata. The
  4.5 migration guide says `z_arm_platform_init()` was replaced by `soc_reset_hook()`.
- `pinctrl_soc.h`: maps DT pinctrl to the SoC's pin mux registers for the pinctrl driver.
- `CMakeLists.txt` must define the base-line linker script (for Cortex-M the architecture one is
  `include/zephyr/arch/arm/cortex_m/scripts/linker.ld`); extra RAM regions use devicetree
  `zephyr,memory-region` nodes (`dts/bindings/base/zephyr,memory-region.yaml`).
- MPU regions: Arm SoCs provide `arm_mpu_regions.c` (see `arch/arm/core/mpu`) if the defaults
  do not fit.

## Bring-up order
1. Minimal: CPU, SRAM, flash, NVIC, SysTick, one UART; `hello_world` with a test board.
2. GPIO + pinctrl; then clock control driver.
3. Run `tests/kernel` with twister on the board (device testing uses `--device-testing` with a
   hardware map).
4. Add drivers peripheral by peripheral (most reuse existing IP drivers via `compatible`).

## Verify
- [ ] `west build -b <test_board> samples/hello_world` boots and prints.
- [ ] The `tests/kernel` suite passes with twister on the board.
- [ ] `soc.yml` names match Kconfig `SOC`/`SOC_SERIES`/`SOC_FAMILY` strings.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository (migration guide read from main, the 4.5 development branch).
Confirmed in the SoC porting guide: mandatory files soc.yml, soc.h, CMakeLists.txt, Kconfig.soc and optional Kconfig/Kconfig.defconfig; the soc.yml family/series/socs/cpuclusters schema; the Kconfig.soc symbol pattern (SOC_FAMILY_*, SOC_SERIES_*, SOC_*, with SOC_FAMILY/SOC_SERIES/SOC defaults and names matching soc.yml); Kconfig.soc must not select outside the SoC tree; Kconfig.defconfig wrapped in `if SOC_<NAME>`; the dtsi location and `<soc>_<cluster>.dtsi` naming; the module `soc_root` key; the vendor-prefix rule. Confirmed in source: hooks and their Kconfig guards in `platform/hooks.h`; `CPU_CORTEX_M4`, `CPU_HAS_FPU`, `CPU_CORTEX_M_HAS_SYSTICK`, `NUM_IRQS`, `CORTEX_M_SYSTICK` symbols; `arm,num-irq-priority-bits`; the Cortex-M linker script and `zephyr,memory-region` binding.
Removed as unconfirmed: the `Kconfig.defconfig.<soc>` and per-series file names, `pinctrl_soc.h` as a required file, and the symbols HAS_SWO, HAS_PM, CPU_HAS_ARM_MPU and SYS_CLOCK_HW_CYCLES_PER_SEC. Fixed: soc.h is a mandatory file, and the hook list was updated to the hooks.h names.

Method: documentation only; no commands were run.
