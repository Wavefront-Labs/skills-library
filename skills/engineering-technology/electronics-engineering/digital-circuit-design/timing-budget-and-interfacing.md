---
id: engineering-technology.electronics-engineering.digital-circuit-design.timing-budget-and-interfacing
name: timing-budget-and-interfacing
category: engineering-technology
field: electronics-engineering
product: digital-circuit-design
tags: [digital-circuit-design, timing-budget, setup-time, hold-time, clock-skew, flight-time, propagation-delay, source-synchronous, common-clock, logic-levels, lvcmos, level-shifting, noise-margin, clock-distribution, fanout-buffer, series-termination, length-matching, i2c-pull-up, spi, ddr]
level: advanced
status: gated
description: "Board-level digital timing: setup/hold budgets across flight time and skew, logic-level compatibility, clock distribution, and source-synchronous interfaces."
sources:
  - "Johnson & Graham, High-Speed Digital Design: A Handbook of Black Magic"
  - "Hall & Heck, Advanced Signal Integrity for High-Speed Digital Designs"
  - "NXP, UM10204 I2C-bus specification and user manual"
  - "JEDEC JESD8 series (LVCMOS/LVTTL interface level standards)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Board-level digital timing and interfacing — make the datasheets agree on paper

**Goal:** prove, with a written budget, that every synchronous interface on the board
meets setup and hold with margin, and that every driver/receiver pair agrees on
voltage levels — before layout, then again with real trace lengths.

## 1. Logic-level compatibility (do this for every net that crosses parts)
For driver D and receiver R, both must hold:
- **VOH(D, min) ≥ VIH(R, min)** and **VOL(D, max) ≤ VIL(R, max)** — the difference is
  your noise margin; aim for ≥ 0.3–0.4 V on 3.3 V logic (rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
- Receiver absolute maximum not exceeded: a 3.3 V output into a 1.8 V-only input
  (or 5 V into a non-tolerant 3.3 V pin) needs a level translator, not a resistor
  divider (dividers kill edge rates and add RC delay).
- Watch **powered-down back-feeding**: an output driving an unpowered device's input
  through its ESD diodes can power it partly. Use parts with Ioff / partial-power-down
  specs on such boundaries.
- Translators: direction-fixed buffers (e.g. 74LVC1T45-class) for push-pull signals;
  auto-direction "open-drain friendly" parts only for I2C-like buses — the auto-sense
  types misbehave with strong push-pull loads.

## 2. Common-clock (system-synchronous) budget
Driver and receiver clocked from the same source. With Tco = clock-to-output,
Tflight = trace delay, Tskew = clock arrival at receiver minus at driver:
- **Setup**: Tclk ≥ Tco,max + Tflight,max + Tsu + jitter − Tskew
- **Hold**: Tco,min + Tflight,min ≥ Th + Tskew
Write slack = left side minus right side; want positive slack on both, and keep a
margin (10–20 % of the period is a common target (gated: unconfirmed, source is paywalled or blocked)) for things you didn't model.
- Flight time on FR-4: roughly **6–7 ps/mm** (~150–170 ps/inch; computed: √εr,eff / c gives 6.2 ps/mm at 3.4 and 6.7 ps/mm at 4.0); microstrip slightly
  faster than stripline. Use your stack's actual εr,eff.
- Common clock tops out around 100–200 MHz at board level (rule of thumb (gated: unconfirmed, source is paywalled or blocked)) because Tco and Tflight
  eat the period; above that, use source-synchronous.

## 3. Source-synchronous budget
Clock (or strobe) travels with the data, so flight time largely cancels; what matters
is **skew between clock and data** at the receiver vs the receiver's setup/hold window
and the transmitter's output skew.
- Budget: Tvalid window from transmitter − Tsu − Th − board skew − jitter > 0.
- **Length-match** clock to data within the skew allowance (e.g. ±25 ps ≈ ±4 mm, computed at 6.5 ps/mm: 3.8 mm), on the
  same layer type so velocities match.
- DDR SDRAM: follow the SoC/FPGA vendor's layout guide for byte-lane matching and
  fly-by topology; their write/read levelling calibrates residual skew, but only
  within the limits the guide states.

## 4. Clock distribution
- Point-to-point: one driver, one load. For multiple loads use a **fan-out buffer**,
  not a daisy chain, unless the topology is designed and terminated as one.
- **Series termination** at the source (Rs so Rs + Rdriver ≈ Z0; typically 22–33 Ω
  for 50 Ω lines with CMOS drivers (gated: unconfirmed, source is paywalled or blocked)) on edges whose line is "long": a common rule is
  length > rise-time / (2 × tpd) — e.g. tr = 1 ns, tpd = 6.5 ps/mm → ~77 mm (computed). Some
  authors use 1/6 of the rise time; edge rate, not clock frequency, decides.
- Keep clock traces away from board edges and I/O, with a solid reference plane and
  no layer changes without a return via.

## 5. Slow buses still have timing
- **I2C**: rise time limited by pull-up and bus capacitance: Rp,max ≈ tr / (0.8473 ×
  Cb). Standard mode tr ≤ 1000 ns, fast mode ≤ 300 ns, Cb ≤ 400 pF. Rp,min set by
  3 mA sink at VOL = 0.4 V (≈ 970 Ω at 3.3 V). All confirmed in NXP UM10204 (2021-10-01 edition) (the 0.8473·RC rise-time constant and the Rp,min = (VDD − 0.4 V) / 3 mA form appear there; 2.9 V / 3 mA = 967 Ω computed).
- **SPI**: at high SCLK the MISO path is a round trip (SCLK out → slave Tco → MISO
  back); the master's sample point must cover both flight times plus Tco — many
  "SPI works at 10 MHz, fails at 40 MHz" bugs are this.

## 6. Reset and asynchronous inputs
Asynchronous inputs to synchronous logic need a 2-flop synchroniser in the receiving
domain; reset should be asserted asynchronously and deasserted synchronously.

## Verify
- [ ] A spreadsheet lists every synchronous interface with setup and hold slack from datasheet min/max values.
- [ ] Slack recomputed with post-layout trace lengths, still positive with margin.
- [ ] VOH/VIH and VOL/VIL margins checked for every cross-part net; no abs-max violations.
- [ ] Clock nets point-to-point or buffered, source-terminated where long relative to rise time.
- [ ] I2C pull-ups give rise time within spec at measured bus capacitance.
- [ ] Scope at the receiver (not the driver) confirms clean edges and timing.
