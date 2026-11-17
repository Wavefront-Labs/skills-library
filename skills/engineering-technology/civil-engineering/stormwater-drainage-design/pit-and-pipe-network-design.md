---
id: engineering-technology.civil-engineering.stormwater-drainage-design.pit-and-pipe-network-design
name: pit-and-pipe-network-design
category: engineering-technology
field: civil-engineering
product: stormwater-drainage-design
tags: [stormwater-drainage-design, stormwater, urban-drainage, pit-and-pipe, storm-sewer, inlet-design, hydraulic-grade-line, hgl, pit-losses, rational-method, time-of-concentration, minor-major-system, overland-flow, gutter-flow, spread, hec-22, arr-2019, qudm, drains, swmm, 12d, civil-3d, infodrainage, aep, manning-n]
level: practitioner
status: verified
description: "Design a minor/major stormwater pit-and-pipe network: catchments, Rational Method, HGL with pit losses, pipe grades and cover, and overland flow checks."
sources: ["FHWA HEC-22 Urban Drainage Design Manual (3rd ed.)", "Australian Rainfall and Runoff 2019 (ARR), Book 9: Runoff in Urban Areas", "Queensland Urban Drainage Manual (QUDM)", "US EPA SWMM Reference Manual (Hydraulics)", "ASCE/WEF Design and Construction of Urban Stormwater Management Systems (MOP 77)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pit-and-pipe network design — minor system sized by HGL, major system checked overland

**Goal:** a piped (minor) system that captures and carries the minor design storm with
the hydraulic grade line safely below the surface, plus a major-storm overland flow
path that keeps people and buildings safe when the pipes are full or blocked.

## 1. Criteria first
Set from the local authority manual; typical values:
- **Minor system AEP:** Australia (ARR 2019/QUDM-style practice) roughly 10% AEP for
  residential streets, 5–2% for commercial/industrial and CBD (practice figures (gated: unconfirmed, source is paywalled or blocked)). US (HEC-22 style)
  storm sewers often sized for the 10-year event; HEC-22 (3rd ed.) says the minor system is normally designed for 10-year storms and storm drains serving sag points with no other relief should be designed for at least a 50-year storm.
- **Major system:** 1% AEP for overland flow paths, with freeboard to floor levels
  (commonly 300 mm in Australian practice (gated: unconfirmed, source is paywalled or blocked); local codes vary).
- **Street flow limits:** US — spread limits on the travelled lane (HEC-22, e.g. shoulder
  plus a fraction of a lane depending on road class); Australia — depth × velocity
  d·V ≤ 0.4 m²/s for pedestrian safety where people are likely (gated: unconfirmed, source is paywalled or blocked), and a maximum ponding
  depth at the kerb.
- **Pipes:** minimum diameter commonly 375 mm (AU (gated: unconfirmed, source is paywalled or blocked)); HEC-22's worked example uses 460 mm (18 in) minimum "for maintenance purposes". Self-cleaning velocity: HEC-22 7.2.4 says design for full-flow velocity of 0.9 m/s (3 ft/s) or more, which is 0.6 m/s (2 ft/s) at 25% depth. Maximum velocity commonly ~6 m/s (gated: unconfirmed, source is paywalled or blocked). Minimum cover: HEC-22 7.2.5 says 0.9 m (3.0 ft) for highway applications where possible, else check structural capacity; ~600 mm is an Australian-practice figure (gated: unconfirmed, source is paywalled or blocked) (pipe class and local
  standards govern).

## 2. Layout
1. Place pits at low points (sags), at changes of direction, grade or size, at junctions,
   and on grade to keep gutter flow within limits — typically every 60–100 m (gated: unconfirmed, source is paywalled or blocked) on a
   continuous grade, closer on steep or wide roads.
2. Pipes follow roads/easements, straight between pits.
3. Draw sub-catchments to each pit; assign fraction impervious and flow-path lengths.

## 3. Hydrology
- **Rational Method** for small urban catchments: Q = C·i·A (consistent units).
  Time of concentration = inlet time (property + overland + gutter) + pipe travel time.
  Accumulate tc along the network; at each pipe use the critical tc and the
  contributing area — the "partial area" effect can make a smaller, faster area govern.
- Larger or detention-controlled systems: use a hydrograph method (ILSAX/DRAINS-type,
  SWMM, or the authority's method). ARR 2019 moved Australian practice toward ensemble
  and hydrograph methods even for urban design — check what your authority accepts.

## 4. Inlet capacity
- On-grade pits: capture < 100%; bypass flow goes to the next pit downstream — carry it.
- Sag pits: capture everything up to the ponding limit; check both weir and orifice regimes.
- Apply **blockage factors** to inlet capacity per local guidance (sag pits typically
  get a larger reduction than on-grade).

## 5. Pipe sizing and the HGL
1. Size pipes for full-flow capacity with Manning (n = 0.013 for ordinary concrete per HEC-22 Table 7-7 and the Chapter 7 example; plastic 0.011–0.012 is common practice (gated: unconfirmed, source is paywalled or blocked); agencies may specify).
2. Start the **HGL at the outfall**: the higher of the receiving water level for a
   coincident event or the pipe's normal-flow level. A free-outfall assumption in a creek
   that is itself flooding is a classic error.
3. Work upstream: friction loss (Sf·L) plus **pit/structure losses** h = K·V²/(2g).
   K depends on the pit geometry, junction angle, flow ratios and plunging inflow
   (Missouri charts in QUDM/ARR; HEC-22 energy-loss method). Straight-through K ≈ 0.5
   is a rough start (gated: unconfirmed, source is paywalled or blocked); 90° bends and multi-pipe junctions are far higher.
4. **Check the HGL at every pit** is below the surface by the freeboard required (a Brisbane City Council drawing checklist, which refers to QUDM, flags an HGL more than 150 mm from the surface level at manholes and kerb inlets, so confirm the QUDM wording (gated: unconfirmed, source is paywalled or blocked) and your authority's value).
5. Match pipe obverts (crowns) at size increases, not inverts; never reduce pipe size
   downstream.

## 6. Major system check
At the major event, pipes carry what they can (with blockage); the remainder runs in
roads and designated flow paths. Check d·V, depth, and freeboard to floor levels along
every overland path, including sags with no escape route.

## Tools
DRAINS (Australia), 12d, Civil 3D (Storm and Sanitary Analysis/ Hydraflow), Autodesk
InfoDrainage, EPA SWMM, PCSWMM. All produce an HGL; all depend on the loss coefficients
and tailwater you give them.

## Verify
- [ ] Minor and major AEPs, freeboard and street-flow limits come from the governing authority manual.
- [ ] Tailwater at the outfall reflects a realistic coincident downstream level.
- [ ] HGL is below every pit surface by the required freeboard at the minor design flow.
- [ ] Bypass from on-grade pits is carried downstream and sag pits have safe overflow.
- [ ] Velocities are within self-cleansing and maximum limits; cover and minimum sizes met.
- [ ] Major-event overland flow paths satisfy d·V and floor-level freeboard checks.
