---
id: engineering-technology.mechanical-engineering.heat-transfer-analysis.thermal-resistance-network
name: thermal-resistance-network
category: engineering-technology
field: mechanical-engineering
product: heat-transfer-analysis
tags: [heat-transfer, thermal-resistance, thermal-network, heat-sink, heat-sink-sizing, electronics-cooling, junction-temperature, conduction, convection, radiation, fin-efficiency, thermal-interface-material, tim, spreading-resistance, natural-convection, forced-convection, thermal-management, incropera, thermal-design]
level: practitioner
status: verified
description: "Size cooling with a thermal resistance network: junction-to-ambient budget, conduction, convection, TIM, spreading and fin efficiency for heat-sink selection."
sources: ["Incropera, DeWitt, Bergman and Lavine, Fundamentals of Heat and Mass Transfer (Wiley)", "Cengel and Ghajar, Heat and Mass Transfer: Fundamentals and Applications (McGraw-Hill)", "Kraus and Bar-Cohen, Design and Analysis of Heat Sinks (Wiley)", "JEDEC JESD51 series (thermal test methods; jedec.org returned 403, series existence unconfirmed)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thermal resistance networks — fast, honest temperature budgets

**Goal:** predict the hottest temperature in a steady-state design (typically a
semiconductor junction) to within ~10–20 %, and size the heat sink or cooling path
that keeps it below the limit with margin.

## 1. Draw the network
Treat heat flow like current: `dT = Q * R`. Series resistances add; parallel paths
combine as `1/R = sum(1/Ri)`. For a component on a heat sink:

```
Tj --R_jc--> Tcase --R_cs (TIM)--> Tsink base --R_sa--> Tambient
```

Also consider the parallel path into the PCB (often 10–30 % of the heat for surface-
mount parts (gated: unconfirmed, source is paywalled or blocked); ignoring it is conservative).

## 2. Resistance formulas
| Mode | R (K/W) |
|---|---|
| Plane wall conduction | `L / (k A)` |
| Cylindrical shell | `ln(r2/r1) / (2 pi k L)` |
| Convection | `1 / (h A)` |
| Radiation (linearised) | `1 / (h_rad A)`, `h_rad ~ 4 eps sigma Tm^3` (computed: 5.1 W/m2K at 293 K, 5.5 at 300 K, 6.1 at 310 K with eps 0.9) |
| Contact / TIM | `R''_TIM / A` (area-specific value from the datasheet at your pressure) |

Order-of-magnitude h (W/m2K): free convection in air 2–25; forced air 25–250; forced
liquid water 100–20 000; boiling/condensation higher (textbook ranges, Incropera table 1.1 style (gated: unconfirmed, source is paywalled or blocked)). Pick from a correlation (Nusselt
number for the actual geometry), not from this range, once the layout is known.

## 3. Budget the sink
Required sink-to-ambient resistance:

```
R_sa,req = (Tj,max - Ta,max) / Q - R_jc - R_cs
```

Example: Q = 25 W, Tj,max = 125 C but design to 110 C (15 K margin), Ta,max = 45 C
inside the enclosure, R_jc = 0.8 K/W, R_cs = 0.2 K/W -> R_sa,req = 65/25 - 1.0 = 1.6 K/W (computed).
Use the **worst-case** ambient (enclosure internal air, not room air) and the
**maximum** power, not typical.

## 4. Fins
Fin efficiency for a straight fin with tip correction: `eta_f = tanh(m Lc)/(m Lc)`,
`m = sqrt(h P / (k Ac))`, `Lc = L + t/2`. Array: `R_sa = 1 / (h (A_base + eta_f A_fins))`.
- Fins with `eta_f` below ~0.6–0.7 (rule of thumb (gated: unconfirmed, source is paywalled or blocked)) are too long or too thin — extra length adds mass,
  not cooling.
- Natural convection needs wide spacing (order of 6–10 mm for ~100 mm tall vertical
  fins (gated: unconfirmed, source is paywalled or blocked); check with an optimum-spacing correlation such as Bar-Cohen and Rohsenow).
  Forced air allows much tighter pitch but costs pressure drop — check the fan curve
  against the sink's pressure-drop curve.
- Orientation matters for natural convection: vertical fins, open top and bottom.

## 5. Spreading resistance
A small source on a large base heats only part of the sink. When the source is much
smaller than the base, add a spreading resistance (Lee/Song/Au or Yovanovich
closed-form approximations) or thicken the base / add a copper spreader or vapour
chamber. Ignoring it is the most common reason measured temperatures beat the
datasheet R_sa.

## 6. Gotchas
- Datasheet R_ja (JEDEC test board, still air) is a comparison figure, not a design
  value for your board.
- Heat-sink R_sa curves assume a uniform heat source over the whole base and a given
  airflow; derate for concentrated sources and real (bypassed) airflow.
- Altitude reduces air density: forced-air capacity drops roughly in proportion (mass flow scales with density); some
  standards give derating per 1000 m — check the applicable one.
- Radiation helps natural-convection designs noticeably (anodised black vs bare
  aluminium); it is negligible under strong forced air.
- Transient pulses: steady R networks are conservative; use thermal impedance Zth(t)
  curves for short pulses.

## Verify
- [ ] Network includes every series element from source to the true ambient.
- [ ] Worst-case ambient and maximum power used; margin to Tj,max stated.
- [ ] Fin efficiency computed and > ~0.7; spreading resistance assessed.
- [ ] Hand result cross-checked with a CFD or simple FEA thermal model on the final design.
- [ ] Prototype thermocouple or on-die sensor test agrees within ~10–20 %.
