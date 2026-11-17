---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.pack-crash-protection-design
name: pack-crash-protection-design
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [pack-crash-protection, pack-mechanical, reess-protection, underbody-protection, intrusion-limit, crush-zone, battery-crash, un-r100, gtr-20]
level: practitioner
status: gated
description: "Protect an EV traction battery in crashes and impacts: place it, build crush and shear structures, set cell intrusion limits, and plan CAE and test checks. Practice guidance."
sources:
  - "UN Regulation 100 (REESS safety; confirm current revision at https://unece.org)"
  - "UN GTR 20 (electric vehicle safety); ISO 6469 series"
  - "Kramer, Passive Safety of Vehicles; Huang, Vehicle Crash Mechanics (chapter lists)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pack crash protection design

Safety-critical practice guidance. Regulations and consumer-test requirements change; confirm current UN, FMVSS and NCAP texts and defer approvals to qualified safety engineers and the approval authority.

## 1. Placement
Put the pack where crash intrusion is least likely: between axles, inside the sills, away from front and rear crush zones. Keep a designed crush distance at the sides (side-pole intrusion is the severe case; see EV side pole battery protection).

## 2. Structures around the pack
- **Frame/perimeter:** extrusions or hot-formed members absorb side loads and spread them into body and floor cross-members.
- **Crush zones and shear plates:** sacrificial structure takes intrusion before the cells.
- **Underbody shield:** thickness and material (steel, aluminium, composite) for stone strike and ground impact; account for corrosion and mass.
- **Cross-members inside the pack** limit lateral squash and cell sliding.

## 3. Cell and pack limits
Obtain from cell suppliers and abuse tests the cell deformation, compression and penetration tolerance and the failure thresholds (short circuit, venting, thermal runaway). Convert to pack-level intrusion and acceleration limits with margin.

## 4. Tests and standards context
UN Regulation 100 covers REESS safety including mechanical tests (gated: unconfirmed, source is paywalled or blocked), and GTR 20 defines electric vehicle safety requirements for the parties that adopt it; both have revisions and national implementations, so confirm the edition applicable to your market. Whole-vehicle crash regulations and consumer tests (frontal, side, pole, rear) add post-crash electrical safety criteria (isolation, voltage, fire, electrolyte spillage); see the post-crash skills.

## 5. CAE process
Cell and module models (or homogenised mechanical equivalents) correlated to component crush tests; whole-vehicle pole and rear impact; predict intrusion at cell level and damage to contactors and busbars. Include the HV disconnect (pyrotechnic fuse or contactor) response time.

## Failure modes
- A pole entering at sill height and striking the pack edge.
- Sill collapse from a joint failure not captured in the CAE.
- Pack mount bolt shear letting the pack move into the cabin.

## Verify
- [ ] Intrusion limits traced to cell abuse test data.
- [ ] CAE correlated with component and full-vehicle tests.
- [ ] Post-crash HV safety strategy (disconnect, isolation) reviewed.
- [ ] Applicable regulation editions confirmed with the approval authority.
