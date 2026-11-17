---
id: computing-software.firmware-embedded-development.hardware-debugging.oscilloscope-fft-emi-view
name: oscilloscope-fft-emi-view
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [scope-fft, fft, emi-debugging, near-field-probe, spectrum, windowing, spread-spectrum-clock, oscilloscope, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Use scope FFT to find noise and EMI sources: span/RBW from timebase, windowing, near-field probes, matching spurs to firmware clocks and PWM, and spread-spectrum fixes."
sources:
  - https://www.rohde-schwarz.com/us/applications/emi-debugging-with-oscilloscopes-application-note_56280-15740.html
  - https://www.st.com/resource/en/application_note/an1709-emc-design-guide-for-stm8-stm32-and-legacy-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scope FFT and EMI spectrum view

## Settings that matter
- **Span** = sample rate / 2. **Resolution bandwidth** ~ 1 / capture time (times the window
  factor). For 1 kHz resolution you need 1 ms of record at the chosen sample rate, so memory depth
  limits RBW.
- **Window:** Hann (general), Flat-top (accurate amplitude of a single tone), Rectangular
  (transients), Blackman-Harris (low leakage, wide dynamic range).
- Vertical in dBm or dBV; average 8-64 acquisitions to pull spurs out of noise.
- Turn off the 20 MHz bandwidth limit when looking for harmonics above it.

## Finding sources
1. Put a near-field H-field loop probe (or a short wire antenna) on the scope input, 50 ohm.
2. Sweep over the board; strongest spurs locate the source (regulator inductor, crystal, clock
   traces, SDRAM, switching MOSFETs).
3. Correlate spur frequencies with firmware: SYSCLK and its harmonics, PLL outputs, SPI/QSPI
   clocks, PWM frequency, DC-DC switching frequency, USB 12/48/480 MHz.
4. Confirm by changing firmware: disable a peripheral clock, change PWM frequency, switch the
   regulator mode; the matching spur moves or vanishes.

## Firmware mitigations
- Enable **spread-spectrum clocking** on the PLL (STM32 `RCC_SSCGR`, some nRF/NXP parts) to smear
  harmonics by several dB.
- Lower GPIO slew rate (`OSPEEDR` low speed) on pins that do not need fast edges.
- Gate clocks of unused peripherals; avoid MCO output in production.
- Pick PWM frequencies away from sensitive bands (AM radio, sensor sampling).
- DC-DC: force PWM mode instead of PFM if PFM's variable frequency lands in an audio/RF band.

## Gotchas
- Scope FFT dynamic range (~60-70 dB for 8-bit ADCs) is far below a spectrum analyser's; it finds
  sources but does not replace pre-compliance scanning.
- Aliasing in FFT: an out-of-band tone folds into the span; check by changing sample rate.

## Verify
- [ ] Each major spur is attributed to a named clock or switcher.
- [ ] The mitigation reduces the spur by a measured number of dB.
