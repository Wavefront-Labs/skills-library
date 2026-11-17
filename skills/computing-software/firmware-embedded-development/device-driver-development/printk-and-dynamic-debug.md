---
id: computing-software.firmware-embedded-development.device-driver-development.printk-and-dynamic-debug
name: printk-and-dynamic-debug
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-kernel-module, dynamic-debug, printk, dev-dbg, pr-fmt, loglevel, dyndbg-control, ratelimit, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Log from Linux drivers properly: dev_* helpers, log levels, pr_fmt, rate limiting, and enabling dev_dbg at runtime or boot with dynamic debug."
sources:
  - https://docs.kernel.org/admin-guide/dynamic-debug-howto.html
  - https://docs.kernel.org/core-api/printk-basics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# printk and dynamic debug

**Goal:** driver logs that identify the device, cost nothing when disabled, and can be turned
on in the field without rebuilding.

## Use the device-aware helpers
```c
dev_err(&pdev->dev, "reset timeout after %d ms\n", ms);
dev_warn_once(dev, "firmware too old, using fallback\n");
dev_info(dev, "probed, rev %u\n", rev);
dev_dbg(dev, "irq status 0x%08x\n", st);
dev_err_probe(dev, ret, "failed to get clock\n");  /* quiet on -EPROBE_DEFER */
```
Messages get prefixed with driver and device name (`mydrv 1-0044: ...`). Without a device,
use `pr_err`/`pr_info` with
`#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt` before includes.

## Levels and the console
`dmesg` shows everything in the ring buffer; the **console** only prints messages more
important than `console_loglevel` (`cat /proc/sys/kernel/printk`; write a level there or set
`loglevel=` on the command line).
Keep chatty messages in hot paths at `dev_dbg`, since console output is slow.

## Rate limiting
In interrupt or error paths that can repeat: `dev_err_ratelimited`, `pr_warn_ratelimited`, or
`*_once`. Otherwise a stuck interrupt floods the log and the CPU.

## Dynamic debug
With `CONFIG_DYNAMIC_DEBUG=y`, every `dev_dbg`/`pr_debug` is compiled in but disabled, and can be
toggled per file, function, line or module:
```
mount -t debugfs none /sys/kernel/debug   # if not mounted
echo 'module mydrv +p' > /sys/kernel/debug/dynamic_debug/control
echo 'file mydrv_irq.c line 120-180 +pflt' > /sys/kernel/debug/dynamic_debug/control
cat /sys/kernel/debug/dynamic_debug/control | grep mydrv    # list call sites, =p means enabled
```
Flags: `p` print, `f` function name, `l` line number, `m` module name, `t` thread ID. At boot:
`dyndbg="module mydrv +p"` on the cmdline, or `mydrv.dyndbg=+p` (the module name is stripped and
the query must not name the module) / modprobe option `options mydrv dyndbg=+p`.
Without dynamic debug, `dev_dbg` compiles only if `DEBUG` is defined for that file
(`ccflags-y += -DDEBUG` in the Kbuild).

## Gotchas
- Missing `\n` at the end merges the next message onto the same line (continuation).
- `%p` prints hashed pointers by design; use `%px` only when you truly need raw addresses.
- Use the printk format specifiers for kernel types: `%pe` for error pointers, `%pOF` for DT
  nodes, `%*ph` for small hex dumps.

## Verify
- [ ] Enabling dynamic debug for the module produces the expected `dev_dbg` lines with no rebuild.
- [ ] Error paths that can repeat are rate-limited.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/admin-guide/dynamic-debug-howto.rst: control file under /proc/dynamic_debug and, with debugfs, under /sys/kernel/debug/dynamic_debug/control; query keywords file, line (ranges), module, func; flags p, t, m, f, l; =p marks enabled call sites; dyndbg="QUERY" and module.dyndbg="QUERY" on the command line; options foo dyndbg=+pt for modprobe; -DDEBUG compile flag. Confirmed in Documentation/core-api/printk-basics.rst: console_loglevel and /proc/sys/kernel/printk, pr_fmt. Confirmed in include/linux/dev_printk.h: dev_warn_once, dev_*_ratelimited, dev_err_probe. Confirmed in Documentation/core-api/printk-formats.rst: %p hashed, %px, %pe, %pOF, %*ph. Confirmed in admin-guide/kernel-parameters.txt: loglevel= and dyndbg. Removed the specific "115200 serial console stalls the system" claim.

Method: documentation only; no commands were run.
