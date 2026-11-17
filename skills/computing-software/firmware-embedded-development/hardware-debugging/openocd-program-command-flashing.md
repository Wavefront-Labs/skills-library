---
id: computing-software.firmware-embedded-development.hardware-debugging.openocd-program-command-flashing
name: openocd-program-command-flashing
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [openocd-program, openocd, flash-write-image, verify-image, production-flashing, option-bytes, mass-erase, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Flash firmware headlessly with OpenOCD: program with verify/reset/exit, .bin offsets, finer flash commands, unlock, option bytes and flash readback."
sources:
  - https://openocd.org/doc/html/Flash-Commands.html
  - https://openocd.org/doc/html/Flash-Programming.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flashing with the OpenOCD `program` command

## One-liner
```sh
openocd -f board/<your-board>.cfg -c "program build/app.elf verify reset exit"
# raw binary needs the flash address, and the offset comes LAST in the argument list
openocd -f board/<your-board>.cfg -c "program build/app.bin verify reset exit <flash-base-address>"
```
Syntax: `program filename [preverify] [verify] [reset] [exit] [offset]`. The manual's example for a binary is
`program filename.bin exit 0x08000000`. By default `program` does this:
1. `init`, then `reset init` (reset and halt, running any reset-init scripts).
2. `flash write_image` to erase and write.
3. With `preverify`, verify first and flash only if that fails.
4. `verify_image` if `verify` is given.
5. `reset run` if `reset` is given; shutdown if `exit` is given.

ELF, HEX and S19 images carry their addresses; binary files need the address passed.

## Finer control
```tcl
init
reset init
flash banks                           ;# lists the bank numbers used below
flash probe 0
flash erase_sector 0 0 last           ;# bank, first sector, last sector ("last" = end of bank)
flash write_image erase app.hex
flash verify_image app.hex
flash read_bank 0 readback.bin 0 <length>   ;# dump for diffing
reset run
shutdown
```
- Always issue `reset init` before flash commands, and do not issue another `reset`, `reset halt` or resume until
  programming is finished.
- `flash write_image [erase] [unlock] filename [offset] [type]`: only loadable sections are written; `type` may be
  bin, ihex, elf or s19; `offset` is added to each section's base. Warning from the manual: `erase` also erases the
  rest of any sector an image section touches, and sector "holes" between sections; an image with one byte at the start
  and one at the end of a bank erases the whole bank.
- `unlock` unlocks the flash banks before erase and program; re-apply protection afterwards if it matters.
- `flash verify_image filename [offset] [type]` uses a bank's own verify method and gives only an overall good/bad
  result, not failing addresses. The general `verify_image filename [address [bin|ihex|elf]]` tries a CRC first, then a
  binary compare.
- Other bank-number commands: `flash write_bank num file [offset]`, `flash read_bank num file [offset [length]]`,
  `flash verify_bank num file [offset]`, `flash erase_check num`, `flash info num`.
- Driver-specific commands exist, for example `stm32f2x unlock num`, `stm32f2x mass_erase num`,
  `stm32l4x option_write num reg_offset value [reg_mask]` followed by `stm32l4x option_load num` (which causes a
  system reset). For stm32f1x, `unlock` causes a mass erase if the device was locked. Read the driver section of the
  Flash Commands page for your chip.

## Speed, probes and ports
- A bank for external flash needs its own `flash bank` line with the matching driver (see the driver list).
- `adapter serial <serial_string>` selects one probe when several are attached (supported by the listed adapter
  drivers).
- `gdb port`, `tcl port` and `telnet port` accept "disabled" to turn that service off; otherwise defaults include 6666
  for tcl and 4444 for telnet. Disabling avoids port clashes when flashing several boards from one host.

## Gotchas
- Verify only compares against the image you give it, so verify the right (current) build artefact.
- `erase` in `write_image` can erase more than the image's own sectors; do not use it on flash holding data to keep.

## Verify
- [ ] The flashing script finishes without error and `verify` reported success.
- [ ] A readback from `flash read_bank` matches the release artefact.

## Checked
Method: docs-checked 2026-11-09 against the OpenOCD manual pages Flash Commands (sections 12.1-12.5 read in part: program, write_image, verify_image, bank commands, stm32 option commands) and Flash Programming (read in full), plus Server Configuration and Debug Adapter Configuration for ports and adapter serial. Corrected: the `.bin` offset belongs at the end of the `program` argument list. Removed unconfirmed claims: exit-code behaviour, adapter speed ranges, connect_assert_srst, RDP/APPROTECT blank-check notes, 0x0 alias behaviour, `** Verified OK **` log string, interface and target file names.
