---
id: computing-software.firmware-embedded-development.zephyr.retained-memory-and-boot-mode
name: retained-memory-and-boot-mode
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [retained-mem, retention-subsystem, boot-mode, bootloader-entry, noinit-ram, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Keep data across warm resets in Zephyr with retained_mem drivers and the retention subsystem, and use boot mode to tell MCUboot or the app to enter recovery."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/storage/retention/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/retention/zephyr,retention.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/retention/retention.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/retention/bootmode.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/retention/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retained memory and boot mode

**Use cases:** crash reason and counters across reboot, "enter bootloader/serial recovery on next
boot" flags, passing data from app to bootloader.

## Drivers (retained_mem)
Back-ends include `zephyr,retained-ram` (a reserved RAM region not cleared at boot) and SoC retention
registers (for example `nordic,nrf-gpregret`); the driver directory has several others.
```dts
/ {
    sram@2003FC00 {
        compatible = "zephyr,memory-region", "mmio-sram";
        reg = <0x2003FC00 DT_SIZE_K(1)>;
        zephyr,memory-region = "RetainedMem";
        status = "okay";
        retainedmem0: retainedmem {
            compatible = "zephyr,retained-ram";
            status = "okay";
            #address-cells = <1>;
            #size-cells = <1>;
            retention0: retention@0 {
                compatible = "zephyr,retention";
                status = "okay";
                reg = <0x0 0x100>;
                prefix = [08 04];
                checksum = <1>;            /* CRC8 */
            };
            boot_mode0: boot_mode@100 {
                compatible = "zephyr,retention";
                status = "okay";
                reg = <0x100 0x1>;
            };
        };
    };
    chosen { zephyr,boot-mode = &boot_mode0; };
};
/* shrink main sram0 so the linker doesn't use the retained region */
&sram0 { reg = <0x20000000 DT_SIZE_K(255)>; };
```

## Retention subsystem
```
CONFIG_RETAINED_MEM=y
CONFIG_RETENTION=y
```
```c
#include <zephyr/retention/retention.h>
static const struct device *ret = DEVICE_DT_GET(DT_NODELABEL(retention0));

struct crashinfo { uint32_t reason; uint32_t pc; uint32_t count; };

void save(const struct crashinfo *ci) { retention_write(ret, 0, (const uint8_t *)ci, sizeof *ci); }
bool load(struct crashinfo *ci) {
    if (retention_is_valid(ret) != 1) return false;    /* prefix + checksum check */
    return retention_read(ret, 0, (uint8_t *)ci, sizeof *ci) == 0;
}
```
The `prefix` (optional magic bytes at the front) and `checksum` (0, 1, 2 or 4 bytes: none, CRC8, CRC16, CRC32) are
optional and both count against the area's `reg` size, so the usable size is smaller (256 minus 2-byte prefix minus
1-byte checksum leaves 253). `retention_is_valid()` returns 1 if valid, 0 if not, and `-ENOTSUP` if no
prefix/checksum is configured. `retention_size()` returns the usable size.

## Boot mode
```
CONFIG_RETENTION_BOOT_MODE=y
```
```c
#include <zephyr/retention/bootmode.h>
bootmode_set(BOOT_MODE_TYPE_BOOTLOADER);
sys_reboot(SYS_REBOOT_WARM);
```
MCUboot built with `CONFIG_MCUBOOT_SERIAL=y` and `CONFIG_BOOT_SERIAL_BOOT_MODE=y` (and the same DT) enters serial
recovery when it sees the flag. The boot-mode area must be a retention node (only one usable byte is needed)
named by the `zephyr,boot-mode` chosen property. `bootmode_check(BOOT_MODE_TYPE_...)` and `bootmode_clear()`
are for the receiving side.

## Gotchas
- The retention system is for data kept while the device stays powered; the docs say it should not persist
  across power failure or during some low-power modes. Check the SoC reference manual's RAM retention per
  reset source.
- The region must be excluded from `.bss`/`.data` in **every** image that runs (bootloader and app),
  or startup code zeroes it.
- `__noinit` variables are a simpler alternative within one image, but their addresses can move between
  builds; a fixed DT region keeps one location for both bootloader and app.

## Verify
- [ ] Retained data valid after `sys_reboot(SYS_REBOOT_WARM)` on the target, invalid after a power cycle.
- [ ] Bootloader and app linker maps both exclude the region.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub (retention docs, binding, headers, subsys/retention/Kconfig,
drivers/retained_mem): devicetree layout and sizes, prefix/checksum options and their size effect, `retention_is_valid()`
return values, `CONFIG_RETENTION_BOOT_MODE`, `zephyr,boot-mode` chosen, `BOOT_MODE_TYPE_BOOTLOADER`, `bootmode_*` functions,
MCUboot options (`CONFIG_MCUBOOT_SERIAL` and `CONFIG_BOOT_SERIAL_BOOT_MODE`) and the `nordic,nrf-gpregret` driver.
Removed the unconfirmed mcumgr reset claim and the warm-reset-only statement.

Method: documentation only; no commands were run.
