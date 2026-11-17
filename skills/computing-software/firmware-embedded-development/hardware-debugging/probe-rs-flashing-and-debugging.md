---
id: computing-software.firmware-embedded-development.hardware-debugging.probe-rs-flashing-and-debugging
name: probe-rs-flashing-and-debugging
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [probe-rs, cargo-flash, cargo-embed, defmt, rtt, dap-server, rust-embedded, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use probe-rs to flash, run and debug Cortex-M/RISC-V: probe-rs run as cargo runner, defmt over RTT, chip names, attach, DAP server for VS Code."
sources:
  - https://probe.rs/docs/tools/probe-rs/
  - https://probe.rs/docs/tools/debugger/
  - https://raw.githubusercontent.com/probe-rs/probe-rs/master/README.md
  - https://defmt.ferrous-systems.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# probe-rs

A Rust-native debug toolkit that drives CMSIS-DAP (DAPLink), ST-LINK, J-Link, FTDI probes, ESP32
USB-JTAG, WLink and Blackmagic probes directly (no OpenOCD/GDB server needed). It talks to ARM,
RISC-V and Xtensa cores over SWD or JTAG, and flashes ELF, BIN and IHEX. It works for C firmware
too; it just takes an ELF.

## Install and discover
Install a precompiled build (see the probe.rs installation guide). Then:
```sh
probe-rs list                           # attached probes
probe-rs chip list                      # supported chip names (filter with your shell)
probe-rs info --probe <VID:PID:serial>  # identify the target behind a probe
```
Pick the exact chip name from `probe-rs chip list` and pass it as `--chip`.

## Run as a cargo runner
`probe-rs run` is the recommended entry point: it flashes, resets and streams RTT/defmt output
and panics to the console. Set it once per target triple:
```toml
# .cargo/config.toml
[target.<architecture-triple>]
runner = 'probe-rs run --chip <chip-name>'
```
Then `cargo run` flashes and prints logs. `probe-rs attach` is the same but does not reset or
flash, so you can inspect a running target without changing its state.
`defmt` logs need the ELF (format strings are decoded host-side from it); see the defmt book
for the `DEFMT_LOG` filter variable.

## Debugging in VS Code
Install the probe-rs extension (alpha status at the time of reading). A `launch.json` entry uses
`"type": "probe-rs-debug"`, `chip`, an optional `probe` of the form `VID:PID:<Serial>`, and a
`coreConfigs` array whose entries carry `coreIndex`, `programBinary` and, for RTT logging,
`rttEnabled: true`. A standalone server is started with `probe-rs dap-server --port 50000`
(any free TCP port) and attached to from VS Code.

## Custom targets
Target files are generated with `target-gen` from CMSIS packs. A launch configuration can point
at one with `chipDescriptionPath`.

## Gotchas
- Two probes connected: pass the probe selector (`--probe VID:PID:serial`), otherwise a CI job
  has no way to choose.
- Logs stop after deep sleep: the debug domain is often powered down; check the vendor's
  low-power debug setting for your part.
- Server and client features (`probe-rs serve`, `--host`, `--token`) are behind the `remote`
  feature and not in the default distribution.

## Verify
- [ ] `probe-rs info` identifies the target.
- [ ] `cargo run` flashes and prints the first defmt line within seconds.

## Checked
2026-10-31. Confirmed on probe.rs (probe-rs tool page, debugger page), the probe-rs README and
the defmt book: `probe-rs run` as cargo runner, `attach` (no reset or flash), supported probes
and cores, `type: probe-rs-debug`, `coreConfigs`/`coreIndex`/`programBinary`/`rttEnabled`,
`dap-server --port 50000`, `chipDescriptionPath`, `VID:PID:<Serial>`, target-gen from CMSIS
packs, and `--probe` selection. Removed as unconfirmed: the `cargo install` command, `download`,
`erase`, `reset`, `--connect-under-reset`, `--no-location`, `--rtt-scan-memory`, `probe-rs gdb`
and its port, `--chip-description-path`, example chip names, and the RTT-placement and DBGMCU
gotchas.
Method: documentation only; no commands were run.
