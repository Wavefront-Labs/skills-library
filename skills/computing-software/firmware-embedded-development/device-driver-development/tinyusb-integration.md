---
id: computing-software.firmware-embedded-development.device-driver-development.tinyusb-integration
name: tinyusb-integration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-device, tinyusb, tusb-config, tud-task, usb-composite, dcd-port, rtos-integration, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Integrate the TinyUSB device stack: tusb_config.h, descriptor callbacks, running tud_task from a loop or RTOS task, IRQ hookup and building composite devices."
sources:
  - https://docs.tinyusb.org/en/latest/
  - https://github.com/hathach/tinyusb/blob/master/src/tusb_option.h
  - https://github.com/hathach/tinyusb/blob/master/src/device/usbd.h
  - https://github.com/hathach/tinyusb/blob/master/docs/troubleshooting.rst
  - https://github.com/hathach/tinyusb/blob/master/docs/integration.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TinyUSB integration

**Goal:** add USB device classes (CDC, HID, MSC, MIDI, vendor) to an MCU project with
TinyUSB, which supports STM32, nRF5x, RP2040, ESP32-S2/S3, SAMD, i.MX RT and many others (see the
`OPT_MCU_*` list in `tusb_option.h`).

## Pieces you provide
1. **`tusb_config.h`**:
   ```c
   #define CFG_TUSB_MCU          OPT_MCU_STM32F4
   #define CFG_TUSB_OS           OPT_OS_FREERTOS     /* or OPT_OS_NONE */
   #define CFG_TUD_ENABLED       1
   #define CFG_TUD_ENDPOINT0_SIZE 64
   #define CFG_TUD_CDC           1
   #define CFG_TUD_HID           1
   #define CFG_TUD_CDC_RX_BUFSIZE 512
   #define CFG_TUD_CDC_TX_BUFSIZE 512
   ```
2. **Descriptor callbacks**: `tud_descriptor_device_cb`, `tud_descriptor_configuration_cb`,
   `tud_descriptor_string_cb` (copy `usb_descriptors.c` from an example and edit).
3. **USB IRQ** forwarding to the stack:
   ```c
   void OTG_FS_IRQHandler(void) { tud_int_handler(0); }
   ```
4. **Clock and pins**: 48 MHz USB clock (PLL Q or HSI48 + CRS), USB pins configured, VBUS
   sensing configured or disabled to match the board.

## Running the stack
```c
tud_init(BOARD_TUD_RHPORT);       /* or tusb_init(); older style needs CFG_TUSB_RHPORT0_MODE in tusb_config.h */
for (;;) { tud_task(); app(); }   /* bare metal: call it from the main loop often (the docs say under 1 ms apart) */
```
With an RTOS, run `tud_task()` in a dedicated task: `tud_task()` is `tud_task_ext(UINT32_MAX, false)`, so it waits
for USB events. Initialise the stack in the same task/context as `tud_task()`.

## Composite devices
Enable several classes in config, then make the configuration descriptor contain each
function's interfaces (use helper macros `TUD_CDC_DESCRIPTOR`, `TUD_HID_DESCRIPTOR`), with
unique interface numbers and endpoint addresses, and the total length summed
(`TUD_CONFIG_DESC_LEN + TUD_CDC_DESC_LEN + TUD_HID_DESC_LEN`).

## Gotchas
- **Wrong USB clock**: USB needs a precise 48 MHz clock; check the crystal and PLL settings.
- **VBUS sensing**: the troubleshooting guide lists VBUS sensing configuration among the hardware
  settings to check; match it to how the board is wired.
- On STM32 Cube projects, don't also enable ST's USB middleware: two stacks fight over the IRQ.
- `tud_task` starvation (long blocking code in the main loop) breaks enumeration: the docs list
  "`tud_task()` not called" among the causes.
- RP2040 builds use the pico-sdk, which can override `tusb_config.h` settings such as `CFG_TUSB_OS`. ESP32
  builds need ESP-IDF v5.3 or later and an example with an ESP-IDF build file (for example
  `cdc_msc_freertos`).

## Verify
- [ ] Example `cdc_msc` builds and enumerates on your board before you customise.
- [ ] Composite device shows all functions on Windows, macOS, Linux.

## Checked

2026-10-27, hathach/tinyusb master (source and docs).
Confirmed in tusb_option.h: CFG_TUSB_MCU, OPT_MCU_STM32F4/G4/H7, RP2040, ESP32S2/S3, SAMD21, NRF5X, MIMXRT, CFG_TUSB_OS with OPT_OS_NONE and OPT_OS_FREERTOS, CFG_TUD_ENABLED, CFG_TUD_ENDPOINT0_SIZE, CFG_TUD_CDC, CFG_TUD_HID, CFG_TUSB_RHPORT0_MODE. Confirmed in cdc_device.h: CFG_TUD_CDC_RX_BUFSIZE and TX. Confirmed in usbd.h: tud_task, tud_task_ext (tud_task waits with UINT32_MAX), tud_init(rhport), tud_int_handler, the three descriptor callbacks, TUD_CONFIG_DESC_LEN, TUD_CDC_DESCRIPTOR, TUD_CDC_DESC_LEN, TUD_HID_DESCRIPTOR, TUD_HID_DESC_LEN. Confirmed in docs: precise 48 MHz clock, VBUS sensing configuration, tud_task not being called as a cause of enumeration failure, ST's USB middleware conflicting with TinyUSB, pico-sdk overriding CFG_TUSB_OS, ESP-IDF v5.3 or later. Removed the HSI48/CRS claim, the NOVBUSSENS register names, the task priority and ISR-call advice, and the esp_tinyusb and Pico SDK bundling statements. The cdc_msc example exists in examples/device.

Method: documentation only; no commands were run.
