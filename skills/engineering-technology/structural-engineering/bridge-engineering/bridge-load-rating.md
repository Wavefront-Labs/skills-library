---
id: engineering-technology.structural-engineering.bridge-engineering.bridge-load-rating
name: bridge-load-rating
category: engineering-technology
field: structural-engineering
product: bridge-engineering
tags: [bridge-engineering, load-rating, bridge-rating, lrfr, lfr, asr, rating-factor, aashto-mbe, manual-for-bridge-evaluation, aashto-lrfd, hl-93, legal-loads, shv, emergency-vehicles, posting, distribution-factors, dynamic-load-allowance, condition-factor, system-factor, girder-bridge, nbi, aashtoware-brr, inventory-rating, operating-rating]
level: advanced
status: verified
description: "Load rate a highway girder bridge using AASHTO MBE LRFR (and LFR notes): HL-93 and legal loads, distribution factors, condition factors, rating factor equation."
sources:
  - "AASHTO Manual for Bridge Evaluation (MBE), current edition with interim revisions"
  - "AASHTO LRFD Bridge Design Specifications"
  - "AASHTO Standard Specifications for Highway Bridges (for LFR/ASR legacy ratings)"
  - "FHWA guidance on load rating of specialized hauling vehicles and emergency vehicles"
  - "FHWA Specifications for the National Bridge Inventory"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bridge load rating (LRFR) — capacity left for live load, member by member

**Goal:** determine rating factors (RF) for the critical members and limit states of
an in-service girder bridge, for the design load (HL-93) and the legal and
permit vehicles. Then decide whether it needs posting or further evaluation.

Based on the AASHTO MBE (3rd edition and interims) and AASHTO LRFD. The AASHTO texts are paywalled: every MBE/LRFD figure below is from recall and is marked (gated: unconfirmed, source is paywalled or blocked) once here, so confirm each value in the current text; only the FHWA memo statements were checked this session. Factors and
legal-load lists have been revised in interims, so the load-rating engineer must use
the owner's (DOT's) current manual and edition.

## 1. Gather the as-is structure
- As-built plans, shop drawings, material test data and the latest inspection
  report. Record the NBI condition ratings, section loss, cracking, frozen bearings
  and any added wearing surface.
- **Field-measure** the wearing surface thickness where possible. This lets γDW drop
  from 1.50 to 1.25.
- If materials are unknown, use the MBE default strengths by year of construction.

## 2. The rating factor (LRFR, MBE 6A.4.2)
RF = (C − γDC·DC − γDW·DW ± γP·P) / (γLL·(LL + IM))

- **Capacity (strength):** C = φc·φs·φ·Rn, with φc·φs ≥ 0.85.
  - **Condition factor φc:**
    - good/satisfactory (NBI 6 or higher): 1.00;
    - fair (5): 0.95;
    - poor (4 or lower): 0.85.
    Do not take φc on top of a section-loss reduction already measured in Rn
    without checking the MBE guidance.
  - **System factor φs:**
    - redundant multi-girder bridges: 1.00;
    - welded two-girder bridges: 0.85;
    - three-girder bridges and some floor systems: 0.85–0.95.
    Read the MBE table.
- **Dead load factors:** γDC = 1.25; γDW = 1.50 (1.25 if field-measured).
- **Live load factors γLL:**

  | Rating | γLL |
  |---|---|
  | HL-93 inventory | 1.75 |
  | HL-93 operating | 1.35 |
  | Legal loads | ADTT-based, about 1.30–1.45; confirm the table in the current MBE edition (gated: unconfirmed, source is paywalled or blocked) |
  | Permit loads | From the permit-type table |

## 3. Live load effects
- **HL-93:** the design truck (8, 32 and 32 kips, axles at 14 ft and 14–30 ft), or
  the design tandem (two 25-kip axles 4 ft apart), plus a 0.64 klf lane load.
  Dynamic allowance IM = 33% on the truck or tandem only, not the lane.
  For negative moment, also use 90% of two trucks plus 90% of the lane load.
