---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.filtration-and-hvl
name: filtration-and-hvl
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [half-value-layer, x-ray-tube, x-ray-generation, hvl, added-filtration, beam-quality, aluminium-equivalent, effective-energy]
level: practitioner
status: gated
description: "Measure and choose X-ray filtration and half-value layer: narrow-beam HVL method, effective energy, added copper filtration, dose-contrast trade-offs and regulatory minimums."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (X-ray beam quality)", "IEC 60601-1-3:2008+AMD1:2013+AMD2:2021 consolidated edition 2.2 Radiation protection in diagnostic X-ray equipment (https://webstore.iec.ch/en/publication/68449)", "US 21 CFR 1020.30(m) https://www.ecfr.gov/current/title-21/part-1020/section-1020.30"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Filtration and half-value layer (HVL)

**Goal:** characterise beam quality and set filtration that removes low-energy photons that add skin dose without contributing to the image.

## HVL
**HVL** is the thickness of a specified material (aluminium, high purity) that reduces the air kerma of the beam to half. Higher HVL means a harder (more penetrating) beam. The effective attenuation coefficient is mu = ln 2 / HVL; the effective energy of the beam is typically one third to one half of the peak kVp.

## Measurement
1. Fix the tube at the specified kVp, with a calibrated dosimeter (ion chamber or solid-state detector with suitable energy response) well away from scatter sources.
2. Use **narrow-beam geometry**: small field, filters placed halfway between source and detector, detector far from filters, to avoid scatter inflating readings.
3. Measure air kerma without filters, then with increasing thicknesses of 1100-alloy (or equivalent high-purity) aluminium sheets.
4. Plot ln(kerma) against thickness and interpolate the thickness for 50% (or use measured points bracketing 50%).
5. Record kVp waveform, anode angle and total filtration so the HVL is reproducible.

## Choosing filtration
- Inherent filtration (tube window, oil, housing) plus added aluminium; total aluminium equivalent filtration commonly at least about 2.5 mm Al in general radiography (gated: unconfirmed, source is paywalled or blocked) (IEC 60601-1-3 and national rules specify minimums; confirm).
- **Added copper (0.1-0.3 mm)** with aluminium is used in paediatric, fluoroscopy and some CT or radiography to reduce dose, with a contrast trade-off.
- Mammography uses molybdenum or rhodium filters matched to the anode for the characteristic X-ray spectrum.

## Regulatory
Regulations set a minimum HVL as a function of kVp to limit skin dose (21 CFR 1020.30(m)(1), table 1, which gives separate minimum HVL columns for dental intraoral systems, for other systems made before 10 June 2006 and for systems made on or after 10 June 2006; linear interpolation is allowed between listed kVp values); confirm the table in the current text for your market and generator type.

## Verify
- [ ] HVL measured at several kVp and compared with the regulatory minimum and manufacturer specification.
- [ ] kVp accuracy measured at the same time.
- [ ] Check at the end of tube life (the tube window and anode roughening change HVL).
