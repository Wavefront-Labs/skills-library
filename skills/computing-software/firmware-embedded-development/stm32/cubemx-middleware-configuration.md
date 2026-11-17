---
id: computing-software.firmware-embedded-development.stm32.cubemx-middleware-configuration
name: cubemx-middleware-configuration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, cubemx-middleware, freertos-cmsis-rtos, fatfs-cubemx, usb-device-cubemx, lwip-cubemx, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Configure STM32CubeMX middleware (FreeRTOS, FatFs, USB Device, LwIP, Azure RTOS/ThreadX) correctly: dependencies, timebase, heap sizes and regeneration-safe user code."
sources:
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
  - https://wiki.st.com/stm32mcu/wiki/Introduction_to_STM32Cube_middleware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Middleware configuration in CubeMX

CubeMX can enable middleware stacks under "Middleware and Software Packs". Each has
prerequisites that CubeMX only partly enforces.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## FreeRTOS (CMSIS-RTOS v1/v2)
- Change the HAL timebase from SysTick to a basic timer (TIM6/TIM7) in SYS > Timebase Source.
  FreeRTOS owns SysTick; CubeMX warns, and ignoring it gives HAL_Delay hangs.
- Heap: `configTOTAL_HEAP_SIZE` (heap_4) must fit RAM after .bss; check the Build Analyzer.
- Tasks/queues created in CubeMX land in `main.c`/`app_freertos.c`; put task bodies in user
  sections or separate files.
- Enable `configCHECK_FOR_STACK_OVERFLOW` and `configUSE_MALLOC_FAILED_HOOK` in Config parameters.

## FatFs
- Select the medium: SD Card (needs SDMMC/SDIO plus DMA), User-defined (you implement
  `user_diskio.c`), or USB Disk (with USB Host MSC).
- SD with DMA plus FreeRTOS requires the RTOS-aware template (`sd_diskio.c` with queues);
  CubeMX selects it when FreeRTOS is enabled.
- `_USE_LFN` needs heap or stack buffer; `_MAX_SS` 4096 for flash with 4 KB sectors.

## USB Device
- Enable USB_OTG_FS (Device_Only) first, then middleware class (CDC, MSC, HID, DFU).
- USB needs an accurate 48 MHz clock (PLL Q or HSI48 + CRS): the clock tab must show 48 MHz exactly.
- CDC `CDC_Receive_FS` and `CDC_Transmit_FS` are in `usbd_cdc_if.c` user sections.
- Raise `USBD_MAX_STR_DESC_SIZ` / endpoint sizes only via CubeMX parameters (regeneration overwrites `usbd_conf.h`).

## LwIP
- Requires ETH with correct PHY (LAN8742 template) and RMII pins; on H7, MPU and memory
  placement for DMA descriptors (`.RxDecripSection` in D2 SRAM) must be added by hand in the linker script.
- DHCP or static IP in the General Settings tab.

## Azure RTOS / ThreadX (X-CUBE-AZRTOS)
- Comes as a pack for newer series (U5, H5, H7). Like FreeRTOS, needs a non-SysTick HAL timebase.
- In 2024+ ST moved to Eclipse ThreadX naming; packs still generate `app_threadx.c`.

## Regeneration
Middleware configuration files (`FreeRTOSConfig.h`, `ffconf.h`, `usbd_conf.h`, `lwipopts.h`)
are regenerated. Edit settings in CubeMX, or only inside USER CODE sections.

## Verify
- [ ] Build Analyzer shows RAM margin with all heaps and stacks.
- [ ] Regenerate the project with no diff in your user code.
- [ ] Each stack's example function works (USB enumerates, file write/read, ping).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