- **Legal loads:**
  - AASHTO Type 3, Type 3S2 and Type 3-3;
  - the lane-type legal loads for long spans;
  - the specialized hauling vehicles SU4–SU7 (or the Notional Rating Load, NRL, screening model: if the NRL rating factor is 1.0 or greater the SU4–SU7 ratings are not needed) and the FAST Act emergency vehicles EV2 (single rear axle) and EV3 (tandem rear axle). Both are FHWA policy: SHV memo of 15 Nov 2013 (fhwa.dot.gov/bridge/loadrating/131115.pdf) and EV memo of 3 Nov 2016 (161103.pdf). EVs are rated at the operating or legal level, and the memo allows a live load factor of 1.3 and exempts bridges (for now) with, e.g., HL-93 inventory RF of at least 0.9 by LRFR.
- **Distribution factors** (LRFD Table 4.6.2.2.2b-1, interior girder moment, concrete
  deck on steel or concrete beams; S and L in ft):
  - one lane: g = 0.06 + (S/14)^0.4·(S/L)^0.3·(Kg/(12·L·ts³))^0.1;
  - two or more lanes: g = 0.075 + (S/9.5)^0.6·(S/L)^0.2·(Kg/(12·L·ts³))^0.1.
  Check the range of applicability. Exterior girders use the lever rule with
  multiple-presence factors (1.20, 1.00, 0.85, 0.65), plus the rigid-section check
  for steel girders with diaphragms.

## 4. Members and limit states
- **Strength I:** flexure at maximum positive and negative moment and at section
  changes; shear at supports and at stirrup or stiffener changes.
- **Service:** Service II for steel permanent deformation (inventory and operating
  stress limits). Service III for prestressed concrete tension (inventory only, for
  the design load).
- **Concrete shear:** MBE allows in-service concrete members with no visible shear
  distress to skip the shear rating for the design and legal loads. Owners vary; confirm the current MBE wording (gated: unconfirmed, source is paywalled or blocked).
- Also rate the deck, floorbeams and stringers, and pin-and-hanger or other
  fracture-critical details where present. Substructure is rated where the owner
  requires it.

## 5. Interpret
- **HL-93 inventory RF ≥ 1.0:** the bridge satisfies current design-level
  reliability, and legal-load rating may be skipped per MBE (gated: unconfirmed, source is paywalled or blocked); but check the FHWA SHV and EV policy, which can still require those vehicles to be rated.
- **Legal-load RF < 1.0:** post or restrict. A common MBE posting expression is
  posting weight = (W/0.7)·(RF − 0.3) for 0.3 ≤ RF < 1.0, with closure considered
  below 0.3. Confirm against the owner policy.
- Report the rating in tons (RF × vehicle weight) for each vehicle, along with the
  controlling member and limit state, for NBI submission.
- **LFR (legacy):** RF = (C − A1·D)/(A2·L·(1 + I)), with A1 = 1.3, A2 = 2.17 for
  inventory and A2 = 1.3 for operating. It is still accepted for older bridges where
  owner policy allows.
- Load testing (MBE Section 8) can justify higher ratings.

**Tools:** AASHTOWare Bridge Rating (BrR) is the common US platform. Refined (grillage
or FE) analysis can replace the distribution factors when ratings are marginal.

## Verify
- [ ] Section properties reflect current section loss and condition from the latest inspection.
- [ ] φc, φs, γDW and γLL match the MBE edition and the owner's manual.
- [ ] HL-93, legal, SHV and EV loads are all rated, including the negative-moment two-truck case.
- [ ] Distribution factors are within their applicability range, or a refined analysis is used.
- [ ] Every critical member and limit state is rated and the controlling RF is identified.
- [ ] Posting decisions follow owner policy and the MBE posting provisions.
