---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.culvert-sizing
name: culvert-sizing
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [hydraulic-hydrologic-design, culvert, culvert-design, culvert-hydraulics, hds-5, hy-8, fhwa, inlet-control, outlet-control, headwater, tailwater, entrance-loss, manning-n, outlet-velocity, scour-protection, rock-riprap, hec-14, energy-dissipator, aep, design-storm, austroads, rational-method, road-drainage, box-culvert, pipe-culvert, cross-drainage]
level: practitioner
status: verified
description: "Size a road culvert: design flow and AEP, inlet vs outlet control, headwater limits, outlet velocity and scour protection, using HDS-5 methods or HY-8."
sources: ["FHWA HDS-5 Hydraulic Design of Highway Culverts (3rd ed., 2012)", "FHWA HEC-14 Hydraulic Design of Energy Dissipators for Culverts and Channels", "FHWA HY-8 Culvert Hydraulic Analysis Program user documentation", "Austroads Guide to Road Design Part 5B: Drainage - Open Channels, Culverts and Floodways", "Chow, Open-Channel Hydraulics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Culvert sizing — inlet control, outlet control, and what happens at the outlet

**Goal:** choose a culvert size, shape, material and inlet that passes the design flow
with headwater below the allowable level, survives the check flood, and doesn't scour
its own outlet.

## 1. Set the design criteria (before any hydraulics)
- **Design AEP:** set by the road authority, not by preference. Typical US state DOT
  practice: around 2% AEP (50-year) for major highways with a 1% check; lower-class roads
  10–4%. Austroads/Australian state practice is similar in shape (e.g. 10% AEP for minor
  roads up to 1% AEP for major roads/freeways) (gated: unconfirmed, source is paywalled or blocked) — use the specific authority manual.
- **Allowable headwater (HW):** the lowest of: road shoulder minus freeboard (often
  300 mm / 1 ft (gated: unconfirmed, source is paywalled or blocked)), upstream property flood levels, and a HW/D ratio limit. FHWA HDS-5 states the allowable HW/D varies by agency and
  commonly ranges from 1.0 to 1.5 (fetched, HDS-5 3rd ed. 2012); use the agency's value.
- Minimum diameter for maintenance (often 450–600 mm / 18–24 in in US and AU practice (gated: unconfirmed, source is paywalled or blocked)).
- Fish/fauna passage requirements can override pure hydraulic sizing.

## 2. Design flow
Small catchments: Rational Method Q = C·i·A (Q = 0.278·C·i·A with i in mm/h, A in km²,
Q in m³/s (computed: 1 mm/h over 1 km² = 0.2778 m³/s); or Q = C·i·A in cfs with i in in/h, A in acres). Larger or rural catchments:
regional regression, unit hydrograph, or a runoff-routing model. Get time of
concentration right — it controls i.

## 3. Tailwater
Get TW from a normal-depth calculation of the downstream channel (Manning), or from a
known downstream control. TW governs whether outlet control dominates.

## 4. Inlet control vs outlet control (HDS-5 approach)
Compute HW both ways for each trial size; the **higher** governs.

**Inlet control** — capacity limited by the entrance (barrel flows part-full,
supercritical). Use the HDS-5 nomographs or inlet-control equations for the specific
inlet type. Improving the inlet (bevels, wingwalls, tapered inlet) helps; a longer or
smoother barrel does not.

**Outlet control** — barrel friction, TW and losses govern:
HW = H + h_o − L·S
H = [1 + k_e + (2g·n²·L)/R^(4/3)]·V²/(2g) (SI form; HDS-5 eq. 3.4 writes the friction term as K_U n² L/R^1.33 with K_U = 29 in English units and 19.63 in SI, and 2g = 19.62 m/s², so the forms agree; the exit loss is the full barrel velocity head, giving the leading 1)
h_o = max(TW, (d_c + D)/2) for the usual case (HDS-5 allows the (d_c + D)/2 approximation only where the barrel flows full for part of its length).

Entrance loss coefficients k_e (HDS-5 Table C.2, checked: socket-end concrete pipe projecting 0.2, square-edged headwall 0.5, bevelled edges 0.2, projecting corrugated metal 0.9, mitred to slope 0.7):
| Inlet | k_e |
|---|---|
| Concrete pipe, socket end projecting | 0.2 |
| Square-edged headwall | 0.5 |
| Bevelled / wingwalls with bevelled edges | 0.2 |
| Projecting thin-wall CMP | 0.9 |
| Mitred to slope | 0.7 |

Manning's n: concrete pipe/box 0.012–0.013; helical corrugated metal 0.022–0.027 depending on corrugation profile (HDS-5 Appendix B, fetched; the HDS-5 body also uses 0.012 smooth and 0.024 rough as typical values).

## 5. Use HY-8 (or equivalent) properly
- Enter crossing, roadway profile (for overtopping), tailwater channel, and each barrel.
- Run a range of flows up to the check flood; read the **performance curve** for the
  control type, HW, outlet velocity and overtopping.
- Multi-barrel sets split flow equally only if inverts and inlets are identical.

## 6. Outlet velocity and scour
- Compute outlet velocity with outlet depth (normal depth in barrel for inlet control,
  or max(d_c, TW) for outlet control).
- Compare with the downstream channel's permissible velocity. Concrete pipes on steep
  grades commonly produce 4–6 m/s (13–20 ft/s) (gated: unconfirmed, source is paywalled or blocked) — far beyond what grass or most soils
  tolerate.
- Protection: rock riprap apron sized per HEC-14 (or Austroads Part 5B), or an energy
  dissipator (stilling basin, impact basin) for high velocities.

## Gotchas
- Sizing only for inlet control on flat grades with high tailwater undersizes the culvert.
- Ignoring road overtopping hides where the water actually goes in the check flood.
- Debris and sediment blockage: many Australian guidelines (e.g. ARR 2019 Book 6
  blockage procedures) require explicit blockage factors (gated: unconfirmed, source is paywalled or blocked); US practice often adds a size
  margin instead.
- Equations above are the classic HDS-5 forms; check the US-units coefficient (29·n²L/R^1.33
  in imperial) before mixing units.

## Verify
- [ ] Design AEP, check flood and allowable HW are taken from the governing authority.
- [ ] HW computed for both inlet and outlet control; the controlling value is reported.
- [ ] HW/D and freeboard to road edge meet the criteria at the design flow.
- [ ] Check flood behaviour (overtopping depth/velocity, upstream flood level) is acceptable.
- [ ] Outlet velocity compared with downstream permissible velocity; scour protection designed.
- [ ] Blockage and minimum-size requirements addressed.
