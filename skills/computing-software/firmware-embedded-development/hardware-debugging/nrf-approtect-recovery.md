---
id: computing-software.firmware-embedded-development.hardware-debugging.nrf-approtect-recovery
name: nrf-approtect-recovery
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [approtect, nrf52, nrf53, nrfjprog-recover, ctrl-ap, eraseall, uicr, access-port-protection, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Recover locked Nordic nRF devices: APPROTECT behaviour on nRF52 rev3/nRF53/nRF91, CTRL-AP ERASEALL via nrfutil/nrfjprog/OpenOCD, and keeping debug open in firmware."
sources:
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/dif.html
  - https://docs.nordicsemi.com/bundle/nwp_044/page/WP/nwp_044/nWP_044_intro.html
  - https://openocd.org/doc/html/Flash-Commands.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# nRF APPROTECT recovery

## What changed
- nRF52 older revisions: debug is open unless `UICR.APPROTECT` is written to 0x00.
- nRF52 build code Fxx/rev3+, nRF5340, nRF91: **hardware APPROTECT is enabled at every reset**
  unless firmware also opens it: `UICR.APPROTECT = HwDisabled (0x5A)` **and** at runtime
  `NRF_APPROTECT->DISABLE = APPROTECT_DISABLE_DISABLE_SwDisable` (nRF52: written by MDK
  `SystemInit` when `ENABLE_APPROTECT` is not defined). Old firmware on new silicon locks after the
  first reset; that is the classic "worked once, now cannot connect".

## Symptoms
- `nrfjprog --readregs`: "Access protection is enabled".
- OpenOCD/pyOCD: AHB-AP reads fail, `IDR` reads 0 for AP0, while CTRL-AP (AP1 on nRF52) works.

## Recover (erases flash, RAM and UICR)
```sh
nrfutil device recover --serial-number <sn>          # current tool
nrfjprog --recover -f NRF52                          # legacy
nrfjprog --recover -f NRF53 --coprocessor CP_NETWORK # then CP_APPLICATION
```
OpenOCD: `nrf52_recover` (in `target/nrf52.cfg`) or manually through CTRL-AP:
```tcl
dap apreg 1 0x04 0x01      ;# ERASEALL
sleep 500
dap apreg 1 0x08           ;# ERASEALLSTATUS -> 0 when done
dap apreg 1 0x00 1 ; dap apreg 1 0x00 0   ;# RESET pulse
```
J-Link: `J-Link Commander` will offer to unsecure when it detects protection.

## Keep debug open in development builds
- Write `UICR.APPROTECT = 0x5A` in the hex (Zephyr/NCS: `CONFIG_NRF_APPROTECT_USE_UICR=y` or
  `CONFIG_NRF_APPROTECT_LOCK=n`; nRF5 SDK: do not define `ENABLE_APPROTECT`).
- Production: lock deliberately (`ENABLE_APPROTECT`, NCS `CONFIG_NRF_APPROTECT_LOCK=y`) and add
  SECUREAPPROTECT on nRF53/91 for the secure domain.

## Gotchas
- Recover wipes UICR too: bootloader settings, keys and calibration you put there are gone.
- nRF5340: recover the network core first, then the application core.
- A hard-locked part whose firmware still writes APPROTECT-enable will relock on every reset;
  recovering and flashing immediately in one session is the only way.

## Verify
- [ ] After flashing dev firmware and a power cycle, the probe still attaches.
- [ ] Production firmware readback via AHB-AP fails as intended.
