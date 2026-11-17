---
id: engineering-technology.biomedical-engineering.biomaterials.taper-corrosion
name: taper-corrosion
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [taper-corrosion, implant-corrosion, fretting-corrosion, mechanically-assisted-crevice-corrosion, modular-taper, head-neck-junction, astm-f1875, trunnionosis]
level: advanced
status: verified
description: "Understand and test modular taper fretting corrosion in hip implants: mechanically assisted crevice corrosion, risk factors, design levers and ASTM F1875 test approach."
sources: ["ASTM F1875 Standard practice (revised 2026 as a test method) for fretting corrosion testing of modular implant interfaces: hip femoral head-bore and cone taper interface (confirm edition)", "Gilbert, Buckley and Jacobs, In vivo corrosion of modular hip prosthesis components in mixed and similar metal combinations (J Biomed Mater Res 1993;27)", "Jacobs, Urban and Gilbert, Corrosion of metal orthopaedic implants (J Bone Joint Surg Am 1998)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modular taper fretting corrosion

**Goal:** limit corrosion and metal release at the head-neck taper junction of modular hip implants.

## Mechanism
At a modular taper, micromotion under load removes the passive oxide film (**fretting**); within the narrow crevice the local chemistry becomes acidic and chloride-rich, so repassivation is hindered and corrosion proceeds (**mechanically assisted crevice corrosion, MACC**). Corrosion products (metal ions, particles) cause adverse local tissue reactions.

## Risk factors (from clinical and retrieval studies)
- **Material pairing:** cobalt-chromium heads on titanium stems show more corrosion in many retrievals than matching metals; ceramic heads avoid CoCr but can fracture and may corrode the stem taper at the contact.
- **Head size and offset:** larger heads and longer neck offsets increase torque and bending at the taper.
- **Taper design:** angle, length, surface finish (machining grooves) and engagement geometry control contact area and micromotion.
- **Assembly:** insufficient impaction force or contamination (blood, fluid) in the taper reduces locking strength; surgical technique instructions matter.
- **Patient factors:** weight, activity.

## Design levers
Same-metal pairing or ceramic or ceramic-sleeved heads with attention to stem taper; optimise taper geometry and finish for engagement; add corrosion-resistant coatings; define assembly forces and instructions.

## Testing
1. **ASTM F1875**: fretting corrosion testing of modular head-bore and cone taper interfaces. The 1998 practice has a long-term method (corrosion products and debris) and a short-term electrochemical method, recommends proteinaceous solutions, and warns against using it to rank material combinations; it has been revised as a long-term test method (F1875-26), so confirm the current edition. Onset-load and corrosion-current style metrics are used in the literature; define them in your protocol.
2. Standardised assembly (for example impacting at defined force) and non-standard assembly conditions (contaminated or misaligned).
3. Post-test inspection of taper surfaces by SEM and stereo microscopy (fretting scars, pits) and a quantitative scoring system such as the retrieval corrosion damage score.
4. Ion release measurements (ICP-MS) from test fluid.
5. Combine with fatigue test per ISO 7206 for the stem and head.

## Verify
- [ ] Fretting corrosion metrics (for example onset load and corrosion currents) reported with assembly conditions.
- [ ] Retrieval data from similar designs reviewed in the risk file.
- [ ] Surgical technique and IFU specify cleaning and assembly forces.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
