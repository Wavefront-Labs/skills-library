---
id: computing-software.firmware-embedded-development.stm32.usb-device-library
name: usb-device-library
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-comms, stm32-usb-device, usb-cdc, usbd-descriptors, usb-composite, stm32, firmware-embedded-development]
level: advanced
status: draft
description: "Build STM32 USB device firmware with the ST USB Device library (CDC, MSC, HID, composite): descriptors, endpoint PMA config, CDC transmit flow control and enumeration debugging."
sources:
  - https://www.st.com/resource/en/user_manual/um1734-stm32cube-usb-device-library-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/stm32_mw_usb_device
  - https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STM32 USB device library

ST's classic middleware (`stm32_mw_usb_device`): core (`usbd_core`), classes (CDC, MSC, HID, DFU,
Audio, CustomHID), and the glue (`usbd_conf.c`, `usbd_desc.c`, `usbd_xxx_if.c`). Newer series
(U5, H5) also offer USBX (Azure RTOS) via CubeMX.

## CDC (virtual COM port)
```c
/* usbd_cdc_if.c */
static int8_t CDC_Receive_FS(uint8_t *buf, uint32_t *len) {
    ring_put(buf, *len);                                /* copy out quickly */
    USBD_CDC_SetRxBuffer(&hUsbDeviceFS, &UserRxBufferFS[0]);
    USBD_CDC_ReceivePacket(&hUsbDeviceFS);              /* re-arm OUT endpoint */
    return USBD_OK;
}
uint8_t usb_send(uint8_t *p, uint16_t n) {
    USBD_CDC_HandleTypeDef *c = hUsbDeviceFS.pClassData;
    if (c == NULL || c->TxState != 0) return USBD_BUSY; /* previous transfer still running */
    USBD_CDC_SetTxBuffer(&hUsbDeviceFS, p, n);
    return USBD_CDC_TransmitPacket(&hUsbDeviceFS);
}
```
- `CDC_Transmit_FS` returns BUSY instead of queuing: build a TX ring buffer and send the next
  chunk from `CDC_TransmitCplt_FS` (newer versions) or a periodic task.
- Transfers that are an exact multiple of 64 bytes need a zero-length packet to end the
  transfer on the host side.
- Receive callback runs in USB interrupt context: no blocking.

## Descriptors
`usbd_desc.c`: VID/PID (use your own VID or ST's 0x0483 only for development), strings, serial
number (generated from the UID). Changing PID/class requires Windows to re-enumerate (driver
cache: uninstall device or bump `bcdDevice`).

## Endpoint memory (FS device peripheral on F0/F1/F3/L0/L4/G4)
PMA buffer addresses are set in `USBD_LL_Init` with `HAL_PCDEx_PMAConfig()`. Composite devices
need non-overlapping PMA offsets after the BTABLE (EP0 OUT/IN at 0x18/0x58 typical). OTG cores
(F4/F7/H7) use FIFO sizes via `HAL_PCDEx_SetRxFiFo/SetTxFiFo` instead.

## Composite devices
The classic library supports one class per instance; composite (CDC+MSC, CDC+HID) needs
hand-merged descriptors and class dispatch, or the newer library version with
`USE_USBD_COMPOSITE` and `USBD_RegisterClassComposite`.

## Enumeration debugging
- No enumeration at all: 48 MHz clock wrong, D+ pull-up missing (F1 needs external 1.5 k, most
  others internal), VBUS sensing enabled without VBUS connected (`vbus_sensing_enable = DISABLE`).
- "Device descriptor request failed": interrupt priority or the USB IRQ handler not linked.
- Use Wireshark + USBPcap or a hardware analyser to see the descriptor exchange.

## Verify
- [ ] Enumerates on Windows, macOS and Linux; survives unplug/replug and host sleep.
- [ ] CDC throughput test at sustained rate without data loss.
