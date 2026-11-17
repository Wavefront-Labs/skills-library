---
id: computing-software.firmware-embedded-development.device-driver-development.debugging-kernel-oops
name: debugging-kernel-oops
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [kernel-oops, linux-kernel-module, decode-stacktrace, faddr2line, ftrace, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Decode a Linux kernel oops or panic from a driver: reading the report, decode_stacktrace.sh and faddr2line on module offsets, taint flags, and ftrace/pstore for hard cases."
sources:
  - https://docs.kernel.org/admin-guide/bug-hunting.html
  - https://docs.kernel.org/admin-guide/tainted-kernels.html
  - https://docs.kernel.org/admin-guide/ramoops.html
  - https://docs.kernel.org/trace/ftrace.html
  - https://github.com/torvalds/linux/blob/master/scripts/decode_stacktrace.sh
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging kernel oops

## Reading the report
```
Unable to handle kernel NULL pointer dereference at virtual address 0000000000000010
pc : mydrv_read+0x44/0x120 [mydrv]
lr : vfs_read+0xa8/0x2b0
Call trace:
 mydrv_read+0x44/0x120 [mydrv]
 vfs_read+0xa8/0x2b0
 ksys_read+0x70/0x100
Tainted: G           O       6.6.23 #1
```
- Fault address 0x10: NULL pointer + offset 0x10 (a struct member).
- `function+offset/size [module]`: where it happened.
- Taint letters: `O` out-of-tree module loaded, `E` unsigned, `P` proprietary, `W` a previous
  warning happened (look further up the log for the first problem), `D` died recently.

## Map offset to source line
Build the kernel and module with debug info (`CONFIG_DEBUG_INFO`).
```sh
./scripts/faddr2line drivers/mydrv/mydrv.ko mydrv_read+0x44/0x120
# mydrv_read at drivers/mydrv/mydrv.c:212
./scripts/decode_stacktrace.sh vmlinux auto <modules_path> < oops.txt   # whole trace with lines
./scripts/decode_stacktrace.sh -r <release> < oops.txt                  # finds vmlinux for a release
gdb mydrv.ko -ex 'list *(mydrv_read+0x44)'
```
For cross-compiled targets use the target `gdb`/`addr2line` (`CROSS_COMPILE=aarch64-linux-gnu-`).

## Getting the log when the system dies
- Serial console (`console=ttyS0,115200`) is the most reliable.
- `pstore`/ramoops: reserve RAM in the device tree (`ramoops` node) to keep the last oops across
  a warm reboot; mount the pstore filesystem and read the `dmesg-ramoops-N` records.
- `kdump` on larger systems; `panic_on_oops=1` + `panic=5` for automatic reboot.

## Finding the cause
- NULL derefs in callbacks often mean use-after-unbind: file operation running after `remove()`
  freed devm memory.
- "BUG: sleeping function called from invalid context" / "scheduling while atomic": sleeping under
  a spinlock or in IRQ context.
- KASAN reports give allocation and free stacks for use-after-free.
- **ftrace** to see what led up to it:
```sh
cd /sys/kernel/tracing
echo function_graph > current_tracer
echo 'mydrv_*' > set_ftrace_filter
echo 1 > tracing_on; <reproduce>; cat trace
```
- `dynamic_debug` (`echo 'module mydrv +p' > /sys/kernel/debug/dynamic_debug/control`) for
  `dev_dbg` output without rebuilding.

## Verify
- [ ] Oops location resolved to a source line; root cause reproduced and fixed.
- [ ] Re-run with KASAN, lockdep and DEBUG_ATOMIC_SLEEP: no further reports.

## Checked

2026-10-27, Linux kernel documentation and scripts (mainline v7.3).
Confirmed in bug-hunting.rst: decode_stacktrace.sh needs CONFIG_DEBUG_INFO. Confirmed in tainted-kernels.rst: P proprietary module, W warning, O externally built module, E unsigned module, D died recently (OOPS or BUG). Confirmed in scripts/decode_stacktrace.sh usage: vmlinux, base_path or auto, modules_path, and -r release. Confirmed in scripts/faddr2line: usage with an object file and func+offset. Confirmed in ramoops.rst: reserved-memory ramoops node and dmesg-ramoops-N files. Confirmed in ftrace.rst: current_tracer, function_graph, set_ftrace_filter, tracing_on. Confirmed in kasan.rst: alloc and free stack traces. Confirmed in sysctl/kernel.rst: panic_on_oops. Corrected the decode_stacktrace.sh arguments (the second argument is a base path, not the modules directory). Removed the -g ccflags tip and the fixed pstore mount path.

Method: documentation only; no commands were run.
