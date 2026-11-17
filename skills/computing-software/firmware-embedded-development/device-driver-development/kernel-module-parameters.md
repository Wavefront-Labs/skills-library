---
id: computing-software.firmware-embedded-development.device-driver-development.kernel-module-parameters
name: kernel-module-parameters
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-kernel-module, module-param, module-param-array, sys-module-parameters, modprobe-d, kernel-cmdline-param, param-ops, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Expose Linux driver tunables with module_param: types, permissions and sysfs exposure, setting via modprobe.d or kernel cmdline, validation with custom param ops."
sources:
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
  - https://github.com/torvalds/linux/blob/master/include/linux/moduleparam.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel module parameters

**Goal:** driver settings (debug level, buffer sizes, quirks) that can be set at load time or
boot time without rebuilding, and validated so bad values can't crash the driver.

## Declaring
```c
static unsigned int rx_buf_kb = 64;
module_param(rx_buf_kb, uint, 0444);           /* readable in sysfs, not writable */
MODULE_PARM_DESC(rx_buf_kb, "RX buffer size in KiB (16..1024)");

static bool debug;
module_param(debug, bool, 0644);               /* root can change at runtime */

static int irqs[4]; static int n_irqs;
module_param_array(irqs, int, &n_irqs, 0444);
```
Standard types (from `moduleparam.h`): `byte`, `hexint`, `short`, `ushort`, `int`, `uint`, `long`,
`ulong`, `charp`, `bool`, `invbool`. Permission `0` = not in sysfs at all.

## Setting values
- Load time: `modprobe mydrv rx_buf_kb=128 debug=1`, or persist in
  `/etc/modprobe.d/mydrv.conf`: `options mydrv rx_buf_kb=128`.
- Kernel command line with a module name prefix: `mydrv.rx_buf_kb=128` (built-in drivers, and
  modules loaded later; modprobe reads the options from the command line).
- Runtime (if writable): `echo 1 > /sys/module/mydrv/parameters/debug`.
- `modinfo -p mydrv.ko` lists parameters and descriptions.

## Validation
Plain `module_param` accepts any value of the type. Validate with custom ops:
```c
static int set_rx_buf(const char *val, const struct kernel_param *kp) {
    unsigned int v;
    int ret = kstrtouint(val, 0, &v);
    if (ret) return ret;
    if (v < 16 || v > 1024) return -EINVAL;
    return param_set_uint(val, kp);
}
static const struct kernel_param_ops rx_buf_ops = { .set = set_rx_buf, .get = param_get_uint };
module_param_cb(rx_buf_kb, &rx_buf_ops, &rx_buf_kb, 0444);
```

## Gotchas
- Writable parameters (0644) can change while the driver is using them; the header advises
  `kernel_param_lock()` around accesses (especially `charp`, which can be freed when it changes).
  Read once into a local; prefer 0444 for structural sizes.
- Per-device configuration belongs in **devicetree properties** or sysfs device attributes,
  not module parameters (which are global for all instances).

## Verify
- [ ] `modprobe mydrv rx_buf_kb=5` fails with -EINVAL in dmesg.
- [ ] `/sys/module/mydrv/parameters/` shows exactly the intended parameters and permissions.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/moduleparam.h: standard type list (byte, hexint, short, ushort, int, uint, long, ulong, charp, bool, invbool), perm 0 means not in sysfs, kernel_param_lock() advice for writable parameters, module_param_cb, module_param_array, param_set_uint/param_get_uint. Confirmed in Documentation/admin-guide/kernel-parameters.rst: module parameters can be given on the kernel command line with a module-name prefix or through modprobe. The statement about upstream reviewers was removed as unconfirmed.

Method: documentation only; no commands were run.
