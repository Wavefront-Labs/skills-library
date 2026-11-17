---
id: computing-software.firmware-embedded-development.stm32.rdp-regression-and-lifecycle
name: rdp-regression-and-lifecycle
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, rdp-regression, rdp-level-0-5, oem-key-regression, product-lifecycle, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Manage STM32 readout protection lifecycle: level 1 regression with mass erase, level 0.5 on TrustZone parts, password (OEM key) regression on U5/L5 and H5 product states."
sources:
  - https://www.st.com/resource/en/application_note/an5156-introduction-to-stm32-microcontrollers-security-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0456-stm32u5-series-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://wiki.st.com/stm32mcu/wiki/Security:Debug_Authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDP regression and lifecycle

## Classic RDP (F/L/G series)
- Level 0 (0xAA): open. Level 1: flash not readable via debug/bootloader/RAM boot. Level 2 (0xCC):
  debug disabled forever.
- **Regression 1 -> 0**: write RDP = 0xAA; the device mass-erases user flash (and backup
  registers/SRAM2 on some) first. Firmware is gone; the chip is reusable.
  ```bash
  STM32_Programmer_CLI -c port=SWD mode=UR -ob RDP=0xAA
  ```
  A power cycle (not just reset) may be required for level changes to take effect.
- Level 2 has no regression.

## TrustZone parts (L5, U5, H5 TZ variants): level 0.5
With TZEN=1, level 0.5 blocks debug access to secure memory while allowing non-secure debug.
Typical in development of secure firmware. Regression from 1 to 0.5 erases non-secure flash
only; from 0.5/1 to 0 erases everything and is required to clear TZEN.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Password regression (L5/U5 OEM keys)
U5/L5 add OEM1/OEM2 keys (`OEM1KEYR`, `OEM2KEYR`) programmed while at level 0/0.5. Then:
- Level 2 can regress to level 1 only if OEM2 key is provided via the debug port (U5): devices can
  be returned for failure analysis without making level 2 truly permanent.
- Level 1 regression may require OEM1 key (prevents an attacker erasing and reusing the part).
```bash
STM32_Programmer_CLI -c port=SWD -lockRDP1 0x12345678 0x9ABCDEF0      # program OEM1 key (L5/U5 syntax)
STM32_Programmer_CLI -c port=SWD -unlockRDP1 0x12345678 0x9ABCDEF0
```
Command names and argument order are per UM2237 for your CubeProgrammer version.
Lose the key and the regression path is gone.

## H5 product states
H5 replaces RDP with `PRODUCT_STATE`: Open -> Provisioning -> iROT-Provisioned -> TZ-Closed ->
Closed -> Locked. Regression from Closed uses **Debug Authentication (DA)** with a password or
certificate-based challenge (`STM32_Programmer_CLI -c port=SWD debugauth=1`, with provisioned DA
data). Locked is permanent.

## Policy
- Development: level 0 or 0.5. Pilot/production: level 1 with keys or level 2 (with a field
  update path).
- Document per SKU: RDP level, OEM keys custody (HSM/vault), who may run regression.
- Regression = full erase: plan RMA flows accordingly (diagnostics logs exported before).

## Verify
- [ ] Production unit rejects flash reads over SWD.
- [ ] Regression procedure (with keys) tested on a sample, including re-provisioning afterwards.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
