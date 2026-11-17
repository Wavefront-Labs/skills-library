---
id: computing-software.firmware-embedded-development.low-power-design.dc-dc-vs-ldo-selection
name: dc-dc-vs-ldo-selection
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [dc-dc-converter, ldo, buck-converter, quiescent-current, light-load-efficiency, smps, nrf-dcdcen, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Choose LDO vs buck for battery devices: quiescent current vs light-load efficiency, PFM/PWM modes, on-chip DC-DC enables (nRF DCDCEN, STM32 SMPS), and noise trade-offs."
sources:
  - https://www.ti.com/lit/an/slva079a/slva079a.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/power.html
  - https://www.st.com/resource/en/application_note/an5373-stm32u5-series-power-management-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DC-DC vs LDO selection

## The trade
- **LDO:** input current = output current + Iq. Efficiency = Vout/Vin. From a 3.0 V coin cell to
  1.8 V core: 60%. Iq of nano-power LDOs: 25-500 nA (TPS7A02, ~25 nA).
- **Buck (DC-DC):** input power = output power / efficiency (85-95% at medium load). At light load
  the switching losses and Iq (300 nA-20 uA) dominate; efficiency at 10 uA can be < 50%.
- For a device sleeping at 2 uA and active at 10 mA for 1% of the time, compare total charge per
  day for both, not peak efficiency.

## Worked example
Li-SOCl2 3.6 V, MCU at 1.8 V, active 8 mA x 1%, sleep 3 uA.
- LDO (Iq 1 uA): active input 8 mA, sleep input 4 uA -> average 0.08 + 0.004 = 84 uA.
- Buck (90% active, Iq 0.5 uA, sleep efficiency poor): active input = 8 x 1.8/(3.6 x 0.9) = 4.4 mA;
  sleep about 2.5 uA eq + 0.5 = ~3.5 uA -> average 44 + 3.5 = ~48 uA.
Buck wins when Vin >> Vout and active current matters; LDO wins when Vin ~ Vout (e.g. 1.8 V from
two AA's through a buck-boost is different again) or when sleep dominates.

## On-chip converters (firmware controls these)
- **nRF52:** `NRF_POWER->DCDCEN = 1` (REG1) after verifying the inductor is fitted; enabling it
  without the LC filter bricks power until reflashed. Saves ~30-40% active current. nRF52840 has
  REG0 (`DCDCEN0`) for high-voltage input too. Zephyr: board DTS `regulator-initial-mode`.
- **STM32U5/L4+/WB/WL SMPS:** `HAL_PWREx_ConfigSupply(PWR_SMPS_SUPPLY)`; on WB `HAL_PWREx_SMPS_*`
  with bypass in low power; must match the "SMPS" package and external inductor.
- **ESP32:** no on-chip buck; board regulators matter (AMS1117 Iq ~5 mA destroys deep sleep).

## Modes
PFM/burst mode at light load (high efficiency, variable frequency, higher ripple) vs forced PWM
(fixed frequency, low ripple, worse light-load efficiency). Some converters have a mode pin
firmware can drive: PWM during ADC/radio, PFM otherwise.

## Gotchas
- Switching ripple and harmonics couple into ADCs and radios; sample ADC with the converter in a
  quiet mode or filter well.
- Datasheet efficiency curves at the exact Vin/Vout/load; check below 100 uA explicitly.
- Regulator enable sequencing: some MCUs require DC-DC enable only after a stable supply.

## Verify
- [ ] Average current at the battery measured for both configurations on the target profile.
- [ ] ADC noise and RF sensitivity checked with the converter enabled.
