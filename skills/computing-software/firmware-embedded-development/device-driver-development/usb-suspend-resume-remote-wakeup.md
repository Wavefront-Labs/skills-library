---
id: computing-software.firmware-embedded-development.device-driver-development.usb-suspend-resume-remote-wakeup
name: usb-suspend-resume-remote-wakeup
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-suspend, usb-device, remote-wakeup, suspend-current, bus-powered, firmware-embedded-development]
level: advanced
status: gated
description: "Handle USB suspend and resume in device firmware: 3 ms idle detection, the 2.5 mA bus-powered suspend budget, remote wakeup, and Windows selective suspend."
sources:
  - https://github.com/hathach/tinyusb/blob/master/src/device/usbd.h
  - https://github.com/hathach/tinyusb/blob/master/src/device/usbd.c
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/winusb-power-management
  - https://github.com/STMicroelectronics/cmsis_device_l4/blob/master/Include/stm32l476xx.h
  - https://github.com/STMicroelectronics/cmsis_device_f1/blob/master/Include/stm32f103xb.h
  - https://www.usb.org/document-library/usb-20-specification
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspend, resume and remote wakeup

## Suspend
When the host stops sending SOFs (laptop sleeps, Windows selective suspend, hub port suspended),
the bus idles; after **3 ms** of idle the device must enter suspend (gated: unconfirmed, source is paywalled or blocked) and, if bus-powered,
draw at most **2.5 mA** average within 7 ms of the suspend callback (TinyUSB's `usbd.h` comment on
`tud_suspend_cb`, which implies 10 ms from the start of idle).
The controller signals it with a suspend interrupt (STM32 `USB_ISTR_SUSP` on USB FS device cores,
`USB_OTG_GINTSTS_USBSUSP` on OTG cores; TinyUSB `tud_suspend_cb(bool remote_wakeup_en)`).

Firmware response:
1. Stop or slow peripherals and LEDs, put external chips in low-power mode.
2. Set the USB peripheral's low-power bits (`USB_CNTR_FSUSP` and `USB_CNTR_LP_MODE` on STM32 USB FS
   device cores; stop the PHY clock with `USB_OTG_PCGCCTL_STPPCLK` on OTG cores).
3. Enter a sleep/stop mode with the USB wakeup EXTI line enabled.

## Resume
The host drives resume signalling (a K state of about 20 ms) (gated: unconfirmed, source is paywalled or blocked). The controller raises a
wakeup interrupt (`USB_ISTR_WKUP`, or `USB_OTG_GINTSTS_WKUINT` on OTG cores); restore clocks
promptly (about 10 ms) (gated: unconfirmed, source is paywalled or blocked) and continue. If clocks come back too slowly the host may reset
the device.

## Remote wakeup
The device may wake the host (keyboard key press) only if:
- the configuration descriptor `bmAttributes` has the remote-wakeup bit (bit 5) set (gated: unconfirmed, source is paywalled or blocked), and
- the host enabled it with `SET_FEATURE(DEVICE_REMOTE_WAKEUP)` (TinyUSB passes this as
  `remote_wakeup_en`; `tud_remote_wakeup()` works only when suspended and enabled by the host).
Then: wait at least 5 ms after entering suspend and drive resume for 1-15 ms (gated: unconfirmed, source is paywalled or blocked) (STM32 FS
`USB_CNTR_RESUME`, OTG `USB_OTG_DCTL_RWUSIG`, or `tud_remote_wakeup()`), and release.

## Selective suspend (Windows)
Windows may suspend an idle WinUSB device: the `DeviceIdleEnabled` registry value marks it capable
and `DefaultIdleTimeout` sets the idle wait in milliseconds (Microsoft's WinUSB power-management
page); HID devices have their own selective-suspend support. If your device misbehaves after idle
periods, test with selective suspend on.

## Self-powered devices
Self-powered devices still handle suspend and resume; the bus-powered current limit does not
apply. Whether they must drop the D+ pull-up when VBUS is absent (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Measure current while the host sleeps: below 2.5 mA for bus-powered designs.
- [ ] Host sleep/wake cycles 50 times: device resumes without re-enumeration.
- [ ] Remote wakeup wakes a sleeping PC only when enabled by the host.

## Checked

TinyUSB master sources (hathach/tinyusb), Microsoft driver documentation (MicrosoftDocs/windows-driver-docs, staging), STM32 CMSIS device headers and Linux kernel Documentation, read 2026-10-27.
Confirmed in TinyUSB: `tud_suspend_cb(bool remote_wakeup_en)` with the comment that the device must draw an average below 2.5 mA within 7 ms, `tud_resume_cb`, `tud_remote_wakeup()` (only when suspended and enabled by the host), SET_FEATURE remote wakeup handling. Confirmed in the STM32 CMSIS headers: `USB_ISTR_SUSP`, `USB_ISTR_WKUP`, `USB_CNTR_FSUSP`, `USB_CNTR_LP_MODE`, `USB_CNTR_RESUME`, `USB_OTG_GINTSTS_USBSUSP`, `USB_OTG_GINTSTS_WKUINT`, `USB_OTG_DCTL_RWUSIG`, `USB_OTG_PCGCCTL_STPPCLK`. Confirmed in Microsoft's WinUSB power-management page: `DeviceIdleEnabled` and `DefaultIdleTimeout`.
Gated: the 3 ms, 20 ms, 10 ms, 5 ms and 1-15 ms timings, the bmAttributes bit and the self-powered pull-up rule come from the USB 2.0 specification, which was not read in this review. Removed: the USB 1.1 500 uA remark and the claim about CDC devices and selective suspend.

Method: documentation only; no commands were run.
