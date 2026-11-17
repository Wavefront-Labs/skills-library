---
id: computing-software.firmware-embedded-development.stm32.stm32cubemonitor-live-variables
name: stm32cubemonitor-live-variables
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, stm32cubemonitor, live-variable-plot, node-red-dashboard, non-intrusive-monitoring, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Plot and log STM32 variables live without stopping the core using STM32CubeMonitor (Node-RED based): ELF import, acquisition setup, dashboards and probe sharing."
sources:
  - https://www.st.com/en/development-tools/stm32cubemonitor.html
  - https://wiki.st.com/stm32mcu/wiki/STM32CubeMonitor:STM32CubeMonitor_overview
  - https://www.st.com/resource/en/user_manual/um2593-stm32cubemonitor-software-description-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STM32CubeMonitor

CubeMonitor reads RAM through the ST-LINK while the target runs (background SWD access), so you
can plot control loop variables in real time.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Basic flow
1. Build with debug info (`-g`); globals or statics only (locals live on the stack and move).
2. Create a flow: `variables` node (import the ELF, pick variables) -> `acq out` (probe config) ->
   `acq in` -> `processing` -> `chart`/`gauge`/`write` nodes. The "Basic flow" template has this.
3. Probe config: SWD, frequency, connect mode "Hotplug" (attach without reset) or under reset.
4. Deploy, open the dashboard, Start Acquisition.

## Acquisition modes
- **Direct**: polled reads, roughly up to 1 kHz per variable depending on count and probe.
- **Snapshot** (newer versions): firmware-side buffer for higher rates (needs code support).
Sampling is not synchronous with your code: values may come from different loop iterations.
For exact time series, log into a RAM buffer in firmware and read it as an array.

## Writing variables
`write` nodes set variables (gains, setpoints) on the fly: handy for PID tuning. Make such
variables `volatile` and validate ranges in firmware.

## Sharing the probe
To debug in CubeIDE and monitor simultaneously, enable "Shared ST-LINK" in both tools (uses
the ST-LINK server).

## Logging
`processing` node can save CSV; or wire to a `file` node. Node-RED flows (`.json`) can be
committed so the team shares dashboards.

## Gotchas
- Optimised builds keep variables in registers: a variable that never changes in the plot
  probably isn't stored to RAM; make it `volatile` or global.
- Variable addresses change each build: re-import the ELF after rebuilding.
- Cortex-M7 with D-cache: debug reads see RAM, not cache; data written by the CPU may be stale
  in RAM briefly (write-back). Use write-through or non-cacheable regions for monitored variables.

## Verify
- [ ] Known test signal (sine counter) plots at expected frequency.
- [ ] Acquisition runs alongside a CubeIDE debug session when shared mode is on.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
