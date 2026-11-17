---
id: computing-software.firmware-embedded-development.low-power-design.peak-current-and-battery-internal-resistance
name: peak-current-and-battery-internal-resistance
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [peak-current, battery-internal-resistance, coin-cell-pulse, brownout, bulk-capacitor, load-scheduling, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Keep pulse loads from browning out a battery device: internal resistance vs temperature and age, coin-cell pulse limits, bulk capacitor sizing, and firmware load scheduling."
sources:
  - https://www.ti.com/lit/wp/swra349/swra349.pdf
  - https://www.nordicsemi.com/Nordic-news/2017/03/coin-cell-battery-life
  - https://data.energizer.com/pdfs/lithiumcoin_appman.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Peak current and battery internal resistance

Average current sets battery life; **peak current** decides whether the device resets. Every
battery has internal resistance (Ri): `V_load = V_oc - I_peak x Ri`.

## Typical Ri
| Cell | Ri (fresh, 25 C) | Notes |
|---|---|---|
| CR2032 | 10-30 ohm, >100 ohm near end of life or at -20 C | rated for ~0.2-3 mA continuous |
| AA alkaline | 0.15-0.3 ohm | rises sharply when cold |
| AA Li-FeS2 (L91) | ~0.1-0.15 ohm | good cold performance |
| Li-SOCl2 bobbin (ER14505) | tens of ohm under pulses, passivation | needs hybrid capacitor for pulses |
| Li-ion 18650 | 0.03-0.1 ohm | rarely the problem |

Example: CR2032 with Ri = 40 ohm (cold, half used) and a 15 mA radio TX burst: drop 0.6 V, so
3.0 V becomes 2.4 V. MCU brownout at 2.7 V resets during every transmit.

## Measure the real peak
Current profiler (PPK2, Joulescope, Otii) at high sample rate around radio TX, flash erase,
sensor heater, motor start, display refresh. Also capture the supply voltage at the battery
terminals and after the regulator during the burst.

## Mitigations
- **Bulk capacitor:** supply the burst from a capacitor that the battery recharges slowly.
  `C = I x t / dV` -> 15 mA for 3 ms with 0.3 V allowed droop = 150 uF. Use low-leakage parts
  (ceramic or low-leakage tantalum/polymer); some electrolytics leak microamps, wrecking sleep.
- **Series resistor / current limit** between battery and capacitor so the cell sees only the
  averaged current.
- **Firmware scheduling:** never overlap peaks (do not erase flash during radio TX, stagger sensor
  heater and modem); reduce TX power when battery voltage is low; lower CPU clock during radio
  activity.
- **Brownout and voltage thresholds:** measure battery voltage *under load* (right after a TX
  burst), not idle, to decide when to warn about low battery.
- **Cell choice:** hybrid layer capacitors (HLC) for Li-SOCl2, or Li-MnO2 high-pulse cells.

## Gotchas
- Ri rises with age and cold, so a design that passes on the bench at 25 C with a fresh cell fails
  in winter after six months. Test with an aged cell or a series resistor that simulates Ri.
- Coin cell capacity at high pulse current is far below the datasheet number (rated at ~0.2 mA).

## Verify
- [ ] Worst-case burst at -20 C with simulated end-of-life Ri stays above brownout.
- [ ] Low-battery warning triggers on loaded voltage with margin before brownout.
