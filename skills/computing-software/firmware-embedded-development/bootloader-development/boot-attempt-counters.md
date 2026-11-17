---
id: computing-software.firmware-embedded-development.bootloader-development.boot-attempt-counters
name: boot-attempt-counters
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [boot-attempt-counter, bootcount, bootlimit, altbootcmd, boot-loop-detection, rollback, rtc-backup-register, firmware-recovery, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Detect boot loops with a boot attempt counter: where to store it, incrementing in the bootloader, clearing after a health check, falling back after N attempts, U-Boot bootcount."
sources:
  - https://docs.u-boot.org/en/latest/api/bootcount.html
  - https://docs.mcuboot.com/design.html
  - https://docs.u-boot.org/en/latest/usage/environment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boot attempt counters

**Goal:** a firmware image that crashes or hangs during startup (watchdog resets, faults) is
abandoned after a few attempts instead of looping forever, and the device falls back to a
known-good image or recovery mode.

## Mechanism
1. Bootloader increments `attempts` before starting an image.
2. Application clears it only after it has proven healthy (started all tasks, connected to the
   network, passed self-test) - not at the top of `main()`.
3. If `attempts > LIMIT` at boot, the bootloader takes the fallback path: previous slot,
   recovery image, or safe mode.

## Where to store it
| Storage | Pros/cons |
|---|---|
| RTC backup registers / backup SRAM | survive resets and often power loss on VBAT, no wear - best choice |
| `.noinit` RAM (see `noinit-ram-sections`) | survives warm resets only; lost on power cycle (which is usually fine: power cycle = new attempt sequence) |
| Flash (trailer, env) | survives everything but wears; write once per boot is acceptable, use a log-structured or bit-clearing counter (program one more 0-bit per attempt without erase) |
| External EEPROM/FRAM | robust, FRAM has no wear concern |
Protect against garbage: magic word + inverted copy or CRC.

## U-Boot bootcount
```
CONFIG_BOOTCOUNT_LIMIT=y
CONFIG_BOOTCOUNT_ENV=y          # one of several storage backends (also RAM, filesystem file)
setenv bootlimit 3
setenv altbootcmd 'run boot_other_slot'
setenv upgrade_available 1      # counting only happens while this is non-zero
```
After a power-on reset `bootcount` starts at 1; while `upgrade_available` is non-zero each reboot adds 1.
Once it exceeds `bootlimit`, U-Boot runs `altbootcmd` instead of `bootcmd`. Without `bootlimit` the
feature is disabled; with no `altbootcmd` U-Boot stops at its prompt. Application code (typically
Linux userspace) must reset `bootcount` and `upgrade_available` to 0 after a successful boot.

## MCUboot
MCUboot's test/confirm flow is a one-attempt counter: a test swap that is not made permanent is
reverted at the next boot. For "N attempts" behaviour or protecting a confirmed image that later starts
crash-looping, add an application-level counter in retained RAM and trigger a revert or
recovery yourself.

## Design rules
- Count all reset causes except deliberate ones (decide whether a user-requested reboot counts).
- The watchdog must be running during early boot so hangs become resets that count.
- Log the counter value and reset cause to telemetry; a device on attempt 2 of 3 is a warning.
- After fallback, mark the bad image so it is not retried until a new update arrives.

## Verify
- [ ] Image that faults in `main()`: device falls back after exactly LIMIT attempts.
- [ ] Healthy image: counter reads 0 after each boot's health check.

## Checked

2026-10-28. Confirmed in the U-Boot bootcount page: `CONFIG_BOOTCOUNT_LIMIT`, `bootlimit`, `altbootcmd`, `upgrade_available` gating, initial value 1 after power-on reset, userspace resets the counter; `CONFIG_BOOTCOUNT_ENV` in drivers/bootcount/Kconfig; MCUboot design page for test swap and revert.
Removed: the claim that U-Boot increments on every boot (it is gated by `upgrade_available`), unconfirmed backend names, `fw_setenv` command, and the named update frameworks.

Method: documentation only; no commands were run.
