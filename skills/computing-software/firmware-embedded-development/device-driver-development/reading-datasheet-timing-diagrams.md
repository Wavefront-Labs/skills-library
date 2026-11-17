---
id: computing-software.firmware-embedded-development.device-driver-development.reading-datasheet-timing-diagrams
name: reading-datasheet-timing-diagrams
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [timing-diagram, datasheet-reading, setup-time, hold-time, spi-mode, ac-characteristics, min-max-typ, bit-banging, firmware-embedded-development]
level: practitioner
status: draft
description: "Turn a datasheet timing diagram and AC table into driver settings: setup/hold, min vs typ vs max, edge and polarity conventions, SPI mode, delays between commands, and margins."
sources:
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  - https://www.analog.com/en/resources/analog-dialogue/articles/introduction-to-spi-interface.html
  - https://www.ti.com/lit/an/scaa035b/scaa035b.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading datasheet timing diagrams

**Goal:** derive every timing value a driver needs (clock speed, mode, delays, chip-select
gaps) from the datasheet, with margin, instead of copying example code.

## Read the diagram with its table
- Each labelled arrow (tSU, tHD, tCSS, tCLH...) has a row in the **AC characteristics** table
  with min/typ/max under stated conditions (VDD, temperature, load capacitance).
- Arrow endpoints are measured at stated reference levels (e.g. 30 %/70 % VDD or 50 %);
  check the footnote, it matters at slow edges.
- Hatched/cross-hatched regions = "don't care" or "data may change"; a lens shape = valid
  data window.

## Min, typ, max
- **Design to min/max, never typ.** Typ is a characterisation average.
- For something **you** must provide (setup time before an edge, CS high time, delay after
  reset): use the **min** as your lower bound and add margin.
- For something the **device** takes (conversion time, write cycle, wake-up): wait the **max**
  or poll a ready flag.
- Blank min means 0 or unspecified - check notes.

## Translating to an SPI driver
| Datasheet | Driver setting |
|---|---|
| fSCLK max 10 MHz | prescaler giving ≤ 10 MHz at worst-case clock tree |
| data sampled on rising edge, clock idles low | CPOL=0, CPHA=0 (mode 0) |
| clock idles high, sampled on rising (second) edge | CPOL=1, CPHA=1 (mode 3) |
| tCSS (CS low to first clock) 50 ns min | GPIO CS + a few cycles, or hardware NSS delay |
| tCSH / tCS (CS high between transfers) 100 ns min | enforce gap between back-to-back transactions |
| tCONV 4 µs max after CS rises | delay or wait for DRDY before reading |
Also check **tV / tDO** (output valid after clock edge) against your MCU's input setup time:
at high SCLK, data output delay plus trace delay can exceed half a period - lower the clock or
sample late (some SPI blocks offer delayed sampling).

## I2C example
UM10204 Table 10: Fast-mode tLOW ≥ 1.3 µs, tHIGH ≥ 0.6 µs, tSU;DAT ≥ 100 ns, rise time ≤ 300
ns. A 400 kHz setting that ignores rise time with weak pull-ups violates tLOW/tHIGH; compute
pull-ups from bus capacitance.

## Bit-banged interfaces
Translate times into instruction cycles at your core clock and verify with a logic analyser;
compiler optimisation changes timing, so use cycle-counter delays.

## Verify
- [ ] Table of each timing parameter, required value, achieved value (measured) and margin.
- [ ] Logic analyser or scope measurement at min supply and worst-case clock settings.
