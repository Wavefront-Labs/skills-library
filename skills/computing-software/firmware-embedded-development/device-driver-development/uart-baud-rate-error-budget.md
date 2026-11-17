---
id: computing-software.firmware-embedded-development.device-driver-development.uart-baud-rate-error-budget
name: uart-baud-rate-error-budget
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [baud-rate-error, uart-clock-tolerance, brr, ubrr, oversampling, baud-rate-generator, rc-oscillator-accuracy, autobaud, uart-driver, firmware-embedded-development]
level: practitioner
status: draft
description: "Budget UART baud-rate error: divisor rounding, oversampling and receiver tolerance, clock source accuracy (RC vs crystal), and choosing crystals or baud rates so both ends stay within margin."
sources:
  - https://www.analog.com/en/resources/technical-articles/determining-clock-accuracy-requirements-for-uart-communications.html
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://www.st.com/resource/en/application_note/an4908-stm32-usart-automatic-baud-rate-detection-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UART baud rate error budgeting

**Goal:** two UARTs with independent clocks agree on bit timing across a whole frame under all
temperatures, with margin.

## Where the limit comes from
The receiver resyncs on the start-bit edge, then samples each bit at its centre. Timing error
accumulates until the stop bit: the stop bit sample (9.5 bit-times after the edge for 8N1)
must still fall inside the stop bit. Theoretical total mismatch limit ≈ 0.5/9.5 ≈ 5.3 %;
after sampling granularity and edge noise, budget **≤ ±2 % total**, i.e. about **±1 % per side**
when both ends are your design, or keep your own end ≤ 1 % against an unknown peer.
Longer frames (9 data bits, parity, 2 stop bits matter less) reduce the margin.

## Error sources (add them)
1. **Divisor rounding**: actual = f_clk / (oversampling × divisor).
   Example ATmega328P at 16 MHz, 115200: UBRR = 16e6/(16×115200) − 1 = 7.68 → 8 gives
   111 111 baud (−3.5 %, too much); with U2X (8× oversampling) UBRR = 16 → 117 647 (+2.1 %).
   STM32 USART has a fractional divider (BRR with 4 fraction bits at 16×): usually < 0.1 %.
2. **Clock source accuracy**: crystal ±20-50 ppm (negligible); internal RC (HSI, AVR RC) ±1-3 %
   across temperature, sometimes worse uncalibrated. RC + divisor rounding can exceed budget.
3. **The other end**: USB-UART bridges are accurate; another MCU on RC is not.

## Fixes
- Pick a "UART crystal" (7.3728, 11.0592, 14.7456, 18.432 MHz) that divides standard rates
  exactly, or a PLL setting that does.
- Use the higher oversampling (16×) for noise tolerance when the divisor allows it; 8× trades
  tolerance for higher max baud.
- Trim the RC at runtime: calibrate HSI against LSE (STM32 HSITRIM / MSI PLL-mode with LSE),
  or factory-calibrated OSCCAL.
- Autobaud detection on the receiver (STM32 `ABREN`, LIN sync break) when the peer is
  imprecise.
- Choose a lower baud rate when on RC clocks with poor divisor fit.

## Quick calculation script
```python
f, baud, os = 16e6, 115200, 16
div = round(f / (os * baud)); actual = f / (os * div)
print(div, actual, (actual / baud - 1) * 100, "%")
```

## Verify
- [ ] Measure a transmitted 0x55 byte with a scope or logic analyser: bit time within ±1 % of nominal.
- [ ] Test at temperature extremes when on an RC oscillator.
- [ ] Framing-error counter zero over a long soak against the real peer.
