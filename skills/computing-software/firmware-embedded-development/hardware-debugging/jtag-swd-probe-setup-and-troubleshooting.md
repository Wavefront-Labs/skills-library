---
id: computing-software.firmware-embedded-development.hardware-debugging.jtag-swd-probe-setup-and-troubleshooting
name: jtag-swd-probe-setup-and-troubleshooting
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [jtag, swd, debug-probe, openocd, cmsis-dap, cannot-attach, idcode-mismatch, srst-vs-trst, connect-under-reset, swd-multidrop, adapter-speed, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Diagnose why a JTAG/SWD probe can't attach in OpenOCD: reset_config signals, SRST vs TRST, connect_assert_srst, adapter speed and IDCODE checks."
sources:
  - https://openocd.org/doc/html/Reset-Configuration.html
  - https://openocd.org/doc/html/Debug-Adapter-Configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JTAG/SWD probe setup and troubleshooting

**Goal:** get a debug probe attached to the target with OpenOCD, and find the specific reason when
it will not attach.

## Transport
- JTAG exposes a chain of TAPs, each of which must be declared. It supports debugging and boundary
  scan.
- SWD is Arm specific, uses fewer signal wires than JTAG, exposes one declared DAP, and does not
  support boundary scan. Some processors support both.
- Select with `transport select jtag` or `transport select swd` (needed also for the `hla` and
  `st-link` drivers). `transport list` shows what the adapter and build support.
- Confirm which transport the board actually wires before blaming the target.

## SRST and TRST
- SRST (system reset) resets all chips on the adapter and behaves like pressing a reset button.
- TRST resets only the TAP controllers and should not be visible to the rest of the system.
- Common problems listed by the OpenOCD manual: the signal is not wired to the connector or not
  supported by the adapter; SRST and TRST are shorted together; reset circuitry stretches the
  reset; the drive type is wrong (open drain versus push-pull); or the target needs a special
  initialisation sequence.
- A missing TRST is not a problem because JTAG level resets can be done with TMS signalling. A
  missing SRST means startup code may not see fully reset controllers.

Commands and flags:
- `reset_config` modes: `signals` (`none` default, `trst_only`, `srst_only`, `trst_and_srst`); a
  combination (`separate` default, `srst_pulls_trst`, `trst_pulls_srst`, `combined`); gates
  (`srst_gates_jtag` default, `srst_nogate`); connect type (`connect_deassert_srst` default,
  `connect_assert_srst`); driver types `srst_open_drain` (default) or `srst_push_pull`, and
  `trst_push_pull` (default) or `trst_open_drain`. Declare connected signals or OpenOCD will not use
  them. Normally this belongs in the board config file.
- `adapter srst pulse_width <ms>` and `adapter srst delay <ms>` (and `jtag_ntrst_delay`) handle
  reset circuitry that holds the line after the adapter lets go. Reset buttons commonly have
  debouncing, so use the delay.
- With weak pull-ups it can help to drive both levels (push-pull) to shorten rise times. Drivers
  that emulate open drain (for example the GPIO based ones) need a pull-up on the reset line, or use
  `srst_push_pull`.

## Connect under reset
`reset_config connect_assert_srst` asserts SRST before any target connection. It requires
`srst_nogate`, and only some targets support it (the manual names STM32 and STR9). The manual says
it is useful when you cannot connect because of incorrect option byte configuration or illegal
program execution. Combine them, for example `reset_config srst_only srst_nogate connect_assert_srst`.

## Scan chain and IDCODE
`jtag arp_init` validates the scan chain: it issues a JTAG-only reset, then checks the observed
TAPs against the configuration, including each IDCODE and the instruction register length. A
mismatch means the config does not describe the silicon, or the connection is not clean. Use
`jtag arp_init-reset` to use TRST and SRST to reset everything on the chain first. When SRST is not
an option, provide a `reset-assert` handler for the target.

## Clock speed
- `adapter speed <kHz>` sets the maximum clock; the speed actually used will not be faster. The
  datasheet gives a top JTAG clock; the real limit often depends on the CPU clock, and most Arm cores
  accept at most one sixth of the CPU clock.
- Speed 0 selects RTCK if the adapter, board and target support it (adaptive clocking is probably the
  most robust, but adds delay). `jtag_rclk <fallback_kHz>` tries RTCK and falls back.
- If the clock changes after reset (slow at reset, program the CPU clocks, then run fast), set the
  initial speed slow with a `reset-start` handler and raise it in `reset-init`.
- Lower the adapter speed first when attach is intermittent.

## Multi-drop SWD
SW-DP v2 and SWJ-DP v2 devices support multi-drop, allowing two or more devices on one adapter.
OpenOCD uses multi-drop mode when the DAP is declared with both `-dp-id` and `-instance-id`. Only
`cmsis_dap` (CMSIS-DAP 2.0 adapters), `ftdi` and the bitbang based drivers support it.

## Target voltage
Some drivers can report target voltage (for example `jlink hwstatus` and the KitProg adapter info
command). Check it when the probe cannot see the target at all.

## Verify
- [ ] The transport and reset signals declared in the config match what the board wires.
- [ ] Attach is retried with a lower `adapter speed` and with `connect_assert_srst` where supported.
- [ ] The scan chain check passes with the expected IDCODEs.

## Checked
Confirmed from the OpenOCD Reset Configuration chapter (SRST and TRST, reset_config flags, delays,
connect_assert_srst, arp_init) and the Debug Adapter Configuration chapter (transports, multi-drop,
adapter speed, RTCK). Removed as unconfirmed: probe logging strings, pyOCD behaviour, wire length
guidance, debug port lockout and RDP claims, firmware that repurposes SWD pins, and cross-skill
references.

Method: docs-checked 2026-11-09 against the OpenOCD Reset Configuration and Debug Adapter Configuration manual pages.
