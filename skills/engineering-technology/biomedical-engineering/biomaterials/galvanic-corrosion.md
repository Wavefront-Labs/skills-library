---
id: engineering-technology.biomedical-engineering.biomaterials.galvanic-corrosion
name: galvanic-corrosion
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [galvanic-corrosion, implant-corrosion, fretting-corrosion, galvanic-series, zero-resistance-ammeter, astm-g71, astm-g82, mixed-metals, area-ratio]
level: advanced
status: draft
description: "Assess galvanic coupling between dissimilar implant metals: galvanic series, area ratio, zero-resistance ammeter tests, mixed-metal rules and design avoidance."
sources: ["ASTM G71 Standard guide for conducting and evaluating galvanic corrosion tests in electrolytes (confirm edition)", "ASTM G82 Standard guide for development and use of a galvanic series for predicting galvanic corrosion performance", "Jacobs, Gilbert and Urban, Corrosion of metal orthopaedic implants (J Bone Joint Surg Am 1998)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Galvanic corrosion in implants

**Goal:** avoid unplanned galvanic couples between different metals in contact in the body.

## Mechanism
When two dissimilar metals touch in an electrolyte (body fluid), the more active (anodic) one corrodes faster and the nobler (cathodic) one corrodes slower. The driving force is the potential difference; the corrosion rate depends on current, which depends on the cathode-to-anode **area ratio** and the kinetics of oxygen reduction on the cathode. Small anode with large cathode is the worst case.

## Passive metals in practice
Implant alloys (Ti-6Al-4V, CoCrMo, 316L) are passive, with small potential differences when passive, so galvanic currents in the body are usually low; damage rises when passive films are disrupted (fretting at modular tapers, crevices, scratches) or when stainless steel is coupled with other alloys.
Conventional practice: avoid mixing stainless steel with titanium or cobalt-chrome in the same load-bearing construct, and keep any mixed-metal modular interface supported by test data.

## Test approach
1. Choose the couple, area ratio and geometry that match the device (including crevices).
2. Measure open-circuit potentials in simulated body fluid (phosphate-buffered saline, or serum solutions) at 37 C.
3. Couple with a **zero-resistance ammeter** and record galvanic current and potential over days to weeks (ASTM G71 and G82 give the framework).
4. Add mechanical motion (fretting) if the couple is a modular junction, since this resets the passive film.
5. Evaluate corrosion product release (ICP-MS on the solution) and surface damage (SEM).

## Design rules
- Use the same alloy family for all metal parts in contact.
- Avoid crevices and small-area anodic parts in large-area cathodic assemblies.
- Coatings and anodised layers (insulating) interrupt galvanic paths only if intact.

## Verify
- [ ] Couple current density is low and stable compared with the passive current of single metals.
- [ ] No pitting or crevice attack under SEM at the interface.
- [ ] Ion release evaluated in the biological evaluation plan.
