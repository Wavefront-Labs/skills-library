---
id: computing-software.firmware-embedded-development.stm32.external-flash-loaders
name: external-flash-loaders
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [external-loader, stldr, octospi, memory-mapped-flash, stm32cubeprogrammer, stm32, firmware-embedded-development]
level: advanced
status: draft
description: "Program and debug code or assets in external QSPI/OSPI flash on STM32 with CubeProgrammer external loaders (.stldr): choosing or building one, linker placement and IDE setup."
sources:
  - https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/stm32-external-loader
  - https://www.st.com/resource/en/application_note/an4760-quadspi-interface-on-stm32-microcontrollers-and-microprocessors-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# External flash loaders

When images, fonts or code live in external NOR flash mapped at e.g. `0x90000000`, the probe
can't program it directly. An **external loader** is a small program the programmer downloads
to the MCU's RAM; it knows how to initialise the QSPI/OSPI peripheral and erase/write the chip.

## Using an existing loader
CubeProgrammer ships loaders for ST boards in `bin/ExternalLoader/` (e.g.
`MX25LM51245G_STM32L4R9I-DISCO.stldr`).
```bash
STM32_Programmer_CLI -c port=SWD mode=UR \
    -el "<CubeProgrammer>/bin/ExternalLoader/MX25LM51245G_STM32L4R9I-DISCO.stldr" \
    -w app.hex -v -rst
STM32_Programmer_CLI -c port=SWD -el <loader> -r32 0x90000000 0x40   # read back external
```
A combined `.hex`/`.elf` with sections in internal and external flash is programmed in one go.
A loader is specific to **flash chip + pins + MCU**: a Disco board's loader won't work on your
custom board if the QSPI pins or chip differ.

## Building your own
Start from ST's `stm32-external-loader` repository (templates per flash family). A loader is an
ELF (renamed `.stldr`) containing:
- `StorageInfo` struct: device name, type (`NOR_FLASH`), start address, size, page size,
  erase value `0xFF`, sector table.
- Functions: `Init`, `Write`, `SectorErase`, `MassErase`, `Read` (optional), `Verify`/`Checksum`
  (optional).
- Linked to run from internal RAM (template linker script places it at `0x20000004`), no
  interrupts relied on (SysTick-based HAL delays need care: override `HAL_Delay`/`HAL_GetTick`).
Reuse your board's QSPI driver code (pins, clock, dummy cycles, quad enable) so that loader and
application match. Test with `-el` read/erase/write/verify before trusting it.

## Application side
Linker script region and section:
```ld
MEMORY { ... QSPI (rx) : ORIGIN = 0x90000000, LENGTH = 16M }
SECTIONS { .extflash : { *(.extflash*) } >QSPI }
```
```c
__attribute__((section(".extflash"))) const uint8_t splash_png[] = { ... };
```
Before accessing it at run time, the app must init QSPI and enable **memory-mapped mode**
(`HAL_QSPI_MemoryMapped` / `HAL_OSPI_MemoryMapped`). If code executes from external flash, this
must happen before any such function is called (early in `SystemInit` or startup). MPU
attributes: mark the region as normal, cacheable memory and make unused space beyond the chip
non-executable to avoid speculative-access faults (Cortex-M7).

## Debugging
STM32CubeIDE: Debug configuration > Debugger > External loaders: add the `.stldr` so flashing
before debug includes the external sections. Breakpoints in external flash are hardware
breakpoints only.

## Verify
- [ ] Read back of external region matches the image (`-r32` or `-u` dump compare).
- [ ] Cold boot without debugger: app enables memory-mapped mode and assets load correctly.
- [ ] Loader stored in the repo with source and the exact build that produced it.
