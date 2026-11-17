---
id: computing-software.firmware-embedded-development.stm32.system-bootloader-dfu-recovery
name: system-bootloader-dfu-recovery
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32, system-memory-bootloader, boot0, dfu, usb-dfu, dfuse, stm32cubeprogrammer, an2606, an3156, boot-mode-selector, option-byte-boot-config, dfu-util, unbrick, firmware-embedded-development]
level: practitioner
status: gated
description: "Use STM32's factory system-memory bootloader for field recovery: BOOT0 pin strapping per AN2606, DFU/USB and UART protocols per AN3156, and STM32CubeProgrammer/dfu-util flashing."
sources:
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-an2606-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an3156-usb-dfu-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STM32 system bootloader and DFU recovery

**Goal:** use ST's factory-masked system bootloader as the last-resort
recovery path — the STM32-specific implementation of the generic concept in
`computing-software.firmware-embedded-development.bootloader-development.recovery-mode-and-unbrick-strategy`,
with the exact pins, protocols, and tools for this silicon family.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Entering the system bootloader
Every STM32 (across F0/F1/F4/H7/etc.) has a ROM-resident bootloader in system
memory, entered by the boot-mode pin combination documented in **AN2606**
("STM32 microcontroller system memory boot mode") — commonly BOOT0 held high
at reset while BOOT1 (where present) is low, selecting system memory instead
of the main flash as the boot target. The exact pin and required state
**varies by family and sometimes by specific part within a family** — don't
assume BOOT0=1 is universal without checking AN2606's per-device table; some
newer families moved boot selection into an option byte
(`nBOOT_SEL`/`nBOOT0`) rather than a physical pin, changing how you force
system-bootloader entry (via STM32CubeProgrammer's option-byte interface
instead of a strap).

## Which protocols the system bootloader speaks
AN2606 also lists which interfaces the system bootloader supports per part —
typically some combination of USART (a simple, well-documented UART-autobaud
protocol, per **AN3155**), USB DFU (per **AN3156**), I2C, SPI, or CAN,
depending on family and package. A board design intending to rely on this for
field recovery must expose whichever interface the chosen part supports —
if only USB DFU is wired out and the specific part variant doesn't support
USB DFU in its system bootloader, there's no recovery path at all; check
AN2606's table against the exact part number during PCB design, not after
units are already in the field.

## Flashing via STM32CubeProgrammer or dfu-util
- **STM32CubeProgrammer** (GUI or `STM32_Programmer_CLI`) supports both the
  UART and USB DFU system-bootloader protocols, handles unlocking/option-byte
  reads, and is ST's maintained tool — the default choice for anything beyond
  a one-off manual recovery.
- **dfu-util** (open-source, cross-platform) speaks standard USB DFU and
  works against STM32's DFU-mode system bootloader for a lighter-weight CLI
  flash, useful in a CI/scripted recovery flow without installing
  CubeProgrammer:
  ```
  dfu-util -a 0 -s 0x08000000 -D firmware.bin
  ```
  Confirm the `-a` (alt-setting/interface) and `-s` (address) values against
  `dfu-util -l`'s enumeration output for the specific part — these aren't
  universal across STM32 DFU implementations.

## Common failure: RDP already set, system bootloader refuses
If readout protection (RDP) is enabled, the system bootloader itself may
refuse to read back flash (as designed) but can often still *mass erase and
reprogram* depending on RDP level — RDP level 1 typically allows a
mass-erase-then-reflash recovery (losing existing contents, which is the
security trade-off RDP1 makes); RDP level 2 is designed to permanently
disable the debug/bootloader recovery path entirely by ST's own
documentation. This is the STM32-concrete version of the irreversibility
warning in the secure-boot and recovery-strategy skills above — confirm RDP
level before assuming any recovery is possible.

## Verify
- [ ] Boot-mode entry sequence (pin or option byte) for the exact part number was confirmed against AN2606, not assumed from another family.
- [ ] The system bootloader's supported protocol list for this exact part includes an interface actually wired out on the PCB.
- [ ] A full recovery flash (erase + reprogram via CubeProgrammer or dfu-util) was tested end to end on a production-representative board before relying on it as a field recovery plan.
- [ ] RDP level on production units was checked against whether mass-erase recovery via system bootloader is still possible at that level.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
