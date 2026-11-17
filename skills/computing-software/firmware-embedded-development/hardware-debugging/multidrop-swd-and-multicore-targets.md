---
id: computing-software.firmware-embedded-development.hardware-debugging.multidrop-swd-and-multicore-targets
name: multidrop-swd-and-multicore-targets
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [multidrop-swd, swd-v2, targetsel, rp2040, multicore-debug, cross-trigger, openocd-target, ap-select, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug multi-core and multidrop SWD targets with OpenOCD: SWD multi-drop adapters, -dp-id/-instance-id, -ap-num per core, -coreid, SMP groups and one GDB port per target."
sources:
  - https://openocd.org/doc/html/Debug-Adapter-Configuration.html
  - https://openocd.org/doc/html/CPU-Configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multidrop SWD and multi-core targets

## Two different things
- **Multidrop SWD:** newer SWD devices (SW-DP v2 or SWJ-DP v2) support the multi-drop extension, so
  two or more devices share one SWD adapter. In OpenOCD, SWD works in multi-drop mode whenever the
  DAP is configured with both `-dp-id` and `-instance-id`, regardless of how many DAPs exist.
- **Multi-AP:** one DAP with several Access Points, each connected to an independent core. Select
  the core with the target option `-ap-num` (on ADIv5 the numeric AP index; on ADIv6 the base
  address of the AP).

## Probe support
Not every adapter driver supports SWD multi-drop. OpenOCD documents only these as capable:
`cmsis_dap` (use an adapter with CMSIS-DAP version 2.0), `ftdi`, and all bitbang based drivers.
If a multidrop target will not enumerate, check the adapter before anything else.

## OpenOCD configuration
Declare an SWD DAP and a target on it (names are examples):
```tcl
transport select swd
swd newdap chip cpu -dp-id <dp-id> -instance-id <n>
dap create chip.dap0 -chain-position chip.cpu
target create chip.core0 cortex_m -dap chip.dap0 -coreid 0
```
- `swd newdap` takes the same parameters as `jtag newtap`. `dap create` names the DAP; a
  target must specify `-dap` (or `-tap`).
- For a second core on another AP of the same DAP: `target create chip.core1 cortex_m -dap chip.dap0 -ap-num 1`.
  Use the AP numbers from your chip's reference manual or an existing OpenOCD target file.
- Prefer the chip's shipped file under `target/` (or `find target/...`) over writing this by hand.
- `-coreid` is an index identifying the CPU or its debug controller; for several CPUs on one AP of
  types like cortex_a it selects the ROM table entry. `-dbgbase` gives the debug controller base
  and can speed up examination.
- `-gdb-port` sets a GDB port for that target only, overriding the global `gdb port`. Give each core
  its own explicit port so IDE launch configurations do not collide.

## Halting together
`target smp` defines an SMP group; with SMP handling on, halt or resume on one core halts or
resumes all in the group. With SMP handling off, treat each target individually. For separate images
per core, run one GDB per target and check how your target halts the other core; the `-cti` option
is documented only for the aarch64 target, so on Cortex-M follow the vendor's guidance.

## Gotchas
- `-defer-examine` skips target examination at the initial scan and after a reset; a manual
  `arp_examine` is then needed before debugging. Use it for a core that is not yet running or
  powered.
- Declaring the wrong number of DAPs or the wrong ids shows up as a failed scan: check the ids
  against the chip documentation.

## Verify
- [ ] `targets` lists every core with its state.
- [ ] Each GDB connects on its own port and halts only its core (or the whole SMP group if configured).

## Checked
Confirmed from the OpenOCD Debug Adapter Configuration page (SWD transport, multi-drop condition,
capable drivers, `swd newdap`) and CPU Configuration page (`target create`, `-dap`, `-ap-num`,
`-coreid`, `-dbgbase`, `-defer-examine`, `-cti`, `-gdb-port`) plus the SMP description on the
Architecture and Core Commands page. Removed as unconfirmed: RP2040 TARGETSEL ids and rescue DP,
STM32H745 and nRF5340 AP numbers and FORCEOFF register, specific probe firmware and OpenOCD version
claims, the CTI-for-Cortex-M advice, and the Arm IHI0031 and RP2040 datasheet sources (not read).

Method: docs-checked 2026-11-09 against the OpenOCD Debug Adapter Configuration, CPU Configuration and Architecture and Core Commands pages, all read.
