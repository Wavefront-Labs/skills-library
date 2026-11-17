---
id: engineering-technology.mechanical-engineering.thermodynamics-power-cycles.rankine-cycle-analysis
name: rankine-cycle-analysis
category: engineering-technology
field: mechanical-engineering
product: thermodynamics-power-cycles
tags: [rankine-cycle, steam-cycle, power-cycle, thermodynamics, state-points, steam-tables, iapws-if97, coolprop, isentropic-efficiency, turbine, pump, condenser, boiler, reheat, regeneration, feedwater-heater, thermal-efficiency, back-work-ratio, exit-quality, second-law, exergy, brayton-cycle, orc]
level: practitioner
status: verified
description: "Analyse a steam Rankine cycle by state points with CoolProp: pump and turbine isentropic efficiency, reheat, quality limits, efficiency and energy-balance checks."
sources: ["Cengel and Boles, Thermodynamics: An Engineering Approach (McGraw-Hill)", "Moran and Shapiro, Fundamentals of Engineering Thermodynamics (Wiley)", "IAPWS-IF97 Industrial Formulation for the Thermodynamic Properties of Water and Steam", "CoolProp documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Rankine cycle analysis — state points, losses, sanity checks

**Goal:** compute thermal efficiency, net work, steam rate and turbine exit quality for a
steam (or organic) Rankine cycle, including real component efficiencies, and know which
design lever to pull.

## 1. Define the cycle and assumptions
States: 1 condenser outlet (saturated liquid), 2 pump outlet, 3 turbine inlet
(superheated), 4 turbine exhaust. State: steady flow, negligible KE/PE, no pressure drop
in boiler/condenser (add later if needed), adiabatic turbine and pump with isentropic
efficiencies (typical: turbine 0.80–0.90, pump 0.75–0.85).

## 2. Properties from a real formulation
Use IAPWS-IF97 (steam tables) — never ideal-gas relations for steam. In Python with
CoolProp (SI units: Pa, K, J/kg):

```python
from CoolProp.CoolProp import PropsSI as P
f = 'Water'; pc, pb, T3 = 10e3, 10e6, 773.15     # 10 kPa, 10 MPa, 500 C
eta_t, eta_p = 0.85, 0.80
h1 = P('H','P',pc,'Q',0,f); v1 = 1/P('D','P',pc,'Q',0,f)
h2 = h1 + v1*(pb - pc)/eta_p                       # pump: incompressible
h3 = P('H','P',pb,'T',T3,f); s3 = P('S','P',pb,'T',T3,f)
h4s = P('H','P',pc,'S',s3,f); h4 = h3 - eta_t*(h3 - h4s)
x4 = P('Q','P',pc,'H',h4,f)
w_net = (h3-h4) - (h2-h1); q_in = h3 - h2
print(f"eta={w_net/q_in:.3f}  x4={x4:.3f}  bwr={(h2-h1)/(h3-h4):.4f}")
```

The script was run (CoolProp 8.0.0): ideal efficiency 0.402 (x4 0.793, steam rate 2.82 kg/kWh); with 0.85/0.80 efficiency 0.341, x4 0.874, back-work ratio 0.0115, steam rate 3.33 kg/kWh. Saturated liquid enthalpy at 10 kPa is 191.8 kJ/kg, matching steam tables. Use these as a check on your setup.

## 3. Interpret and improve
- **Exit quality**: keep x4 >= ~0.88–0.90 to limit last-stage blade erosion (gated: unconfirmed, source is paywalled or blocked). The example
  (0.874) is too wet — the fix is **reheat** (expand to an intermediate pressure,
  reheat to near T3, expand again), not just more superheat.
- **Raise mean heat-addition temperature**: higher boiler pressure and temperature
  (limited by materials, ~540–600 C for conventional plant (gated: unconfirmed, source is paywalled or blocked)). Higher pressure alone wets
  the exhaust.
- **Lower condenser pressure**: limited by cooling-water temperature (saturation 32.9 C at 5 kPa and 45.8 C at 10 kPa, computed) and by exhaust volume flow.
- **Regeneration**: open/closed feedwater heaters with bleed steam; each heater adds a
  mass-fraction unknown solved from its energy balance.
- Steam rate (kg/kWh) = 3600 / w_net(kJ/kg). Mass flow = W_net / w_net.

## 4. Brayton and refrigeration in one line each
Same state-point method. Brayton: back-work ratio is large (40–60 % (gated: unconfirmed, source is paywalled or blocked)), so compressor
efficiency dominates; use real-gas or variable-cp properties at high temperature.
Vapour-compression refrigeration: COP = (h1 - h4)/(h2 - h1), throttling is h = const.

## 5. Gotchas
- CoolProp's default reference state for water matches steam tables closely (computed: h = 0.6 J/kg and s = 0 at the triple-point liquid), but mixing
  enthalpies from different sources (tables vs library) shifts absolute values — keep
  one source.
- At the saturation line, `P,T` input is ambiguous; use `P,Q` instead.
- Pump work is small for steam (back-work ratio ~1 %, computed 0.8 to 1.2 % here) but not for ORC or supercritical
  CO2 cycles — do not drop it there.
- Quote efficiency on a stated basis (gross vs net, HHV vs LHV for the fuel side).

## 6. Second-law check
Exergy destruction per component `T0 * s_gen`. Boiler (finite temperature difference
with combustion gases) normally dominates in steam plant — this tells you where
improvement effort pays.

## Verify
- [ ] Energy balance closes: `q_in - q_out = w_net` within rounding.
- [ ] Every state lies where expected on a T-s diagram (plot it); s4 > s3 for a real turbine.
- [ ] Ideal-cycle efficiency is below Carnot between the same temperature limits.
- [ ] Turbine exhaust quality >= ~0.88 (rule of thumb) or reheat/regeneration explicitly considered.
- [ ] Numbers reproduce a textbook worked example when you plug in its inputs.
