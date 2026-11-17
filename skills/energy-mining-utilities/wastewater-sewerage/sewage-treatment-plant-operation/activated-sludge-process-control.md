---
id: energy-mining-utilities.wastewater-sewerage.sewage-treatment-plant-operation.activated-sludge-process-control
name: activated-sludge-process-control
category: energy-mining-utilities
field: wastewater-sewerage
product: sewage-treatment-plant-operation
tags: [wastewater-sewerage, sewage-treatment-plant-operation, activated-sludge, asp, mlss, mlvss, srt, sludge-age, mcrt, was, ras, sludge-wasting, return-activated-sludge, dissolved-oxygen, do-setpoint, aeration-control, blowers, svi, sludge-volume-index, settleability, bulking, filamentous, foaming, nocardia, nitrification, ammonia, clarifier, sludge-blanket, f-m-ratio, effluent-compliance]
level: practitioner
status: draft
description: "Control an activated sludge plant: MLSS and sludge age via wasting, DO setpoints for aeration, SVI and settleability, and reading bulking and foaming."
sources:
  - "WEF Manual of Practice 11 (Operation of Water Resource Recovery Facilities), paraphrased"
  - "Sacramento State 'Operation of Wastewater Treatment Plants' training series, concepts paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Activated sludge process control

**Goal:** keep the right amount of healthy, well-settling biomass in the aeration tanks,
with enough oxygen to remove carbon and ammonia, so the clarifiers produce compliant
effluent.

## 1. The levers you actually have
1. **Wasting (WAS)** — sets sludge age (SRT). The main long-term control.
2. **Return rate (RAS)** — keeps sludge moving from clarifiers back to aeration; controls
   blanket depth. Short-term control.
3. **Air (DO setpoint)** — oxygen for the bugs; also mixing.
Everything else (chemicals, step-feed, selectors) is secondary.

## 2. Sludge age (SRT)
SRT (days) = kg solids in aeration ÷ kg solids leaving per day (WAS + effluent solids).
- Carbon removal only: often 3–6 days.
- Nitrification (ammonia removal): typically ≥ 8–15 days, longer in cold water — nitrifiers
  grow slowly and wash out first.
Change wasting by **no more than ~10–15% per day**, then wait one to three sludge ages to
judge. Big swings are the most common self-inflicted upset.

## 3. Daily checks
- **MLSS** in aeration (and MLVSS periodically); RAS concentration.
- **Settleometer** (30-min settled volume, SSV30) → SVI = SSV30 (mL/L) × 1000 / MLSS (mg/L).
  SVI ~ 80–150 mL/g is generally healthy; > 150–200 suggests bulking.
- **DO** across the tank: typically 1.5–2.5 mg/L for nitrification; very low DO favours
  filaments, very high wastes blower energy.
- **Clarifier blanket depth** (sludge judge); rising blanket = raise RAS or fix settleability.
- Effluent ammonia, TSS, BOD/COD trends; pH and alkalinity (nitrification consumes ~7 mg
  alkalinity as CaCO3 per mg ammonia-N — low alkalinity stalls it).

## 4. Common upsets
- **Filamentous bulking** (high SVI, cloudy-stretchy floc): check DO, F/M (low loading),
  nutrient deficiency (N, P for industrial loads), septic influent. Microscope confirms
  filament type. Short term: increase RAS, targeted chlorination of RAS by experienced staff.
- **Brown stable foam** (Nocardia/Microthrix): often long SRT and grease; reduce SRT,
  remove foam from the system (don't return it via scum lines).
- **White billowy foam**: young sludge / start-up or toxic hit — reduce wasting.
- **Pin floc, turbid effluent**: over-old sludge or toxicity.
- **Rising sludge clumps in clarifier**: denitrification under the blanket — cut blanket
  time by raising RAS.
- **Ammonia breakthrough**: check DO, temperature, alkalinity/pH, recent wasting, toxic
  trade discharges.

## 5. Storm flows
High flows push solids to the clarifiers. Lower the blanket in advance (raise RAS), use
step-feed or storm-mode if available, and protect the biomass — don't lose the plant to
save an hour.

## Gotchas
- Settleometer readings depend on doing them the same way every time (same container,
  same time from sampling).
- DO probes foul and drift; clean and check against a portable meter weekly.
- Grab samples at different times of day aren't comparable — note time.

## Verify
- [ ] SRT calculated daily; wasting changes ≤ ~15%/day and logged.
- [ ] SVI, DO profile and blanket depth recorded.
- [ ] Alkalinity adequate for nitrification.
- [ ] Upset diagnosis supported by microscopy or data, not guessed.
- [ ] Effluent within permit with trend reviewed.

*Uncertain:* SRT, DO and SVI ranges are typical textbook values; plant design and permit
drive your actual targets.
