---
id: engineering-technology.electrical-engineering.electromagnetics.magnetic-circuit-design
name: magnetic-circuit-design
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [magnetic-circuit, reluctance, mmf, air-gap, gapped-inductor, inductor-design, transformer-design, faraday-law, flux-density, saturation, bsat, fringing, al-value, core-loss, steinmetz, ferrite, silicon-steel, powder-core, skin-effect, proximity-effect, litz, area-product, femm, finite-element, electromagnetics, air-gap-fringing, saturation-and-bh-curve]
level: advanced
status: gated
description: "Design gapped inductors and transformer cores with magnetic-circuit models: reluctance, gap sizing, fringing, Bsat margin, Faraday's law, core loss."
sources:
  - "McLyman, Transformer and Inductor Design Handbook"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics (magnetics chapters)"
  - "Hurley & Wolfle, Transformers and Inductors for Power Electronics"
  - "Hayt & Buck, Engineering Electromagnetics"
  - "Meeker, FEMM (Finite Element Method Magnetics) user's manual"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Magnetic circuit design — reluctance models for inductors and transformers

**Goal:** size turns, core and air gap so the component has the right inductance,
never saturates at peak current, and stays within its temperature rise — using the
magnetic-circuit (reluctance) analogy, then confirming with FEA or measurement.

## 1. The analogy
MMF `F = N·I` (A-turns) ↔ voltage; flux Φ (Wb) ↔ current; reluctance
`ℛ = l / (μ0 · μr · A)` ↔ resistance. Series path: `N·I = Φ · Σℛ`.
Inductance `L = N² / Σℛ`; manufacturers give `AL = L/N²` (nH/turn²) for a gapped core.
In a gapped core the gap dominates: with μr ≈ 2000, 0.5 mm of gap outweighs ~1 m of ferrite path.
So `L ≈ μ0 · N² · Ae / lg` — the inductance is set by the gap, stabilising it against
μr spread (±25% on ferrite) and temperature.

## 2. Inductor design procedure (DC-biased, e.g. a buck inductor)
1. Specs: L, Ipk, Irms, ripple ΔI, fsw, allowed temperature rise.
2. Pick Bmax: ferrite ~0.25–0.3 T (Bsat falls to roughly 0.35–0.4 T at 100 °C for
   common power grades) (gated: unconfirmed, source is paywalled or blocked); silicon steel ~1.2–1.5 T; powder cores per their roll-off curve.
3. Energy-based core size (area product): `Ap = Wa·Ae ≥ L · Ipk · Irms / (Bmax · J · Ku)`
   with J ≈ 3–5 A/mm², window fill Ku ≈ 0.3–0.4 (lower for litz/bobbins) (typical design values (gated: unconfirmed, source is paywalled or blocked)).
4. Turns: `N = L · Ipk / (Bmax · Ae)`.
5. Gap: `lg = μ0 · N² · Ae / L` (then correct for fringing).
6. Fringing increases effective gap area, raising L. McLyman's factor (gated: unconfirmed, source is paywalled or blocked) (the snippet below was run: F = 1.28 for this case, so L rises from 50 to 64 µH)
   `F = 1 + (lg/√Ae) · ln(2G/lg)` (G = window height); reduce N or open the gap to
   compensate. Fringing also heats nearby windings — keep copper ~2–3 gap lengths
   away from the gap, or distribute the gap.

Worked: L = 50 µH, Ipk = 10 A, ferrite Ae = 1.25 cm², Bmax = 0.25 T →
N = 50e-6 × 10 / (0.25 × 1.25e-4) = 16 turns; lg = 4π·10⁻⁷ × 256 × 1.25e-4 / 50e-6 ≈ 0.80 mm
(before fringing correction; N = 16.0 and lg = 0.804 mm recomputed). Skin depth 66/√f mm recomputed from ρ = 1.68e-8 Ω·m: 9.2 mm at 50 Hz, 0.206 mm at 100 kHz.

```python
from math import pi, sqrt, log
mu0=4e-7*pi; L, Ipk, Ae, B, G = 50e-6, 10, 1.25e-4, 0.25, 0.02
N = round(L*Ipk/(B*Ae)); lg = mu0*N**2*Ae/L
F = 1 + lg/sqrt(Ae)*log(2*G/lg)
print(N, lg*1e3, F, mu0*N**2*Ae*F/lg*1e6)  # turns, gap mm, fringing factor, L with fringing uH
```

## 3. Transformers: Faraday sets the turns
Flux is set by volt-seconds, not load current:
- Sine: `Vrms = 4.44 · f · N · Ae · Bpk`.
- Square wave (e.g. full-bridge): `V = 4 · f · N · Ae · Bpk`.
Choose Bpk from **core loss**, not saturation, at high frequency (often 0.1–0.2 T for
ferrite at 100 kHz (gated: unconfirmed, source is paywalled or blocked)). Mains transformers (silicon steel, 50/60 Hz) run ~1.5–1.7 T and
are inrush-limited. Magnetising current rises with gap — transformer cores (except flyback) are
ungapped. A flyback "transformer" is a coupled inductor: design it as §2.

## 4. Losses
- Core: Steinmetz `Pv = k · f^α · B^β` with maker's fitted coefficients (β ≈ 2.5–3 (gated: unconfirmed, source is paywalled or blocked)),
  valid for sinusoidal excitation; for PWM waveforms use iGSE or the maker's design tool.
- Copper: DC `I²R` plus AC — skin depth `δ ≈ 66 / √f` mm for copper at 20 °C
  (≈ 0.21 mm at 100 kHz, ≈ 9 mm at 50 Hz). Strand diameter ≲ 2δ; beyond a layer or
  two proximity effect dominates (Dowell's method). Use litz or foil and interleave windings.
- Target total loss for ~40 °C rise; check with the core's thermal resistance.

## 5. Gotchas
- Saturation is about **peak** current at **hot** temperature, including start-up and
  current-limit events — not average.
- DC bias in a transformer (unequal volt-seconds) walks the core into saturation; use
  current-mode control or a series DC-blocking cap.
- Gap tolerances of ±0.05 mm matter on small gaps; specify AL tolerance instead.
- Reluctance models ignore leakage and 3-D fringing; use FEMM (2-D axisymmetric) or
  3-D FEA when within ~20% of saturation or when leakage inductance is a design variable.

## Verify
- [ ] Bpk at worst-case peak current and maximum temperature is below Bsat with ≥ 20% margin.
- [ ] Measured L (LCR meter at the operating frequency) within ±10% of target; L vs DC bias checked.
- [ ] Transformer Bpk from Faraday at Vin(max), Dmax and fmin is within the loss-based limit.
- [ ] Winding strand size compared with skin depth; AC resistance estimated.
- [ ] Temperature rise measured or estimated under worst-case load is within the insulation class.
