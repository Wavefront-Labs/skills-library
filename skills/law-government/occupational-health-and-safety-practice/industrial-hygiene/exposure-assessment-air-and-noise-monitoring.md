---
id: law-government.occupational-health-and-safety-practice.industrial-hygiene.exposure-assessment-air-and-noise-monitoring
name: exposure-assessment-air-and-noise-monitoring
category: law-government
field: occupational-health-and-safety-practice
product: industrial-hygiene
tags: [industrial-hygiene, occupational-health-and-safety-practice, occupational-hygiene, exposure-assessment, air-sampling, personal-sampling, breathing-zone, similar-exposure-group, seg, twa, time-weighted-average, stel, ceiling-limit, occupational-exposure-limit, oel, pel, rel, tlv, wel, eh40, coshh, niosh-methods, osha-methods, noise-monitoring, noise-dosimetry, lex-8h, action-level, hearing-conservation, local-exhaust-ventilation, lev, respirator-selection, aiha-strategy]
level: practitioner
status: gated
description: "Workplace exposure assessment: grouping workers, planning personal air and noise sampling, calculating TWA/STEL and noise dose, comparing to OELs and recommending controls."
sources: ["AIHA, A Strategy for Assessing and Managing Occupational Exposures", "NIOSH Manual of Analytical Methods (NMAM)", "HSE EH40 Workplace exposure limits; COSHH Regulations 2002 (GB)", "OSHA 29 CFR 1910.1000 (Table Z) and 1910.95 Occupational noise exposure", "UK Control of Noise at Work Regulations 2005 reg 4 (legislation.gov.uk)", "NIOSH noise topic page (cdc.gov/niosh/noise)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exposure assessment: air and noise monitoring

**Goal:** find out how much of a contaminant or noise workers actually receive, compare it
with the right limit on the right averaging basis, and turn the result into control
decisions. Models: US (OSHA PELs, NIOSH RELs, ACGIH TLVs; AIHA exposure-assessment
strategy) and GB (COSHH with EH40 workplace exposure limits; Control of Noise at Work
Regulations). Limits differ between these lists and are revised — always look up the
current value for your jurisdiction, and note which list is legally binding there.

## 1. Basic characterisation (before measuring)
- Inventory agents: safety data sheets, process by-products (welding fume, silica from cutting, solvent vapour), noise sources.
- Identify tasks, durations and controls in use.
- Group workers into **similar exposure groups (SEGs)**: same agent, task, controls, environment.
- Qualitative rating per SEG to decide where measurement is needed; don't sample what you can judge as trivially low or obviously unacceptable (control first).

## 2. Plan air sampling
| Decision | Rule of thumb |
|---|---|
| Personal vs static | Personal breathing-zone sampling for comparison with OELs; static for source identification |
| Method | Validated method for the agent (NIOSH/OSHA/MDHS): sampler, flow rate, media, minimum/maximum volume |
| Duration | Full shift (or representative periods covering most of the shift; the usual 70–80% minimum is unconfirmed (gated: unconfirmed, source is paywalled or blocked)) for 8-h TWA; 15-min for STEL |
| Sample count | Several samples per SEG (about 6–10 is a common rule (gated: unconfirmed, source is paywalled or blocked)) to estimate the distribution; a single result is a screening point |
| Worst case | For compliance screening, sample the highest-exposed worker/day |
Calibrate pumps before and after (field calibrator); a post-calibration shift beyond about ±5% invalidates or flags the sample (gated: unconfirmed, source is paywalled or blocked); the method sets the real tolerance. Include field blanks. Record task notes during sampling.

## 3. Calculate
- **8-h TWA** = Σ(Cᵢ × tᵢ) / 8 h (unsampled time counts as zero only if you know exposure was zero).
- Compare to STEL/ceiling limits on their own averaging periods.
- Mixtures with additive effects: Σ(Cᵢ / OELᵢ) ≤ 1.
- Adjust for unusual shifts (e.g. 12-h) using a recognised model if your regime allows.
- Statistics for SEGs: geometric mean and GSD; estimate the 95th percentile and compare to the OEL (AIHA practice). If the 95th percentile exceeds the OEL, the group is not acceptable even if most samples are below.

## 4. Noise
1. Survey with a sound level meter to map areas and find sources.
2. Personal **dosimetry** for representative workers over a full shift.
3. Compare in the right framework:
   - GB/EU: daily exposure L_EP,d (L_EX,8h) against lower and upper action values (80 and 85 dB(A)) and the exposure limit value (87 dB(A) taking hearing protection into account), plus peak values.
   - US OSHA: 90 dBA PEL with 5 dB exchange rate; 85 dBA action level for a hearing conservation programme. NIOSH REL is 85 dBA with 3 dB exchange — know which your dosimeter is set to.
4. Above action levels: noise control programme, hearing protection, health surveillance/audiometry, signage.

## 5. Recommend controls and report
- Hierarchy: substitution, enclosure, local exhaust ventilation (check capture velocity; GB requires periodic thorough examination of LEV), process change, then respirators (selected by assigned protection factor and **fit tested**).
- Report: purpose, SEGs, methods, calibration, results table, comparison basis, statistical conclusion, recommendations ranked, resampling interval.
- Share individual results with the workers measured (often a legal duty).

## Gotchas
- Comparing a short task sample directly with an 8-h TWA limit.
- Using the wrong OEL list for the jurisdiction.
- Dosimeter on the wrong exchange rate/threshold.
- Respirators recommended without fit testing and a programme.

## Verify
- [ ] SEGs defined and sampling targeted by qualitative rating.
- [ ] Validated method, pre/post calibration within tolerance, blanks included.
- [ ] Results compared on the correct averaging basis and limit list.
- [ ] Group statistics, not single results, drive the decision.
- [ ] Controls ranked by hierarchy; workers informed of results.
