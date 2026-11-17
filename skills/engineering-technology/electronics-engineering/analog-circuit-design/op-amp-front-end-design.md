---
id: engineering-technology.electronics-engineering.analog-circuit-design.op-amp-front-end-design
name: op-amp-front-end-design
category: engineering-technology
field: electronics-engineering
product: analog-circuit-design
tags: [analog-circuit-design, op-amp, operational-amplifier, sensor-front-end, signal-conditioning, instrumentation-amplifier, noise-budget, offset, error-budget, anti-aliasing-filter, sallen-key, adc-driver, sar-adc, rail-to-rail, capacitive-load, stability, johnson-noise, single-supply, input-protection, ltspice]
level: advanced
status: gated
description: "Design an op-amp sensor front-end: gain and topology, input range, offset/noise budget, anti-alias filter, stability with capacitive loads, ADC driving."
sources:
  - "Horowitz & Hill, The Art of Electronics, 3rd ed."
  - "Jung (ed.), Op Amp Applications Handbook (Analog Devices)"
  - "Kitchin & Counts, A Designer's Guide to Instrumentation Amplifiers (Analog Devices)"
  - "Carter & Mancini, Op Amps for Everyone (Texas Instruments)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Op-amp sensor front-end — from sensor spec to ADC codes with a written error budget

**Goal:** condition a sensor signal into an ADC so that offset, gain error, noise and
bandwidth are all inside a budget you wrote down *before* choosing parts, and the
circuit is stable and survives its environment.

## 1. Write the requirements as numbers
- Sensor: signal range (min/max), source impedance, common-mode level, bandwidth.
- ADC: full-scale range, resolution, input structure (SAR with switched cap, or
  delta-sigma), sample rate.
- Accuracy target in **ADC LSBs or % of FS**, over temperature.
- Supplies available, and whether the input can see faults (ESD, miswiring, 24 V).

## 2. Pick the topology
- **Non-inverting**: high input impedance, gain 1 + Rf/Rg. Default for a single-ended
  voltage sensor.
- **Inverting / transimpedance**: current-output sensors (photodiodes): Vout = −I·Rf,
  with Cf across Rf for stability (Cf ≈ √(Cin / (2π·Rf·GBW)) as a starting point).
- **Difference amp / in-amp**: bridges, thermocouples, anything with common-mode
  voltage. An integrated in-amp beats discrete four-resistor difference amps on CMRR
  unless the resistors are a matched network (0.01 % ratio).
- Set gain so the maximum signal reaches ~80–90 % of ADC FS — headroom for tolerance
  and overrange detection.

## 3. Check input and output range
- Common-mode input range and output swing **at the actual load and supply**. "Rail
  to rail" outputs still lose tens to hundreds of mV at load; on single supply, a 0 V
  signal needs either a negative rail, an offset, or a zero-drift RRIO part that
  really reaches it.
- Single supply bias: create mid-rail with a divider *buffered* or a reference, not
  a bare high-value divider that the signal path loads.

## 4. Error budget (DC)
Referred to input, add worst-case or RSS as your spec demands:
- **Offset**: Vos × noise gain; plus Ib × source resistance (balance resistances or
  use a CMOS/JFET part with pA bias). Zero-drift (chopper) parts give µV offsets and
  nV/°C drift when DC accuracy matters.
- **Gain error**: resistor tolerance (two 0.1 % resistors → up to 0.2 % gain error)
  and tempco mismatch (use same-type, same-package parts or arrays).
- **Reference error** of the ADC — often the biggest term; budget it.
Calibrate out what is stable (initial offset/gain); budget what is not (drift, noise).

## 5. Noise budget
- Contributors: op-amp voltage noise e_n × noise gain; current noise i_n × source
  impedance; resistor thermal noise √(4kTR) — **4 nV/√Hz for 1 kΩ** at room
  temperature (computed: 4.02 nV/√Hz at 293 K, 4.07 at 300 K) (scales with √R).
- Integrate over the noise bandwidth: for a single-pole filter at fc, noise BW ≈
  1.57 × fc (π/2, exact for one pole). Below a few Hz also include 1/f noise (datasheet 0.1–10 Hz p-p figure).
- Compare to the ADC: total RMS noise at the ADC input should be below ~½ LSB RMS
  if you want the ADC, not the front-end, to set resolution.
- Low R values cut thermal noise but cost power and load the op-amp: 1–10 kΩ is a
  usual compromise.

## 6. Anti-alias filter and ADC drive
- Attenuate content above Nyquist by enough to bury aliasing below your error
  budget: a 2nd-order Sallen-Key or MFB (Butterworth, Q = 0.707) is typical for SAR
  ADCs; oversampling delta-sigma ADCs relax this a lot.
- **SAR input kick**: put an RC right at the ADC pin — C large relative to the
  internal sample cap (often 10–20× (gated: unconfirmed, source is paywalled or blocked), and a C0G/NP0 part), R small enough to settle
  to ½ LSB in the acquisition time. The ADC datasheet usually gives recommended
  values; start there.
- The op-amp must drive that capacitor: add an isolation resistor (typically
  10–100 Ω) between op-amp output and the C, or choose a part rated for large
  capacitive loads. A bare op-amp into nanofarads oscillates.

## 7. Protect the input
Series resistor (1–10 kΩ) plus clamp diodes to the rails (or the part's internal
clamps if their current rating allows), TVS at the connector for ESD/surge. Check the
series R's noise and Ib × R offset contribution in the budgets above.

## 8. Simulate and verify
Simulate in LTspice with vendor models: DC operating point at both input extremes,
AC response, loop stability (phase margin ≥ 45°, ideally ≥ 60°), noise (`.noise`),
and Monte Carlo on resistor tolerances. Macromodels sometimes omit noise or input
range limits — cross-check against the datasheet.

## Verify
- [ ] Written budget shows offset, gain, noise and drift each within target over temperature.
- [ ] Input common-mode and output swing hold at both extremes on the real supply.
- [ ] Phase margin ≥ 45° with the actual capacitive load (simulated and step-tested).
- [ ] Anti-alias filter attenuation at Nyquist meets the aliasing allowance.
- [ ] ADC drive settles to ½ LSB in the acquisition time.
- [ ] Measured board noise (input shorted) is close to the predicted figure.
