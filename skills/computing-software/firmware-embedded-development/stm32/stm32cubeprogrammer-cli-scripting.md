---
id: computing-software.firmware-embedded-development.stm32.stm32cubeprogrammer-cli-scripting
name: stm32cubeprogrammer-cli-scripting
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-programmer-cli, stm32cubeprogrammer, production-programming, multi-probe, stm32, firmware-embedded-development, cubeprogrammer-verify, flash-provisioning]
level: practitioner
status: gated
description: "Script STM32 flashing, verification, option bytes and serial numbers with STM32_Programmer_CLI over SWD, USB DFU or UART for CI, test benches and production lines."
sources:
  - https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf
  - https://www.st.com/en/development-tools/stm32cubeprog.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# STM32CubeProgrammer CLI scripting

`STM32_Programmer_CLI` (in the CubeProgrammer `bin/` folder) does everything the GUI does,
non-interactively, with exit code 0 on success.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Connect
```bash
STM32_Programmer_CLI -l                           # list ST-LINK probes (serial numbers)
STM32_Programmer_CLI -c port=SWD freq=4000 mode=UR reset=HWrst sn=0672FF485550755187034646
STM32_Programmer_CLI -c port=USB1                 # system bootloader DFU (BOOT0 high)
STM32_Programmer_CLI -c port=COM5 br=115200       # system bootloader UART
```
`mode=UR` = connect under reset (needed if firmware sleeps or remaps SWD pins). `sn=` selects a
probe when several are attached; essential on multi-board benches.

## Program, verify, run
```bash
STM32_Programmer_CLI -c port=SWD mode=UR -e all -w app.hex -v -rst
STM32_Programmer_CLI -c port=SWD -w app.bin 0x08000000 -v -s 0x08000000
STM32_Programmer_CLI -c port=SWD -w app.elf -v -hardRst
```
- `.hex`/`.elf`/`.srec` carry addresses; `.bin` needs one.
- `-v` verifies after write. `-e all` mass-erases (slow; `-e [0 3]` erases sectors).
- `-rst` software reset, `-hardRst` via NRST, `-s addr` starts execution.
- Read back: `-r32 0x08000000 0x100` (dump), `-u 0x08000000 0x10000 dump.bin` (upload to file).

## Option bytes
```bash
STM32_Programmer_CLI -c port=SWD -ob displ                     # show all
STM32_Programmer_CLI -c port=SWD -ob nBOOT0=1 nSWBOOT0=0       # boot config (L4/G4 style names)
STM32_Programmer_CLI -c port=SWD -ob RDP=0xBB                  # readout protection level 1
STM32_Programmer_CLI -c port=SWD mode=UR -ob RDP=0xAA          # back to level 0: MASS ERASE
```
Field names differ per series; take them from `-ob displ` output. **RDP=0xCC (level 2) is
permanent**: debug and option-byte changes are disabled forever. Never script it without a
deliberate guard.

## Production patterns
- **Serial number / calibration write**: build a small bin per unit and write it to a reserved
  flash page or OTP: `-w sn_000123.bin 0x080FF800` (or `-otp write ...` on parts with OTP).
- Parallel lines: one probe per fixture, each process with its own `sn=`; log probe SN, MCU
  UID (`-r32 0x1FFF7590 12` on L4, address is series-specific) and result per unit.
- External flash: add `-el <loader>.stldr` (see external-flash-loaders).
- Keep scripts strict: `set -e` (bash) or check `$LASTEXITCODE` (PowerShell) after every call;
  grep the log for "File download complete" and "Download verified successfully" as a
  second check.

## Gotchas
- Old ST-LINK firmware causes odd failures: update with STLinkUpgrade (or `-fwupgrade` in newer versions).
- `freq=` too high with long cables gives intermittent verify errors; drop to 1000-1800 kHz.
- After RDP level 1 is set, a power cycle is needed before the protection is fully active.

## Verify
- [ ] Script exits non-zero on a deliberately corrupted image (verify catches it).
- [ ] Multi-probe bench programs the right board by serial number.
- [ ] Option byte settings read back with `-ob displ` match the production spec.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
