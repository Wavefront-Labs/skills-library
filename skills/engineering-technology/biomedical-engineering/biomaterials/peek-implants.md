---
id: engineering-technology.biomedical-engineering.biomaterials.peek-implants
name: peek-implants
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [peek-implant, uhmwpe, peek, polyetheretherketone, spinal-cage, carbon-fiber-peek, radiolucent, astm-f2026]
level: practitioner
status: verified
description: "Use PEEK in implants: properties, carbon-fibre grades, radiolucency and MRI behaviour, bone on-growth limits and coatings, processing, sterilisation and ASTM F2026 controls."
sources: ["Kurtz, PEEK Biomaterials Handbook", "ASTM F2026 Standard specification for polyetheretherketone (PEEK) polymers for surgical implant applications (confirm edition)", "ISO 10993-1 Biological evaluation of medical devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PEEK implants

**Goal:** use polyetheretherketone where its radiolucency, bone-like stiffness and chemical stability suit the application, and manage its limits.

## Properties (typical unfilled implant grade)
- Semi-crystalline thermoplastic: melting point about 343 C and glass transition about 143 C (Wikipedia PEEK article).
- Elastic modulus about 3-4 GPa (closer to cortical bone than titanium at about 110 GPa (gated: unconfirmed, source is paywalled or blocked)); tensile strength about 90-100 MPa.
- **Carbon fibre reinforced PEEK** (for example 30% CF) reaches a modulus of about 18 GPa (gated: unconfirmed, source is paywalled or blocked), adjustable by layup, with high fatigue resistance.
- Radiolucent (images without metal artefacts), MR compatible, resistant to steam, EO and gamma sterilisation, and chemicals.

## Applications
Spinal interbody cages, cranial and maxillofacial implants, trauma plates (carbon fibre PEEK), suture anchors, radiolucent instruments.

## Limits and design considerations
- **Bone integration:** PEEK is bioinert and shows limited bone on-growth, so cages use surface treatments (titanium plasma spray, hydroxyapatite, porous titanium layers), roughened or additively manufactured porous PEEK, or titanium-coated designs.
- **Radiolucency** requires radiopaque markers (tantalum, titanium pins) for position checking on X-ray.
- **Notch sensitivity** and creep: sharp corners reduce fatigue life; include radii.
- **Sterilisation** and ageing: gamma is acceptable; test properties after the final cycle.
- **Processing:** injection moulding or machining from rod (ASTM F2026 controls the polymer); high mould temperature; cleanliness to avoid contaminant inclusions.
- **Wear debris** from PEEK on PEEK articulations is a concern for bearings; mostly used as non-articulating components.

## Standards and testing
- Material standard ASTM F2026 for the polymer; ASTM F2077 (static and dynamic) and F2267 (subsidence) for intervertebral body fusion devices (check scope and edition).
- Biological evaluation per ISO 10993 on the finished sterilised device.

## Verify
- [ ] Resin lot certificate matches ASTM F2026.
- [ ] Mechanical tests of the device after sterilisation.
- [ ] Imaging and marker visibility checked.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
