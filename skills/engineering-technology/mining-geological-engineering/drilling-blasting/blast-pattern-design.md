---
id: engineering-technology.mining-geological-engineering.drilling-blasting.blast-pattern-design
name: blast-pattern-design
category: engineering-technology
field: mining-geological-engineering
product: drilling-blasting
tags: [mining-geological-engineering, drilling-blasting, blasting, bench-blasting, blast-design, blast-pattern, burden, spacing, stemming, subdrill, sub-drill, powder-factor, specific-charge, anfo, emulsion, langefors, konya, kuz-ram, kuznetsov, rosin-rammler, fragmentation, x50, scaled-distance, ppv, ground-vibration, airblast, overpressure, flyrock, quarry, open-pit, o-pitblast, jksimblast]
level: practitioner
status: gated
description: "Design a bench blast: burden, spacing, stemming, subdrill, powder factor, Kuz-Ram fragmentation and scaled-distance vibration checks. Design-calculation guidance only."
sources:
  - "Langefors and Kihlström, The Modern Technique of Rock Blasting"
  - "Konya and Walter, Surface Blast Design / Rock Blasting and Overbreak Control (FHWA)"
  - "Cunningham (1987, 2005), The Kuz-Ram fragmentation model"
  - "Siskind et al., USBM RI 8507, Structure Response and Damage Produced by Ground Vibration from Surface Mine Blasting"
  - "ISEE Blasters' Handbook"
  - "Jimeno, Jimeno and Carcedo, Drilling and Blasting of Rocks"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blast-pattern design — geometry, charge, fragmentation and vibration

**Goal:** produce a first-pass bench blast design whose geometry, charge and
predicted fragmentation and vibration are defensible, ready for review and field
calibration.

> **Safety and legal status:** this is design-calculation guidance only. Handling,
> loading and firing explosives must be done by licensed shotfirers/blasters under
> an approved blast plan, and every limit (vibration, airblast, exclusion zones,
> flyrock, notification) is set by the governing mine or explosives regulator and
> your site permit. Those always override the typical values below.

## 1. Burden — start from two estimates
- **Rule of thumb:** B ≈ 25–40 × hole diameter (lower end for dense, hard rock and
  low-energy explosive) (gated: unconfirmed, source is paywalled or blocked).
- **Konya (metric):** `B = 0.012·(2·SGe/SGr + 1.5)·De`, B in m, De in mm.
  115 mm ANFO (SGe 0.85) in rock SGr 2.7: B ≈ 0.012 × 2.13 × 115 ≈ 2.9 m (recomputed 2.94 m; the Konya coefficients themselves are(gated: unconfirmed, source is paywalled or blocked).
- **Langefors-Kihlström:** `Bmax = (d/33)·√(P·s / (c̄·f·S/B))` (d mm, P loading density
  kg/dm³, s weight strength relative to LFB dynamite, c̄ rock constant ≈ c + 0.05 with
  c typically ~0.4 kg/m³, f fixation factor 1 for vertical holes, S/B ≈ 1.25). Reduce for
  drilling error: practical B ≈ Bmax − (0.05 + 0.03·H).

## 2. The rest of the geometry (typical ratios, all gated: unconfirmed, source is paywalled or blocked)

| Item | Typical | Note |
|---|---|---|
| Spacing S | 1.0–1.5 B (≈1.15 B staggered) | larger S/B improves fragmentation uniformity |
| Stemming T | 0.7–1.0 B or 20–30 d | crushed angular stone ≈ d/10–d/20, not drill cuttings |
| Subdrill J | 0.2–0.5 B (≈0.3 B) | too much damages the next bench crest |
| Stiffness H/B | ≥ 3 preferred | < 2 gives poor breakage and more flyrock/airblast |
| Delay | 3–15 ms/m of burden between rows (typical, gated: unconfirmed) | check per-hole delay windows for vibration |

## 3. Charge and powder factor
- Linear charge `q = π·d²/4 · ρe` (kg/m). 115 mm, ρe 850 kg/m³ → q ≈ 8.8 kg/m.
- Worked example: H 10 m, B 3.5, S 4.0, J 1.0, T 2.8 → charge length 8.2 m,
  Q ≈ 72 kg/hole (recomputed 72.4); rock per hole 3.5 × 4.0 × 10 = 140 m³ → **powder factor ≈ 0.52 kg/m³** (recomputed 0.517).
- Surface bench blasts commonly run roughly 0.2–0.8 kg/m³ (gated: unconfirmed, source is paywalled or blocked); match target fragmentation,
  not habit. Wet holes need water-resistant product (emulsion), which changes ρe and
  energy.

## 4. Predict fragmentation (Kuz-Ram)
```
X50 (cm) = A · K^-0.8 · Q^(1/6) · (115/RWS)^(19/20)
P(<x)    = 1 − exp(−0.693·(x/X50)^n)
n = (2.2 − 14·B/d)·√((1 + S/B)/2)·(1 − W/B)·(|BCL − CCL|/L + 0.1)^0.1·(L/H)
```
A rock factor (≈ 0.8–22; ~7 medium, 10–13 hard (gated: unconfirmed, source is paywalled or blocked)), K powder factor, Q kg/hole, RWS weight
strength relative to ANFO = 100, W drilling deviation (m), L charge length, BCL/CCL
bottom/column charge lengths. Example above with A = 8 → X50 ≈ 31 cm (recomputed 31.6 with the 19/20 exponent as printed; 30.2 with 19/30).
Exponent caveat: Kuznetsov's original form is usually quoted with (115/RWS)^(19/30), but a 2020s open-journal paper (Iranian Journal of Mining Engineering, checked) prints 19/20 as above and a search summary of Cunningham's 2005 paper did the same; confirm against Cunningham 1987/2005 before use. Kuz-Ram
under-predicts fines; use a crush-zone extension (e.g. two-component models) if fines
matter for the plant.

## 5. Check vibration and airblast
- **Scaled distance** `SD = R/√W` (R m, W max charge per delay, kg).
- **PPV = K·SD^−β.** Generic screening values K ≈ 1140, β ≈ 1.6 (mm/s, m/kg^0.5(gated: unconfirmed, source is paywalled or blocked) — a
  starting point only; regress K and β from your own monitored blasts.
- Limits are frequency-dependent and jurisdictional (e.g. USBM RI 8507 curves, BS 7385,
  DIN 4150); low-frequency limits for residences are often in the 5–19 mm/s range (gated: unconfirmed, source is paywalled or blocked).
  Airblast limits are commonly around 115–134 dB(L) (gated: unconfirmed, source is paywalled or blocked). Confirm with your regulator/permit.
- To cut PPV: reduce charge per delay (decking, smaller holes), improve timing.

## Gotchas
- Front-row burden must be measured on the actual face (laser profile), not the plan;
  short burden causes flyrock.
- Drill deviation silently changes B and S; survey holes on critical blasts.
- Simultaneously firing holes within ~8 ms (gated: unconfirmed, source is paywalled or blocked) are often treated as one delay — check
  your regulator's definition.
- Dynamic water and sleep time degrade ANFO; reprime or switch products.
- Software such as O-Pitblast or JKSimBlast helps model timing, but only site
  measurement (fragmentation imaging, seismographs) calibrates it.

## Verify
- [ ] Burden cross-checked by two methods and against the measured face profile.
- [ ] Powder factor and Kuz-Ram X50 suit the downstream crusher/shovel target.
- [ ] Max charge per delay gives PPV and airblast within permit limits at the nearest receptor.
- [ ] Stemming length and material control flyrock and airblast.
- [ ] Design reviewed and fired by licensed personnel under the governing regulator's rules.
