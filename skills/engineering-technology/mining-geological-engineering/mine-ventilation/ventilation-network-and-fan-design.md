---
id: engineering-technology.mining-geological-engineering.mine-ventilation.ventilation-network-and-fan-design
name: ventilation-network-and-fan-design
category: engineering-technology
field: mining-geological-engineering
product: mine-ventilation
tags: [mining-geological-engineering, mine-ventilation, underground-ventilation, airflow, atkinson, square-law, friction-factor, airway-resistance, shock-loss, kirchhoff, hardy-cross, ventilation-network, network-modelling, network-modeling, fan-selection, fan-curve, system-curve, fan-laws, main-fan, booster-fan, auxiliary-ventilation, methane, gas-dilution, diesel-ventilation, dpm, heat-stress, wet-bulb, autocompression, ventsim, vnetpc, ventilation-survey]
level: practitioner
status: gated
description: "Design an underground ventilation circuit: airflow demand, Atkinson's square law resistances, network solving, fan duty and gas/heat checks. Design guidance only."
sources:
  - "McPherson, Subsurface Ventilation and Environmental Engineering"
  - "Hartman, Mutmansky, Ramani and Wang, Mine Ventilation and Air Conditioning"
  - "Tien, Practical Mine Ventilation Engineering"
  - "SME Mining Engineering Handbook, ventilation chapters"
  - "US 30 CFR Parts 57 and 75 (MSHA) as an example regulatory framework"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ventilation network and fan design — airflow demand to fan duty point

**Goal:** size the airflow an underground mine needs, model the airway network to
get the fan pressure-quantity duty, and check gas, dust, diesel and heat conditions
before detailed design.

> **Safety and legal status:** this is design-calculation guidance only. Ventilation
> plans, fan installations, gas limits and monitoring are governed by the mine
> regulator (e.g. MSHA in the US, state/provincial inspectorates elsewhere) and must
> be designed, approved and signed off by qualified/licensed ventilation personnel.
> Regulatory values override every typical number below.

## 1. Airflow demand — take the largest governing case per area
- **Diesel:** a rate per kW of rated engine power, often around 0.04–0.08 m³/s per kW
  depending on jurisdiction and engine certification (0.06 m³/s/kW is a common
  figure (gated: unconfirmed, source is paywalled or blocked); US coal 30 CFR 75.325(f)-(g) instead uses each unit's approval-plate quantity, summed per section). Sum active fleet per level with a utilisation factor.
- **Gas dilution:** `Q = q_gas / (C_limit − C_intake)`. 0.1 m³/s CH₄ to stay below a
  1% design concentration with clean intake → Q ≥ 10 m³/s (add a peak factor). Methane
  is explosive at ~5–15% in air (gated: unconfirmed, source is paywalled or blocked). US coal rule 30 CFR 75.323: at 1.0% CH4 in a working place or intake, electrical equipment is deenergized; at 1.5% persons are withdrawn and power disconnected (eCFR checked).
- **Minimum velocity** in working places (often ~0.25–0.5 m/s (gated: unconfirmed, source is paywalled or blocked); 30 CFR 57.8520 sets no minimum velocity or quantity, only a ventilation plan) for dust and gas layering.
- **Blasting fumes re-entry** time and **heat** (section 4).
- Add leakage: real circuits lose a large share (commonly 20–50% (gated: unconfirmed, source is paywalled or blocked)) through stoppings,
  doors and old workings; measure rather than assume.

## 2. Airway resistance — Atkinson's square law
```
p = R·Q²           (Pa, m³/s)
R = k·C·L / A³     (N·s²/m⁸)   k friction factor (kg/m³) at ρ = 1.2 kg/m³
```
Typical k (gated: unconfirmed, source is paywalled or blocked): smooth concrete-lined ~0.004, shotcreted ~0.005–0.006, unlined rectangular
drift ~0.012, irregular/supported ~0.014–0.02. Scale k by ρ/1.2 at depth.
Example (recomputed, R = 0.01536, p = 153.6 Pa; fan-law 1.1^3 = 1.331): 5 × 5 m drift, 1000 m, k = 0.012 → R = 0.012 × 20 × 1000 / 15 625 ≈ 0.0154;
at 100 m³/s (4 m/s), p ≈ 154 Pa. Add **shock losses** at bends, junctions and
regulators as `p = X·ρ·v²/2` or as equivalent length.
- Series: R = ΣRi. Parallel: 1/√R = Σ 1/√Ri.

Typical maximum velocities (McPherson-style guidance (gated: unconfirmed, source is paywalled or blocked), check local rules): working
faces ~4 m/s, conveyor drifts ~5, haulage ~6, hoisting shafts ~10, ventilation-only
shafts ~20 m/s.

## 3. Solve the network and pick the fan
- Build the network (nodes = junctions, branches = airways with R, fixed-quantity
  branches for regulators). Solve with Kirchhoff's laws via Hardy Cross iteration —
  in practice with Ventsim, VnetPC or similar.
- Calibrate against a **pressure-quantity survey** of the existing mine (aim within
  ~10% on main branches (gated: unconfirmed, source is paywalled or blocked)) before trusting future-phase models.
- **Fan duty:** intersection of the mine system curve (p = R_eq·Q² plus natural
  ventilation pressure, which can aid or oppose and changes seasonally) with the fan
  curve. Select so the duty sits on the stable side of the curve, away from stall.
- Power: air power = p·Q; shaft power = p·Q/η (η often 0.7–0.85 (gated: unconfirmed, source is paywalled or blocked)).
  Fan laws: Q ∝ N, p ∝ N²·ρ, power ∝ N³·ρ — a 10% speed increase costs ~33% more power.

## 4. Heat check
- Autocompression heats descending air by roughly 1 °C dry-bulb per 100 m of depth
  (less in wet-bulb terms; gated: unconfirmed, source is paywalled or blocked); add rock, diesel and electrical heat loads.
- Many regulators/sites set action levels around 27–28 °C wet-bulb (gated: unconfirmed, source is paywalled or blocked) (or use a heat-stress
  index); above that plan refrigeration or bulk air cooling. Confirm the governing limit.

## Gotchas
- Booster fans in series with mains can cause recirculation if mis-sized; model every
  fan combination and failure case.
- Auxiliary duct leakage can halve face airflow on long ducts; size from the delivered,
  not fan, quantity.
- Density differences and natural ventilation pressure can reverse flow in shafts
  during fan stoppages.
- Model results are only as good as the survey; stale R values mislead.
- Emergency (fire, escape route, refuge) scenarios must be modelled, not only normal operation.

## Verify
- [ ] Airflow demand computed for diesel, gas, dust, heat and minimum velocity; the maximum governs.
- [ ] Network calibrated to a pressure-quantity survey.
- [ ] Fan duty point stable, with margin for future phases and natural ventilation.
- [ ] Velocity, gas concentration and wet-bulb checked against regulatory limits.
- [ ] Plan reviewed and signed off by licensed ventilation personnel under the mine regulator's rules.
