---
id: engineering-technology.technical-authentication-testing.product-compliance-testing.emc-pre-compliance-and-test-planning
name: emc-pre-compliance-and-test-planning
category: engineering-technology
field: technical-authentication-testing
product: product-compliance-testing
tags: [emc, emi, pre-compliance, cispr-32, cispr-35, cispr-16, fcc-part-15, iec-61000-4-2, iec-61000-4-3, iec-61000-4-4, iec-61000-4-5, iec-61000-4-6, radiated-emissions, conducted-emissions, lisn, near-field-probe, current-probe, quasi-peak, spectrum-analyzer, esd, eft, surge, immunity, emc-test-plan, iec-62368-1, ce-marking]
level: practitioner
status: draft
description: "Pre-scan conducted/radiated emissions with LISN, near-field and current probes against CISPR 32/FCC Part 15 limits, plan CISPR 35/IEC 61000-4-x immunity, and write an accredited-lab EMC test plan."
sources: ["CISPR 32 Electromagnetic compatibility of multimedia equipment - Emission requirements", "CISPR 35 Electromagnetic compatibility of multimedia equipment - Immunity requirements", "CISPR 16-1-1 and 16-1-2 Specification for radio disturbance and immunity measuring apparatus", "47 CFR Part 15 Subpart B Unintentional Radiators", "ANSI C63.4 Methods of Measurement of Radio-Noise Emissions", "IEC 61000-4-2/-3/-4/-5/-6/-8/-11 Testing and measurement techniques", "Ott, H.W. Electromagnetic Compatibility Engineering", "IEC 62368-1 Audio/video, information and communication technology equipment - Safety requirements"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EMC pre-compliance and test planning — pass the lab on the first visit

**Goal:** find and fix emissions and immunity problems on the bench with cheap tools, then hand an accredited lab a test plan that leaves nothing to interpretation.

## 1. Identify the standards

For IT/multimedia equipment in the EU/UK: CISPR 32 (EN 55032) emissions + CISPR 35 (EN 55035) immunity + EN 61000-3-2/-3-3 harmonics/flicker for mains products; safety under IEC 62368-1 (separate test, often the same lab). US: FCC Part 15 Subpart B, measured per ANSI C63.4. Decide **Class A** (commercial/industrial) or **Class B** (residential) — Class B is about 10 dB tighter. Always check the current edition and the product-family standard (medical, automotive, industrial each differ).

## 2. Key limits (verify against the current edition)

- **Conducted, AC mains, Class B (QP/Avg dBµV):** 0.15-0.5 MHz 66→56 / 56→46 (falling with log f); 0.5-5 MHz 56/46; 5-30 MHz 60/50.
- **Radiated, Class B, 10 m QP:** 30-230 MHz 30 dBµV/m; 230-1000 MHz 37 dBµV/m. At 3 m add ~10 dB (40/47). Above 1 GHz at 3 m: 50 avg/70 peak to 3 GHz, 54/74 to 6 GHz.
- **FCC Class B at 3 m:** 40, 43.5, 46, 54 dBµV/m for 30-88, 88-216, 216-960, >960 MHz.

## 3. Bench conducted emissions

1. Product on a non-conductive table 0.4 m from a vertical ground plane (or 0.8 m above a ground plane), mains through a 50 µH/50 Ω LISN (CISPR 16-1-2) bonded to the reference ground.
2. Analyzer: 9 kHz RBW, 150 kHz-30 MHz, peak detector first. Put a **transient limiter** (10 dB pad plus limiter) between LISN and analyzer — switching transients kill front ends.
3. Measure line and neutral. Peaks within ~6 dB of the QP limit get a QP and average measurement.
4. Typical fixes: X/Y capacitors and common-mode choke sizing, snubbers on switching nodes, reducing the hot-loop area in the SMPS.

## 4. Bench radiated diagnosis

- **Near-field H-field loops** (small loop = high resolution) over switch nodes, clocks, connectors: they locate sources but do not give a far-field number.
- **RF current clamp on each cable** (120 kHz RBW, 30-1000 MHz): common-mode current is the usual radiator. Rule of thumb (Ott): about 5 µA at 100 MHz on a 1 m cable can already approach the FCC Class B limit. Compare before/after a fix in dB, not absolute.
- If you have a pre-compliance antenna in an office, measure ambient first with the product off; use relative changes.
- Common fixes: ferrites on cables, connector shield 360° bonding, spread-spectrum clocking, stitching vias, filtered I/O, edge-rate control.

## 5. Immunity plan (CISPR 35 basic levels, check current edition)

| Test | Typical residential level |
|---|---|
| IEC 61000-4-2 ESD | ±4 kV contact, ±8 kV air |
| IEC 61000-4-3 radiated | 3 V/m, 80-1000 MHz plus spot frequencies to ~6 GHz, 80% AM 1 kHz |
| IEC 61000-4-4 EFT | ±1 kV AC mains, ±0.5 kV signal ports |
| IEC 61000-4-5 surge | ±1 kV line-line, ±2 kV line-earth on AC mains |
| IEC 61000-4-6 conducted RF | 3 V, 0.15-80 MHz |
| IEC 61000-4-8 magnetic field | 1 A/m (only for magnetically sensitive equipment) |
| IEC 61000-4-11 dips/interruptions | per table |

Define **performance criteria** per function: A = normal within spec during test, B = temporary degradation self-recovering, C = operator intervention allowed. Bench ESD with a gun and a horizontal coupling plane is cheap and catches most reset issues.

## 6. Write the test plan

Include: product description and model/variants; standards and edition; class; operating modes and exercise software (worst-case emissions = max data rate, all ports loaded); configuration photo; cable types/lengths and terminations; ports list (AC, DC, signal, telecom) to drive which immunity tests apply; monitoring method and pass/fail per criterion; support equipment kept outside or characterised; highest internal frequency (sets the upper radiated scan limit); margin target (6 dB on emissions is a common internal goal).

## Gotchas

- Peak scans overestimate impulsive noise but never underestimate; QP only above a threshold saves time.
- Laptop support equipment and USB cables often emit more than the product.
- The lab's cable layout differs from yours; specify it.
- Passing on one sample with 1 dB margin is not compliance; production spread is often ±3-4 dB.

## Verify

- [ ] Correct standards, edition and Class A/B identified.
- [ ] Conducted pre-scan shows ≥6 dB QP/avg margin on line and neutral.
- [ ] Cable common-mode currents measured and reduced; worst-case mode used.
- [ ] Immunity performance criteria defined per function.
- [ ] Test plan lists configuration, cables, modes, ports and monitoring.
