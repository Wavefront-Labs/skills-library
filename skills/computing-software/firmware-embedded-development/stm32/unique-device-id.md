---
id: computing-software.firmware-embedded-development.stm32.unique-device-id
name: unique-device-id
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, unique-device-id, uid-base, 96-bit-uid, device-serial-number, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Read and use the STM32 96-bit unique device ID (UID_BASE): addresses per series, formatting serial numbers, USB serials and why the UID is not a secret."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1734-stm32cube-usb-device-library-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unique device ID

Every STM32 has a factory-programmed 96-bit unique ID: wafer X/Y coordinates, wafer number and
lot number. Read-only, readable by firmware and debugger.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Read
```c
uint32_t w0 = HAL_GetUIDw0();      /* *(uint32_t *)UID_BASE */
uint32_t w1 = HAL_GetUIDw1();      /* UID_BASE + 4 */
uint32_t w2 = HAL_GetUIDw2();      /* UID_BASE + 8 */
```
`UID_BASE` comes from the device header; it differs per series (F4: 0x1FFF7A10, L4: 0x1FFF7590,
G0/G4: 0x1FFF7590, F1: 0x1FFFF7E8, H7: 0x1FF1E800, U5: 0x0BFA0700). Use the macro, not a hard-coded
address. Flash size (`FLASHSIZE_BASE`) and package (`PACKAGE_BASE`) registers sit nearby.

## Formatting
- Hex string of all 96 bits (24 chars) for logs and provisioning databases.
- Shorter: hash (CRC32 or SHA-256 truncated) for a 32/64-bit ID; collisions possible with
  CRC32 across large fleets, so prefer 64+ bits.
- USB serial number string: ST's USB library builds it from the UID (`Get_SerialNum()` in
  `usbd_desc.c`) using `w0 + w2` and `w1`: two units can theoretically collide; use all 96 bits if
  host-side uniqueness matters.
- MAC addresses for Ethernet/BLE: derive a locally administered MAC (set bit 1 of the first octet)
  from a hash of the UID, or buy an OUI block / use a MAC EEPROM.

## Not a secret
The UID is readable by anyone with debug access or code execution and is predictable in
structure. Use it as an identifier or a key-derivation **input** together with a secret (e.g.
HMAC(secret, UID) for per-device keys), never as a key or password by itself. Firmware cloning
checks based on UID only are trivial to patch out.

## Debugger read
```bash
STM32_Programmer_CLI -c port=SWD -r32 0x1FFF7590 3     # L4 address
```
On RDP level 1 parts the UID is still readable by the debugger (system memory region).

## Verify
- [ ] Serial format documented and identical in firmware, production tool and database.
- [ ] UID read in production test matches the value reported by firmware.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
