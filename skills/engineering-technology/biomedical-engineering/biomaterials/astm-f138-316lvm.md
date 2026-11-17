---
id: engineering-technology.biomedical-engineering.biomaterials.astm-f138-316lvm
name: astm-f138-316lvm
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [astm-f138, 316l-stainless, cobalt-chromium, 316lvm, stainless-steel-implant, iso-5832-1, surgical-implant-steel, uns-s31673]
level: practitioner
status: verified
description: "Specify ASTM F138 316LVM stainless steel for surgical implants: composition, melting practice, cold work and uses, corrosion limits and nickel and MRI considerations."
sources: ["ASTM F138 Standard specification for wrought 18 chromium-14 nickel-2.5 molybdenum stainless steel bar and wire for surgical implants (UNS S31673; confirm current edition)", "ASTM F139 sheet and strip (UNS S31673)", "ISO 5832-1 Implants for surgery - Metallic materials - Wrought stainless steel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ASTM F138 (316LVM) stainless steel

**Goal:** specify and use implant-grade austenitic stainless steel correctly.

## Material
- Austenitic Fe-Cr-Ni-Mo steel (UNS S31673); the main constituents are about 17-19% Cr, 13-15% Ni and 2.25-3% Mo, with low carbon (maximum 0.03%) (gated: unconfirmed, source is paywalled or blocked). Confirm composition limits in the current standard, which also sets limits on N, Cu, P, S and Si.
- **"VM":** vacuum melted (vacuum induction melting, often followed by vacuum arc remelting) to reduce inclusions and improve fatigue and corrosion resistance. Standard also includes limits for inclusion content, microstructure (no delta ferrite, grain size) and a pitting resistance indicator.
- Delivered annealed or cold worked (for example 30% cold-worked (gated: unconfirmed, source is paywalled or blocked)) to raise yield and ultimate strength; the standard defines condition-specific properties. Cold-worked bar commonly gives yield several hundred MPa higher than annealed.

## Uses and limits
- Temporary and some permanent devices: bone plates and screws, intramedullary nails, cerclage wire, surgical instruments (instrument grades differ). Fixation hardware generally avoids prolonged implantation that exceeds corrosion margin.
- Cold-formed contact areas and screw-plate interfaces are prone to crevice and fretting corrosion; surface passivation after machining is required (see passivation-astm-f86).
- **Nickel:** release can cause sensitisation in sensitive patients; consider alternatives (titanium) for known allergy and state in labelling when relevant.
- **MRI:** austenitic stainless steel is generally low susceptibility but not guaranteed; test per the ASTM MRI standards (F2052 force, F2213 torque, F2182 heating, F2119 artefact; (gated: unconfirmed, source is paywalled or blocked)) for MR Conditional claims.

## Buying and controls
- Specify the standard, edition, condition, heat traceability and certificates of analysis; require supplier audits.
- Incoming inspection: chemistry (OES or XRF as screening), hardness, microstructure and surface.

## Verify
- [ ] Material certificate with heat number and passes the F138 composition.
- [ ] Mechanical properties for the ordered condition.
- [ ] Passivation and corrosion tests on the finished device per the plan.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
