---
id: engineering-technology.nuclear-engineering.thermal-hydraulics.critical-heat-flux-margin-analysis
name: critical-heat-flux-margin-analysis
category: engineering-technology
field: nuclear-engineering
product: thermal-hydraulics
tags: [thermal-hydraulics, critical-heat-flux, chf, dnb, dnbr, mdnbr, mcpr, boiling-transition, w-3-correlation, chf-lookup-table, groeneveld, hot-channel-factors, fdh, fq, subchannel-analysis, cobra-tf, ctf, vipre-01, relap5, trace, rtdp, 95-95, pwr, bwr, 10-cfr-50-46, srp-4-4]
level: advanced
status: gated
description: "Evaluate PWR DNBR and BWR MCPR margins: CHF correlations and lookup table, hot channel factors, subchannel/system codes, 95/95 design limits and statistical uncertainty treatment."
sources:
  - "Todreas & Kazimi, Nuclear Systems Vol. I and II"
  - "Tong & Tang, Boiling Heat Transfer and Two-Phase Flow"
  - "Groeneveld et al., The 2006 CHF Look-up Table (Nuclear Engineering and Design, 2007)"
  - "NUREG-0800 Standard Review Plan, Section 4.4 Thermal and Hydraulic Design"
  - "10 CFR 50.46 and 10 CFR 50 Appendix A (GDC 10)"
  - "VIPRE-01 and COBRA-TF (CTF) theory manuals"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical heat flux margin analysis — proving the hot rod does not boil dry

**Goal:** show, for steady state and every anticipated operational occurrence (AOO), that the limiting fuel rod stays clear of departure from nucleate boiling (PWR) or boiling transition (BWR) with 95% probability at 95% confidence.

Engineering guidance only. Licensing calculations require NRC-approved (or national-regulator-approved) correlations, codes and methodologies applied within their qualified ranges, with independent review.

## The figure of merit

- **PWR:** DNBR(z) = q''_CHF(z) / q''_local(z). The minimum along the hot channel, MDNBR, must exceed the **correlation design limit**: the value at which 95/95 of the correlation's database would not have experienced DNB. Examples: W-3 historically 1.30; WRB-1 / WRB-2 around 1.17gated: unconfirmed, source is paywalled or blocked; confirm the approved value for your fuel and correlation).
- **BWR:** critical power ratio CPR = critical bundle power / actual bundle power. The Safety Limit MCPR (SLMCPR, typically ~1.05-1.10gated: unconfirmed, source is paywalled or blocked) is set so that ≥99.9% of rods avoid boiling transition. The Operating Limit MCPR (OLMCPR, typically ~1.3-1.5gated: unconfirmed, source is paywalled or blocked) = SLMCPR + ΔCPR of the worst AOO. Correlations are vendor-specific (GEXL-family and others).

## Correlations

- **W-3 (Tong):** empirical, uniform-heat-flux correlation with non-uniform shape factor F_c. Valid roughly for p = 1000-2300 psia, G = 1.0-5.0 Mlbm/(h·ft²), local quality −0.15 to +0.15gated: unconfirmed, source is paywalled or blocked). Out-of-range use invalidates the limit.
- **Vendor grid-specific correlations** (WRB-x, ABB-NV, etc.) include mixing-vane grid effects; required for modern fuel.
- **2006 CHF Lookup Table (Groeneveld):** tabulated CHF for an 8 mm tube versus pressure, mass flux and quality, with correction factors for diameter, bundle geometry, grid spacers, heated length, axial flux shape and horizontal flow. Good for scoping, research reactors and code-independent checks; not a substitute for an approved bundle correlation in licensing.

Always use the **local (subchannel) conditions** — never core-average quality or mass flux.

## Method

1. **Power distribution:** take FΔH (enthalpy rise hot channel factor) and the axial shape from the core design (engineering-technology.nuclear-engineering.reactor-physics.core-criticality-and-reactivity-coefficients). Typical PWR FΔH limit ~1.55-1.65; FQ ~2.5 (gated: unconfirmed, source is paywalled or blocked). Use the most limiting axial shapes (top-skewed shapes often limit DNBR at high power).
2. **Engineering factors:** fuel manufacturing tolerances (F_q^E ~1.03gated: unconfirmed, source is paywalled or blocked), inlet flow maldistribution, bypass flow, rod bow penalty, transition core (mixed fuel) penalty.
3. **Subchannel model:** VIPRE-01, COBRA-IV/COBRA-TF (CTF) or THINC-type codes. Model the hot assembly subchannel-by-subchannel with lumped neighbours; set turbulent mixing coefficient (β) and grid loss coefficients to the qualified values; inlet flow reduced for hot-assembly maldistribution (often ~5%gated: unconfirmed, source is paywalled or blocked).
4. **Uncertainty treatment:**
   - *Deterministic:* apply nominal-plus-uncertainty to power, flow, pressure, temperature simultaneously.
   - *Statistical (RTDP/ITDP):* run nominal conditions, propagate the parameter uncertainties statistically into a higher statistical DNBR limit (e.g. ~1.23-1.35, plant-specificgated: unconfirmed, source is paywalled or blocked), then retain extra analytical margin for future penalties (rod bow, fuel changes).
5. **Transients:** system codes (RELAP5, TRACE, RETRAN, CATHARE) give power, flow, pressure and inlet temperature versus time for loss-of-flow, locked rotor, rod withdrawal, etc.; feed boundary conditions into the subchannel code to obtain MDNBR versus time.
6. **Accident criteria beyond DNB:** for LOCA, 10 CFR 50.46(b) criteria (peak cladding temperature not above 2200 °F = 1204 °C, total oxidation not above 0.17 of cladding thickness, hydrogen not above 0.01 of the hypothetical maximum, plus coolable geometry and long-term cooling; checked on eCFR). Check whether your jurisdiction has adopted revised cladding embrittlement rules.

## Gotchas

- Grid spacers raise local CHF downstream; a correlation without grid terms on mixing-vane fuel is wrong in both directions depending on span.
- Rod bow penalty grows with burnup; ignoring it erodes the retained margin silently.
- Low-flow, low-pressure conditions (natural circulation, shutdown) usually lie outside PWR correlation ranges; use a low-flow correlation or the lookup table and state it.
- Mixed cores: the new fuel's different pressure drop diverts flow away from it — model the full mixture, not a uniform core.
- DNBR in BWR or CPR in PWR terms are not interchangeable; convert margins only through the governing methodology.
- Code nodalisation: too-coarse axial nodes smear the MDNBR location. Check node-size convergence.

## Verify

- [ ] Every evaluated point lies within the correlation's qualified range of pressure, mass flux, quality and geometry.
- [ ] MDNBR (or MCPR) for steady state and each AOO exceeds the 95/95 design or safety limit with the stated retained margin.
- [ ] Power distribution used bounds the core design (FΔH, FQ, limiting axial shapes) for all statepoints.
- [ ] Rod bow, transition-core and other penalties applied and documented.
- [ ] Nodalisation and mixing-coefficient sensitivity runs show the result is converged and conservative.
- [ ] Independent check (lookup table or second code) agrees within an explainable amount.
