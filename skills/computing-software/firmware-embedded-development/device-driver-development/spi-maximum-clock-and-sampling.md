---
id: computing-software.firmware-embedded-development.device-driver-development.spi-maximum-clock-and-sampling
name: spi-maximum-clock-and-sampling
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [spi-max-clock, spi, timing-budget, round-trip-delay, signal-integrity-spi, firmware-embedded-development]
level: advanced
status: draft
description: "Work out the real maximum SPI clock from device tSU/tH/tV, MCU pin timing and round-trip trace delay, and fix MISO sampling failures at high speed."
sources:
  - https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html
  - https://www.ti.com/lit/an/slaa734a/slaa734a.pdf
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maximum SPI clock and sampling delay

The number on the peripheral's datasheet ("SPI up to 40 MHz") is a best case. The usable clock
is limited by the slowest of: the target device's max SCK, MISO valid time, and the round trip
through traces, buffers and level shifters.

## Read timing: the usual limit
On a read, the controller launches SCK, the device sees the edge after trace delay `tpd`, drives
MISO after its `tV` (output valid from clock), and the bit travels back (`tpd`). The controller
samples on the next opposite edge (half a period later in modes 0/3). Requirement:
```
tpd + tV(device) + tpd + tSU(MCU MISO setup) <= T_SCK / 2
```
Example: device tV = 15 ns, MCU tSU = 5 ns, tpd = 1 ns each way: 22 ns <= T/2 -> T >= 44 ns ->
**f <= 22 MHz**, even if both parts claim 50 MHz. Level shifters add 5-10 ns each direction;
isolators (ADuM) add 20-60 ns and often force a few MHz.

## Write timing
MOSI is launched by the controller with the clock, so it is limited by the device's tSU/tH and
skew between SCK and MOSI traces: usually less critical than reads.

## Fixes when reads fail at speed
- Lower the clock (prescaler) for reads only, if the protocol allows (flash: fast command at
  high clock, register reads slower).
- Delayed sampling: QSPI/OCTOSPI peripherals have `SSHIFT` (sample half a cycle later) and DLYB
  delay blocks; some SPI peripherals have `MASTER RX sample delay` options (e.g. NXP LPSPI
  `SAMPLE` bit, ESP32 `input_delay_ns` in `spi_device_interface_config_t`).
- Keep SCK traces short, series-terminate SCK at the source (22-33 Ohm) to kill ringing that
  creates double clocks.
- Raise GPIO output speed (`OSPEEDR`) for SCK/MOSI, but not higher than needed (EMI).

## Symptoms
- Data shifted by one bit (MSB lost or every byte doubled-by-2): sampling a bit late or early.
- Correct at room temperature, errors when hot: margin is near zero.
- Works with probe attached, fails without (probe capacitance damps ringing) or vice versa.

## Verify
- [ ] Scope SCK and MISO at the MCU pin: MISO stable for tSU before the sampling edge.
- [ ] Long-run read/compare test (known pattern) at target clock over temperature: zero errors.
