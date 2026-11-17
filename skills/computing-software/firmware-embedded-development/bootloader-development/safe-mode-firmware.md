---
id: computing-software.firmware-embedded-development.bootloader-development.safe-mode-firmware
name: safe-mode-firmware
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [safe-mode, recovery-mode, reset-loop-detection, minimal-firmware, degraded-operation, firmware-embedded-development]
level: advanced
status: draft
description: "Add a safe mode that breaks crash/reset loops: count consecutive abnormal resets, boot with minimal subsystems, keep the update path and diagnostics alive, and exit cleanly."
sources:
  - https://interrupt.memfault.com/blog/firmware-watchdog-best-practices
  - https://docs.zephyrproject.org/latest/services/retention/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe mode firmware

When the application crashes during startup (bad configuration in flash, a sensor that hangs the
I2C bus, corrupted file system), the device reset-loops forever and never reaches the code that
could fix it. Safe mode is a deliberately minimal way to boot that keeps the device reachable.

## Detecting a reset loop
```c
__attribute__((section(".noinit"))) struct { uint32_t magic, crash_count; } g_bootinfo;

void early_boot(void) {
    if (g_bootinfo.magic != BOOTINFO_MAGIC) { g_bootinfo.magic = BOOTINFO_MAGIC; g_bootinfo.crash_count = 0; }
    if (reset_was_abnormal())                   /* watchdog, HardFault/assert reset, lockup; not power-on or user reset */
        g_bootinfo.crash_count++;
    if (g_bootinfo.crash_count >= 3) enter_safe_mode();
}
void mark_boot_healthy(void) { g_bootinfo.crash_count = 0; }   /* after N minutes of normal operation */
```
Use the vendor reset-cause register (RCC_CSR, RESETREAS) plus a software reason recorded before
deliberate resets. Backup registers survive more reset types than SRAM.

## What safe mode does
- Skips optional subsystems: sensors, user configuration, scripting, non-essential tasks, file
  systems that may be corrupt (or mounts read-only).
- Uses compiled-in default configuration, ignoring settings stored in flash.
- Keeps alive: watchdog, minimal connectivity (or the local service port), the **update path**,
  crash log upload, and a way to reset configuration to factory defaults.
- Signals clearly: LED pattern, status field in telemetry ("safe_mode": reason), log message.

## Implementation options
- A flag in the main application that changes init (cheapest; shares code with the failing app, so
  a crash in common code still loops: count safe-mode crashes too and fall back to the bootloader's
  update mode).
- A separate minimal image (recovery image or golden image) selected by the bootloader.

## Exit
- Remote command after the issue is fixed (configuration reset, update applied), or automatic
  after a successful update, or a timeout with retry of normal mode (with backoff so a persistent
  fault doesn't bounce forever).

## Verify
- [ ] Inject a crash in normal init: after 3 resets the device enters safe mode and is reachable for updates.
- [ ] A crash inside safe mode falls back to the bootloader's update mode, never an infinite loop.
- [ ] Power-on resets and user resets don't count toward the threshold.
