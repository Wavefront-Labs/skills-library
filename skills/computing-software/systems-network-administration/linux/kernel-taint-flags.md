---
id: computing-software.systems-network-administration.linux.kernel-taint-flags
name: kernel-taint-flags
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel, kernel-taint, tainted-kernel, proc-sys-kernel-tainted, oops, proprietary-module, support]
level: practitioner
status: docs-checked
description: "Decode kernel taint flags from /proc/sys/kernel/tainted and oops headers (P, O, E, W, D...), find which module tainted the kernel, and know when vendors will refuse support."
sources:
  - https://docs.kernel.org/admin-guide/tainted-kernels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading kernel taint flags

## Check
```bash
cat /proc/sys/kernel/tainted          # 0 = clean; otherwise a bitmask
# decode with the kernel's helper (in kernel source tools/debugging/kernel-chktaint) or by hand:
t=$(cat /proc/sys/kernel/tainted); for i in $(seq 0 20); do [ $(( (t>>i)&1 )) -eq 1 ] && echo "bit $i"; done
dmesg | grep -i taint
```
Oops/warn headers show letters: `CPU: 3 PID: 1 Comm: x Tainted: P  W  OE  6.8.0 ...`.

## Common flags
| Bit | Letter | Meaning |
|---|---|---|
| 0 | P | proprietary module loaded (e.g. nvidia) |
| 1 | F | module force-loaded |
| 4 | M | machine check exception happened (hardware!) |
| 5 | B | bad page referenced |
| 7 | D | kernel died recently (oops/BUG) |
| 9 | W | a WARN() fired |
| 12 | O | externally-built (out-of-tree) module loaded |
| 13 | E | unsigned module loaded |
| 14 | L | soft lockup occurred |
| 15 | K | kernel live patched |
| 17 | T | built with the struct randomization plugin |
| 18 | N | an in-kernel test has been run |
| 20 | Y | device manually bound or unbound from a driver |

## Which module?
The taint flags give the reason (proprietary, out-of-tree, unsigned); find the offending module by matching it to what you loaded (`lsmod`, `modinfo <name>` licence and signer fields) and to the first taint-setting line in `dmesg`.

## Why it matters
- Upstream and distro support commonly ask you to reproduce without P/O/E taint; check your vendor's policy.
- `D`, `W`, `M`, `B`, `L` are signals in themselves: something already went wrong since boot — check
  `journalctl -k -b` for the first event, not the latest.
- Taint is sticky until reboot; unloading the module does not clear it.

## Verify
- [ ] You can name the module and event behind every set bit before opening a vendor case.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (tainted-kernels) on 2026-10-26. Confirmed: bitmask via `/proc/sys/kernel/tainted`, bits 0-20 and their letters/meanings (the shell loop now covers bits 0-20), the `tools/debugging/kernel-chktaint` helper. Removed: the `/proc/modules` per-module letters and `/sys/module/<name>/taint` commands, which that page does not document, and the vendor-support article link.

Method: documentation only; no commands were run.
