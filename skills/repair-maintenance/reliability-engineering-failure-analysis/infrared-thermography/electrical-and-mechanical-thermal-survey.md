---
id: repair-maintenance.reliability-engineering-failure-analysis.infrared-thermography.electrical-and-mechanical-thermal-survey
name: electrical-and-mechanical-thermal-survey
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: infrared-thermography
tags: [infrared-thermography, thermography, thermal-imaging, ir-camera, flir, condition-monitoring, predictive-maintenance, electrical-survey, switchboard, mcc, emissivity, reflected-temperature, delta-t, nfpa-70b, neta-mts, severity-criteria, load-correction, ir-window, arc-flash, mechanical-hot-spots, bearings, couplings, steam-traps, thermal-report]
level: practitioner
status: draft
description: "Run a thermal imaging survey of electrical panels and rotating plant: safe access, emissivity and reflected temperature, load conditions, delta-T severity grading and an actionable report."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Electrical and mechanical thermal survey

**Goal:** find loose connections, overloaded or unbalanced circuits, failing bearings
and other heat-producing faults with an IR camera, grade them consistently and
report them so they get fixed before they fail.

> Draft: severity tables differ (NETA MTS, NFPA 70B guidance, insurer criteria,
> company standards). The temperatures below are widely quoted examples — adopt one
> standard and state it in the report. Certification (e.g. Level I/II thermographer)
> matters for insurer-required surveys.

## 1. Safety and access
- Opening energised panels is **energised work**: follow your site's electrical safety
  rules (NFPA 70E / local equivalent) — arc-flash risk assessment, rated PPE, a
  qualified person opens covers, a second person present.
- Prefer **IR windows/viewing ports** fitted to critical gear so surveys don't need
  covers off (note: windows have transmission < 1 — set it in the camera).
- Never reach into a panel with the camera; keep approach boundaries.

## 2. Camera settings that matter
- **Emissivity (ε):** painted surfaces, insulation, tape, oxidised metal ≈ 0.90–0.95.
  **Bare shiny metal (bus bars, bolts, stainless) ≈ 0.05–0.3** — readings off these
  are unreliable and mostly reflections. Measure on adjacent insulation, paint, or a
  piece of electrical tape (ε ≈ 0.95) applied beforehand.
- **Reflected temperature:** set from a crumpled foil reflector reading (ε=1 setting)
  or ambient for indoor work.
- **Distance and spot size:** check the camera's measurement spot size (often 3× IFOV)
  — a small connector at 3 m may be smaller than one pixel and read low. Get closer
  or use a telephoto lens.
- **Focus** before you save — you can't fix focus later on most cameras.
- Level/span manual, narrow, around the component temperatures to see differences.
- Angle < ~45° from perpendicular to the surface.

## 3. Load conditions
- Survey under **at least 40% of rated load**, ideally normal peak. Record load
  current per phase with a clamp meter for every finding.
- Heat rises roughly with **I²**: a 15 °C rise at 50% load could be ~60 °C at full load.
  Some standards correct: ΔT_full ≈ ΔT_measured × (I_rated / I_measured)²; treat as
  approximate.
- Outdoor: wind cools (over ~5 m/s readings are unreliable), sun heats — survey
  early morning or overcast.

## 4. What to look for
**Electrical:**
- Hot connection/lug vs identical phase neighbour = high resistance (loose, corroded).
- Whole conductor warm on one phase = overload or imbalance (check currents).
- Fuse body hot vs clips hot (internal vs clip contact).
- Breakers, contactors, transformers, cable terminations, capacitors.
**Mechanical:**
- Bearings hotter than sister bearings or > ~40 °C above ambient (trend matters).
- Couplings and belts: misalignment and slippage heat.
- Motors: hot frame with cool end = cooling blocked; check fan and fins.
- Steam traps: inlet and outlet both hot = blowing through; both cold = blocked.
- Refractory and insulation: hot patches = damage.

## 5. Severity grading (example, NETA-style ΔT)
| ΔT between similar components under similar load | Action |
|---|---|
| 1–3 °C | possible deficiency — investigate next maintenance |
| 4–15 °C | probable deficiency — repair as time permits |
| > 15 °C (similar components) / 21–40 °C over ambient | repair at next opportunity / soon |
| > 15 °C over similar AND/OR > 40 °C over ambient | **major — repair immediately** |
Also check absolute temperature against the component's rating (e.g. insulation class).

## 6. Report each finding
Thermal image + matching visual photo, location/asset ID, component, max temperature,
reference temperature, ΔT, emissivity, reflected temp, distance, ambient, load
current(s), severity, recommended action. Summary table sorted by severity. After
repair, **re-image under load** to confirm the ΔT has gone.

## Gotchas
- A "cold" bus bar reading is usually low emissivity, not a healthy joint.
- Reflections of you, lights or the sun appear as hot spots — move and see if it moves.
- Surveying at 10% load on a Sunday finds almost nothing.
- Recently opened panels cool quickly; image promptly after removing covers.

## Verify
- [ ] Energised-work rules followed; covers removed by a qualified person.
- [ ] Emissivity/reflected temp set; measurements taken on high-ε surfaces.
- [ ] Load ≥ 40% and recorded with each finding.
- [ ] Severity graded against a stated standard.
- [ ] Repairs re-imaged under load and closed out.
