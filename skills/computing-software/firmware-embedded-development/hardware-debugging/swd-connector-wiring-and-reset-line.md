---
id: computing-software.firmware-embedded-development.hardware-debugging.swd-connector-wiring-and-reset-line
name: swd-connector-wiring-and-reset-line
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [swd-wiring, swd, cortex-debug-connector, 10-pin-swd, nreset, vtref, swdio-pull-up, series-resistor, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Wire SWD reliably: ARM 10-pin/20-pin pinouts, VTref, nRESET routing, SWDIO/SWCLK pulls and series resistors, cable length and the faults each mistake produces."
sources:
  - https://developer.arm.com/documentation/101453/0100/CoreSight-Technology/Connectors
  - https://wiki.segger.com/SWD
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SWD connector wiring and the reset line

**Goal:** a debug header that attaches first time on every board, including boards whose firmware
reconfigures the SWD pins or sleeps immediately.

## Standard connectors
ARM Cortex Debug 10-pin (1.27 mm, Samtec FTSH-105):

| Pin | Signal | Pin | Signal |
|---|---|---|---|
| 1 | VTref | 2 | SWDIO/TMS |
| 3 | GND | 4 | SWCLK/TCK |
| 5 | GND | 6 | SWO/TDO |
| 7 | KEY (no pin) | 8 | NC/TDI |
| 9 | GNDDetect | 10 | nRESET |

The 20-pin 0.1" (J-Link) header keeps VTref on pin 1, SWDIO=7, SWCLK=9, SWO=13, nRESET=15, many
grounds. Tag-Connect TC2030 maps to the 10-pin via an adapter; check the variant (with/without legs).

## Rules
- **VTref** must be the target's I/O rail, not the probe supplying power. Probes drive level
  shifters from it; 0 V on VTref = "target voltage too low" errors.
- **nRESET** goes to the MCU reset pin, not to a supervisor input that ignores it. Without nRESET
  you cannot connect-under-reset, so firmware that remaps SWD pins or enters deep sleep at boot
  locks you out until you erase via bootloader.
- Keep the reset RC (typ. 10k pull-up, 100 nF) — big caps (>1 uF) make reset edges too slow for
  probes that pulse it briefly; set `adapter srst delay`/`reset_config srst_only` accordingly.
- Pulls: SWDIO 10k-100k pull-up, SWCLK 10k pull-down per ARM recommendation; many MCUs have them
  internally (STM32: PA13 pull-up, PA14 pull-down at reset). Do not add strong external pulls that
  fight the probe.
- Optional 22-47 ohm series resistors near the MCU on SWCLK/SWDIO damp ringing on long cables.
- Keep the cable short (<15 cm for 4+ MHz). Long flying leads: drop `adapter speed` to 1000 kHz
  or lower before blaming firmware.
- Route SWO even if unused now; retrofitting trace later costs a board spin.

## Failure signatures
| Symptom | Likely wiring cause |
|---|---|
| `Error connecting DP: cannot read IDR` | SWDIO/SWCLK swapped, no GND, VTref 0 V |
| Connects at 100 kHz, fails at 4 MHz | ringing, long leads, missing ground returns |
| Attaches, then lost after `reset run` | firmware disables SWD pins; needs nRESET |
| `srst` has no effect | nRESET not connected or held by a supervisor |

## Verify
- [ ] Probe reads correct VTref (e.g. `monitor` / J-Link `VTref=3.300V`).
- [ ] Connect-under-reset works with firmware that immediately calls deep sleep.
- [ ] Attach is reliable at the production programming speed across 20 cycles.
