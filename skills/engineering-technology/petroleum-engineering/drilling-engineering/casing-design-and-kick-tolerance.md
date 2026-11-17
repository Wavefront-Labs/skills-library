---
id: engineering-technology.petroleum-engineering.drilling-engineering.casing-design-and-kick-tolerance
name: casing-design-and-kick-tolerance
category: engineering-technology
field: petroleum-engineering
product: drilling-engineering
tags: [casing-design, casing-setting-depth, pore-pressure, fracture-gradient, mud-weight-window, burst, collapse, tension, design-factor, api-tr-5c3, iso-10400, triaxial, von-mises, kick-tolerance, maasp, well-control, kill-sheet, kill-mud-weight, icp-fcp, lot, fit, ecd, drillers-method]
level: advanced
status: gated
description: "Pick casing setting depths from pore/frac gradients, size casing for burst/collapse/tension with design factors (API TR 5C3), and compute kick tolerance, MAASP and a basic kill sheet."
sources:
  - "API TR 5C3 / ISO 10400, Calculating Performance Properties of Pipe Used as Casing or Tubing"
  - "API RP 96, Deepwater Well Design and Construction"
  - "IWCF and IADC WellSharp well-control syllabus material"
  - "Bourgoyne et al., Applied Drilling Engineering (SPE Textbook Vol. 2)"
  - "Rabia, Well Engineering & Construction"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Casing design and kick tolerance — setting depths, load cases and well-control margins

**Goal:** choose casing points and strings that hold worst credible loads, and know each section's safe kick size before drilling it.

> Engineering guidance only. Casing design and well control are safety-critical; final designs must follow the operator's well-design standard, the governing regulator and a competent, independent review.

## 1. Pressure basics

Hydrostatic: P (psi) = 0.052 × MW (ppg) × TVD (ft); SI: P (kPa) = 9.81 × SG × TVD (m). Plot pore pressure (PP), fracture gradient (FG) and mud weights as equivalent mud weight vs TVD on one chart. PP from offsets and sonic/resistivity trends (Eaton); FG from LOT/FIT data and Eaton or Matthews–Kelly.

## 2. Mud-weight window and setting depths

- Minimum MW = PP + trip margin (typically 0.2–0.5 ppg) (gated: unconfirmed, source is paywalled or blocked).
- Maximum MW (as ECD while circulating) = FG − safety margin (0.3–0.5 ppg) (gated: unconfirmed, source is paywalled or blocked), also above wellbore-stability collapse pressure.
- **Bottom-up selection:** start at TD with the MW needed there plus kick margin (~0.5 ppg) (gated: unconfirmed, source is paywalled or blocked); go up until the FG line meets that requirement — that is the deepest point the previous shoe must reach. Repeat upward. Then check top-down for shallow hazards, aquifers, losses and regulatory minimums.

## 3. Load cases (typical; operators define their own)

**Burst** (internal minus external):
- Gas to surface / gas kick: internal = reservoir pressure at next TD minus gas gradient (0.1–0.15 psi/ft) (gated: unconfirmed, source is paywalled or blocked) up to surface, limited by shoe fracture pressure if that is lower (the shoe breaks first).
- Pressure test and, for production casing, frac/stimulation pressure (see engineering-technology.petroleum-engineering.well-completion-design.hydraulic-fracture-design).
- Backup outside: pore pressure or seawater/brine gradient (~0.45 psi/ft; seawater computes to 0.444 psi/ft from 1.025 SG x 0.4335) — not the original mud, which degrades.

**Collapse** (external minus internal):
- Full evacuation (surface and production casing in gas wells, or deepwater lost returns) or partial evacuation to the level a loss zone supports.
- External: mud at time of running, or pore pressure for long-term; salt/plastic formations may need overburden-equivalent load.

**Tension:** buoyed string weight (buoyancy factor BF = 1 − MW/65.5 for steel in ppg; 65.5 ppg = 7.85 SG x 8.345 computed) + overpull (often 100 klbf (gated: unconfirmed, source is paywalled or blocked)) + shock load + bending in doglegs (≈ 63·OD·DLS·w lbf (gated: unconfirmed, source is paywalled or blocked)). Check pipe body and connection.

**Design factors (common ranges, confirm against your standard):** burst 1.1–1.25, collapse 1.0–1.125, tension 1.6–1.8, triaxial (von Mises) 1.25 (gated: unconfirmed, source is paywalled or blocked). Ratings come from API TR 5C3 / ISO 10400 (four collapse regimes, (gated: unconfirmed, source is paywalled or blocked); tension reduces collapse rating — apply the biaxial correction). Derate yield for temperature and use sour-service grades (NACE MR0175/ISO 15156) where H2S is present.

## 4. Kick tolerance and MAASP
Derivation check: shut-in casing pressure with gas at bottom = (PP_TD − G_mud·TVD) + (G_mud − G_gas)·H; setting it equal to MAASP gives the H_max expression below (hydrostatic algebra, derived this session).

**MAASP** (with current mud) = (FG_shoe − MW) × 0.052 × TVD_shoe. Update it whenever MW changes; re-measure FG with a LOT/FIT after drilling out each shoe (3–5 m/10–20 ft new hole) (gated: unconfirmed, source is paywalled or blocked).

**Kick tolerance** = the maximum influx volume (at a stated kick intensity, e.g. 0.5 ppg over PP) that can be shut in and circulated out without exceeding the shoe fracture pressure. Method:
1. Max gas height at bottom (shut-in case): H_max = [MAASP − (PP_TD − MW)·0.052·TVD_TD] / (G_mud − G_gas), where PP_TD includes the kick intensity and gradients are in psi/ft. This is the bottom-hole shut-in case only; also check the circulating case with the expanded (Boyle's law) bubble at the shoe and take the smaller volume.
2. Convert height to volume with the annular capacity around the BHA (worst case).
3. Compare with what the crew can reliably detect (company minimums vary by hole size; no typical value is claimed; unconfirmed). Zero or negative means the section cannot be drilled as planned: move the shoe or use MPD.

## 5. Kill sheet basics

- Kill mud weight: KMW = OMW + SIDPP / (0.052 × TVD).
- Initial circulating pressure: ICP = SCR pressure (slow circulating rate) + SIDPP.
- Final circulating pressure: FCP = SCR × KMW / OMW.
- Step drillpipe pressure from ICP to FCP over surface-to-bit strokes, then hold FCP. Driller's method circulates the kick out with OMW first; wait-and-weight kills in one circulation.
- Rising SICP with the well shut in suggests gas migration; SICP approaching MAASP is the critical alarm.

## Gotchas

- Using the original mud as burst backup overstates capacity after barite sag.
- Kick tolerance changes with depth; recompute while drilling toward higher pressure.
- LOT vs FIT: a FIT does not find the fracture limit; don't use it as FG without saying so.

## Verify

- [ ] PP/FG/MW chart with every planned shoe inside the window and margins stated.
- [ ] Each string checked for burst, collapse, tension and triaxial with stated design factors and deratings.
- [ ] Kick tolerance positive and above the detection threshold for each section.
- [ ] MAASP posted on the rig floor and updated after each MW change.
- [ ] Kill sheet pre-filled with SCRs, capacities and strokes.
- [ ] Independent review signed off per operator standard.
