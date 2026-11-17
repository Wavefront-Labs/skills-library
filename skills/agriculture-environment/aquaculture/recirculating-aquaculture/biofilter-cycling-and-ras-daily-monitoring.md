---
id: agriculture-environment.aquaculture.recirculating-aquaculture.biofilter-cycling-and-ras-daily-monitoring
name: biofilter-cycling-and-ras-daily-monitoring
category: agriculture-environment
field: aquaculture
product: recirculating-aquaculture
tags: [aquaculture, recirculating-aquaculture, ras, biofilter, nitrification, nitrifying-bacteria, mbbr, moving-bed, drum-filter, cycling, ammonia, tan, nitrite, nitrate, alkalinity, sodium-bicarbonate, co2-stripping, degassing, oxygen-cone, pure-oxygen, uv-sterilisation, ozone, water-exchange, aquaponics, alarms, backup-power]
level: advanced
status: draft
description: "Run a land-based RAS: cycle the biofilter before stocking, ramp feed to biofilter capacity, keep ammonia, nitrite, alkalinity, CO2 and oxygen in range, and set alarms and backups."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Biofilter cycling and RAS daily monitoring

**Goal:** a recirculating system that turns fish waste into harmless nitrate fast enough
to carry a high stocking density — and never crashes. A RAS is a life-support machine:
most catastrophic losses come from a single failure (power, pump, oxygen) with no
alarm. Ranges below are commonly used guidance for warm-water fish and salmonids —
use your species' and system designer's values.

## 1. The loop
Tank → solids removal (**drum filter** / settling / swirl separator) → **biofilter**
(MBBR, fixed bed, trickling) → **CO₂ degassing** → **oxygenation** (cone, LHO, diffusers)
→ disinfection (**UV**, sometimes ozone) → tank. Plus a small daily **water exchange**
(often ~5–10% of system volume per day, varies) to control nitrate and other build-ups.

## 2. Cycling the biofilter (before any fish)
Nitrifying bacteria convert ammonia (NH₃/NH₄⁺) → nitrite (NO₂⁻) → nitrate (NO₃⁻). They take
**~4–8 weeks** to establish at warm temperatures, longer when cold.
1. Run the system with water at operating temperature, pH ~7.0–7.5.
2. Dose an **ammonia source** (ammonium chloride or fish feed) to ~2–3 mg/L TAN.
3. Test TAN and nitrite every 1–2 days. First TAN falls while nitrite rises, then nitrite
   falls and nitrate rises.
4. Cycled when you can dose ammonia and both TAN and nitrite return to near zero within ~24 h.
5. A commercial nitrifier inoculum or media from a healthy system speeds this up.

## 3. Stocking and ramping feed
The biofilter's capacity is set by its **surface area** and how much feed goes in.
Increase daily feed in steps (e.g. ≤ ~10–20% per week), never jump. Each kg of feed produces
roughly ~30 g TAN, depending on protein — use your designer's numbers.

## 4. Daily / weekly checks (log them)
| Parameter | Typical target (verify for species) | Frequency |
|---|---|---|
| Dissolved O₂ (tank outlet) | > ~6 mg/L (salmonids higher) | continuous probe |
| Temperature | species optimum | continuous |
| TAN | < ~1–2 mg/L (unionised NH₃ < ~0.02–0.05 mg/L) | daily |
| Nitrite (NO₂-N) | < ~0.5–1 mg/L | daily |
| Nitrate (NO₃-N) | < ~100–200 mg/L (lower for sensitive species) | weekly |
| pH | ~7.0–7.8 | daily |
| Alkalinity | ~100–150 mg/L as CaCO₃ | 2–3×/week |
| CO₂ | < ~15–20 mg/L | daily/probe |
- Nitrification **consumes alkalinity** (~7 g CaCO₃ per g of TAN). Top up with sodium
  bicarbonate daily as needed — falling alkalinity stalls the biofilter and crashes pH.
- Check probes against a handheld meter weekly; calibrate O₂ and pH probes on schedule.
- Watch fish behaviour at every feed: appetite drop is the first warning.

## 5. Alarms and backup
- Alarms (phone/SMS) on: low O₂, high/low temperature, low water level, pump failure,
  power failure.
- **Backup oxygen** (bottled or liquid O₂ with diffusers that open automatically on
  power loss), **generator** with auto-start tested monthly, spare pumps.
- Write the **emergency procedure** on the wall: who is on call, what valves to open, how
  long fish survive without flow at current biomass (often minutes to an hour).

## Gotchas
- Medication (antibiotics, some formalin doses) can kill the biofilter — isolate or bypass
  per vet advice.
- Over-cleaning biofilter media or a sudden temperature/salinity change also crashes it.
- **Nitrite spike** after increasing feed = biofilter can't keep up; cut feed and raise
  exchange; chloride (salt) addition reduces nitrite toxicity for many freshwater fish.
- Off-flavour (geosmin) builds in RAS; purge fish in clean water before harvest.

## Verify
- [ ] Biofilter cycled (ammonia and nitrite to ~0 within 24 h of dosing) before stocking.
- [ ] Daily log of O₂, temperature, TAN, nitrite, pH, alkalinity, feed.
- [ ] Alarms tested this month; generator and backup oxygen proven.
- [ ] Feed increases are stepped and matched by stable TAN/nitrite.
