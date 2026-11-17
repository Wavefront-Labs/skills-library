---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.myoelectric-site-selection
name: myoelectric-site-selection
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [myoelectric-sites, upper-limb-prosthesis, myoelectric, emg-control-sites, two-site-control, electrode-placement, transradial]
level: practitioner
status: draft
description: "Find and verify surface EMG control sites for myoelectric upper-limb prostheses: palpation, signal testing, two-site control, electrode fit and typical failures."
sources: ["Parker, Englehart and Hudgins, Myoelectric signal processing for control of powered limb prostheses (J Electromyogr Kinesiol 2006)", "Smith, Michael and Bowker (eds.), Atlas of Amputations and Limb Deficiencies (AAOS)", "Manufacturer EMG test-software guides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Myoelectric control site selection

**Goal:** locate two independent, strong, repeatable muscle signal sites (typically wrist flexor and extensor groups) to drive open and close of a hand or other device.

Fitting is by a prosthetist or occupational therapist trained in myoelectric systems.

## Procedure
1. **Palpate** residual forearm during requested contractions (wrist flexion and extension intent, hand open and close) to find muscle bellies; mark candidate sites.
2. **Test** with a surface electrode and an EMG test tool: sites should show clear amplitude increase (typically tens to hundreds of microvolts above rest noise, often up to millivolts), with limited co-contraction.
3. **Choose** two sites with good signal and independence (separate flexor and extensor muscles); avoid sites where crosstalk makes both channels fire on one contraction.
4. **Electrodes:** stainless steel or gold dry electrodes in the socket, with a reference electrode. Skin contact depends on socket fit; electrode pressure should be even and comfortable.
5. **Control schemes:** direct two-site (open on extensor, close on flexor); single-site co-contraction switching for terminals/wrist; proportional control where speed follows amplitude; thresholds and gains set in the controller.
6. **Train:** short sessions with feedback (visual EMG trainer, virtual hand) before final socket fabrication; check muscle fatigue and endurance.

## Failure causes
- Sweat, electrode lift-off during arm movement, limb volume change, cable breakage, interference from other devices, electrode shift under load.

## Verify
- [ ] Both sites produce signals at least a few times resting noise.
- [ ] Independent open and close control with the arm in several positions (arm-position effect).
- [ ] Socket fit tested under load and in motion.
