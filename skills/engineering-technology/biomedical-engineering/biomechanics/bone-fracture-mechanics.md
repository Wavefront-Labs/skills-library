---
id: engineering-technology.biomedical-engineering.biomechanics.bone-fracture-mechanics
name: bone-fracture-mechanics
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [bone-fracture, fracture-mechanics, fracture-toughness, crack-propagation, cortical-toughness]
level: advanced
status: draft
description: "Apply fracture mechanics to bone: toughness testing, crack deflection at osteon boundaries, R-curve behaviour, age and orientation effects, and use in fixation design."
sources: ["Nalla, Kinney and Ritchie, Mechanistic fracture criteria for the failure of human cortical bone (Nature Materials, 2003)", "Cowin (ed.), Bone Mechanics Handbook", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Bone fracture mechanics

**Goal:** quantify resistance to crack growth in bone rather than relying on strength alone.

## Concepts
- Cortical bone fractures by crack growth; **toughness** is the resistance to crack extension (stress intensity K_c or energy J_c).
- **Orientation:** cracks growing across osteons (transverse) are tougher than along them, since crack deflection at cement lines and uncracked-ligament bridging dissipate energy.
- **R-curve:** toughness rises as the crack extends; a single K value hides this. Report crack-growth resistance versus extension.
- Typical cortical bone toughness is of the order of a few MPa times the square root of metre, and falls with age and in the presence of microdamage and altered collagen (confirm values for your use).

## Testing
1. Machined compact tension or single-edge-notched bending specimens with a sharp pre-crack, hydrated, with crack in a defined orientation.
2. Measure load, crack-mouth opening and crack length (compliance or optical); compute K or J per the fracture standard principles for metallic or ceramic materials adapted for bone; check size validity conditions.
3. Report orientation, age, density and loading rate.

## Design relevance
- Fixation holes, screw threads and plate edges act as stress raisers; crack-like defects around implants and press-fit fracture risk are assessed with FE and toughness data.

## Verify
- [ ] Crack orientation and size validity criteria stated.
- [ ] R-curve or multiple crack extensions reported, not a single point.
- [ ] Conclusions stay within the tested population (age, site).

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
