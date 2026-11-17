---
id: engineering-technology.biomedical-engineering.biomaterials.astm-f136-eli-titanium
name: astm-f136-eli-titanium
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [astm-f136, titanium-alloys, ti-6al-4v, ti-6al-4v-eli, iso-5832-3, implant-titanium, extra-low-interstitial, alpha-case]
level: practitioner
status: verified
description: "Specify ASTM F136 Ti-6Al-4V ELI for implants: composition and interstitial limits, minimum mechanical properties, microstructure requirements, heat treatment and traceability."
sources: ["ASTM F136 Standard specification for wrought titanium-6 aluminum-4 vanadium ELI alloy for surgical implant applications (UNS R56401; confirm current edition)", "ASTM F1472 Wrought Ti-6Al-4V alloy (standard interstitial grade)", "ISO 5832-3 Implants for surgery - Metallic materials - Wrought titanium 6-aluminium 4-vanadium alloy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ASTM F136 Ti-6Al-4V ELI

**Goal:** buy and control the standard implant titanium alloy so that mechanical properties, microstructure and traceability are right.

## Material
- Alpha-beta titanium alloy, UNS R56401. Nominal composition 6% aluminium and 4% vanadium (limits approximately Al 5.5-6.5 and V 3.5-4.5 wt% (gated: unconfirmed, source is paywalled or blocked)), balance titanium.
- **ELI (extra low interstitial):** tighter limits on oxygen (maximum about 0.13 wt% (gated: unconfirmed, source is paywalled or blocked)), iron (about 0.25 (gated: unconfirmed, source is paywalled or blocked)), carbon, nitrogen and hydrogen than standard Ti-6Al-4V (F1472 permits oxygen up to about 0.20 (gated: unconfirmed, source is paywalled or blocked)). Lower interstitials improve ductility, fracture toughness and fatigue crack growth resistance. Confirm limits in the current standard.
- **Minimum mechanical properties (annealed bar, as commonly cited):** ultimate tensile strength about 860 MPa, 0.2% yield about 795 MPa, elongation about 10% (thin bar sizes, as shown in supplier datasheets citing F136; (gated: unconfirmed, source is paywalled or blocked)); reduction of area requirements depend on product size and are not stated here, so confirm them in the standard for the product form.

## Microstructure
The standard requires an alpha-beta microstructure with limits on continuous alpha at prior beta grain boundaries and on alpha case (a brittle oxygen-enriched surface layer formed in air at high temperature, which must be removed by machining or pickling). Microstructure of finished parts is checked by metallography.

## Processing notes
- Heat treatment in vacuum or inert gas; avoid hydrogen pickup during pickling; remove alpha case after forging or casting.
- Cold working and machining generate heat, so parameters control to avoid surface damage; finish by passivation or anodising as specified.
- For AM versions use ASTM F3001 (see lpbf-titanium-process).

## Buying controls
1. Specify standard and edition, product form (bar, plate), condition, and certificate type.
2. Require heat number traceability from melt to finished device, mill certificate of analysis for chemistry and mechanical tests.
3. Qualify the supplier (audit; multiple-melt vacuum arc remelting is typical).
4. Incoming inspection: chemistry spot check (XRF or OES), hardness, microstructure per lot or per heat as required by your quality plan.

## Verify
- [ ] Certificate shows compliance for chemistry, tensile and microstructure.
- [ ] Alpha case removed on machined surfaces from hot forming.
- [ ] Traceability preserved to device lot records.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
