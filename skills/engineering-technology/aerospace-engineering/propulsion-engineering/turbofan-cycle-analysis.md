---
id: engineering-technology.aerospace-engineering.propulsion-engineering.turbofan-cycle-analysis
name: turbofan-cycle-analysis
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, gas-turbine, turbofan, cycle-analysis, brayton-cycle, on-design, parametric-cycle, bypass-ratio, overall-pressure-ratio, fan-pressure-ratio, turbine-inlet-temperature, tsfc, specific-thrust, polytropic-efficiency, station-numbering, sae-arp755, nozzle, choked-nozzle, gasturb, npss, pycycle, mattingly, engine-airframe-matching]
level: advanced
status: gated
description: "Run on-design turbofan cycle analysis: station-by-station Brayton cycle with component efficiencies, BPR/OPR/TIT trades, specific thrust and TSFC."
sources:
  - "Mattingly, Elements of Propulsion: Gas Turbines and Rockets"
  - "Saravanamuttoo, Rogers, Cohen et al., Gas Turbine Theory"
  - "Walsh and Fletcher, Gas Turbine Performance"
  - "Kerrebrock, Aircraft Engines and Gas Turbines"
  - "SAE ARP755, Gas Turbine Engine Performance Station Identification and Nomenclature"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Turbofan on-design cycle analysis — from cycle parameters to TSFC

**Goal:** given flight condition, BPR, fan and overall pressure ratio, turbine inlet
temperature and component efficiencies, compute specific thrust and TSFC, then trade
the parameters intelligently.

## 1. Stations (SAE ARP755 style, separate-flow turbofan)
`0` freestream · `2` fan face · `13` fan exit (bypass) · `25` HPC inlet · `3` HPC exit ·
`4` combustor exit (TIT / T41 at rotor inlet) · `45` LPT inlet · `5` LPT exit ·
`8`/`9` core nozzle throat/exit · `18`/`19` bypass nozzle throat/exit.

## 2. The march through the engine
1. **Freestream to total:** `Tt0 = T0 (1 + (γ−1)/2 M0²)`, `Pt0 = P0 (Tt0/T0)^(γ/(γ−1))`.
   Intake pressure recovery ~0.99–0.995 subsonic.
2. **Compressors** with polytropic efficiency (keeps trades fair across pressure ratios):
   `Tt_out/Tt_in = π^((γ−1)/(γ η_p))`. Typical η_p: fan 0.90–0.93, HPC 0.90–0.92 (gated: unconfirmed, source is paywalled or blocked).
3. **Combustor:** `f = (cp_h Tt4 − cp_c Tt3) / (η_b h_PR − cp_h Tt4)`;
   η_b ≈ 0.995+, total pressure loss 3–5%, `h_PR ≈ 43 MJ/kg` for Jet-A (gated: unconfirmed, source is paywalled or blocked).
4. **Turbines from work balance** (per unit core flow, including fuel and bleeds):
   HPT drives HPC (plus offtakes); LPT drives fan **including bypass flow**
   (`(1 + BPR) × fan work`) and booster. `Tt_out/Tt_in = 1 − Δh/(cp Tt_in)`, then
   pressure ratio from turbine polytropic η_p ≈ 0.89–0.92 (`π_t = τ_t^(γ/((γ−1) η_p))`).
   Mechanical efficiency ~0.99.
5. **Nozzles:** choked if `Pt/P0` exceeds the critical ratio (1.85 for γ = 1.33 and 1.89 for γ = 1.4, computed from ((γ+1)/2)^(γ/(γ−1))).
   For a convergent choked nozzle, exit is sonic and thrust includes pressure thrust
   `(P_exit − P0) A_exit`. Nozzle velocity coefficient Cv ~0.98–0.99.
6. **Performance:**
   `F/ṁ_total = [ (1+f) V9 − V0 + BPR (V19 − V0) + pressure terms ] / (1 + BPR)`,
   `TSFC = ṁ_fuel / F`.

Minimal ideal-gas sketch (constant cp per side; real work uses variable cp):
```python
import math
g_c, cp_c, g_h, cp_h = 1.4, 1004.5, 1.33, 1156.0
def turbofan(M0, T0, P0, BPR, FPR, OPR, Tt4, eta_f=0.92, eta_c=0.91, eta_t=0.90,
             hPR=43e6, eta_b=0.995, pi_b=0.96):
    a0 = math.sqrt(g_c*287*T0); V0 = M0*a0
    Tt0 = T0*(1+0.2*M0**2); Pt0 = P0*(Tt0/T0)**3.5
    ex = (g_c-1)/g_c
    Tt13 = Tt0*FPR**(ex/eta_f); Pt13 = Pt0*FPR
    Tt3 = Tt0*OPR**(ex/eta_c);   Pt3 = Pt0*OPR
    f = (cp_h*Tt4 - cp_c*Tt3)/(eta_b*hPR - cp_h*Tt4)
    w_hpc = cp_c*(Tt3 - Tt0)            # all core compression, 0 -> 3
    w_fan_bypass = BPR*cp_c*(Tt13 - Tt0)
    Tt5 = Tt4 - (w_hpc + w_fan_bypass)/((1+f)*cp_h)
    pi_t = (Tt5/Tt4)**(g_h/((g_h-1)*eta_t)); Pt5 = Pt3*pi_b*pi_t
    def V_exit(Pt, Tt, g, cp):          # fully expanded (ideal) exit velocity
        return math.sqrt(2*cp*Tt*(1-(P0/Pt)**((g-1)/g)))
    V9, V19 = V_exit(Pt5, Tt5, g_h, cp_h), V_exit(Pt13, Tt13, g_c, cp_c)
    Fs = ((1+f)*V9 - V0 + BPR*(V19 - V0))/(1+BPR)     # N per kg/s total air
    tsfc = f/((1+BPR)*Fs)                              # kg/(N s)
    return Fs, tsfc*1e6                                # g/(kN s)
```
The sketch lumps all core compression from station 0 to 3 and assumes full expansion;
it is a check tool. Run as written (cruise M 0.8, 35,000 ft, BPR 11, FPR 1.4, OPR 45, Tt4 1650 K) it returns about 133 N per kg/s and TSFC 16.7 g/(kN s); with no cooling-flow or loss model it sits above the quoted cruise range. 14 and 15.5 g/(kN s) convert to 0.49 and 0.55 lb/(lbf h). Production work uses GasTurb, NPSS, pyCycle or Mattingly's
companion software with real-gas properties, bleeds and cooling flows.

## 3. Typical numbers (modern high-BPR civil, indicative; all figures in this section (gated: unconfirmed, source is paywalled or blocked))
- BPR 9–12 (geared designs higher), FPR 1.35–1.5, OPR 40–55 at top of climb,
  T4 at take-off roughly 1,800–2,000 K class (programme-dependent).
- Cruise TSFC ~14–15.5 g/(kN·s) (≈ 0.50–0.55 lb/(lbf·h)); older low-BPR engines 0.6–0.8.
- Turbine cooling and leakage bleed 15–25% of core flow; ignoring it overstates
  efficiency by several percent of TSFC.

## 4. Trades that matter
- **Optimum FPR for a given BPR/core:** best fuel burn when the jet velocity ratio
  `V19/V9 ≈ η_LPT · η_fan` (~0.75–0.85). Sweep FPR and look for the TSFC minimum.
- Raising BPR lowers TSFC (propulsive efficiency) but cuts specific thrust: bigger fan,
  nacelle drag and weight. The installed optimum is lower than the uninstalled one.
- Raising OPR raises thermal efficiency until compressor exit temperature T3 (disc
  material limit, roughly 900–1,000 K class) or small-core blade-height losses bite.
- Size the engine at top of climb / take-off and check cruise as off-design.

## Gotchas
- Mixing γ = 1.4 everywhere overpredicts hot-side work; use ~1.33 or variable cp.
- The fan's bypass work comes from the LPT: forgetting the `BPR ×` term gives absurd T5.
- Specific thrust per total vs per core airflow: state which.

## Verify
- [ ] Energy balance closes at each spool (compressor work = turbine work × η_mech).
- [ ] Nozzle choke status checked; pressure thrust included if under-expanded.
- [ ] Results reproduce a textbook worked example (e.g. Mattingly) before new studies.
- [ ] TSFC and specific thrust fall in plausible ranges for the BPR class.
- [ ] Trends behave: TSFC falls with BPR at fixed core; specific thrust falls too.
