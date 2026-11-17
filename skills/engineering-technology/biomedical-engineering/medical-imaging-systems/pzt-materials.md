---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.pzt-materials
name: pzt-materials
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [pzt, piezoelectric-ceramic, piezocomposite, pmn-pt, transducer-materials]
level: advanced
status: draft
description: "Select ultrasound transducer piezo materials: PZT ceramics, 1-3 piezocomposites, single-crystal PMN-PT and polymers, with coupling, acoustic impedance and depoling limits."
sources: ["Shung, Diagnostic Ultrasound: Imaging and Blood Flow Measurements", "Szabo, Diagnostic Ultrasound Imaging: Inside Out", "https://www.ieee-uffc.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PZT and piezocomposite materials

**Goal:** choose active material that gives bandwidth, sensitivity and manufacturability for the probe.

## Materials
- **PZT (lead zirconate titanate) ceramics** (for example soft PZT types): high coupling and permittivity; acoustic impedance high, of the order of 30 MRayl, so matching layers to tissue (about 1.5 MRayl) are needed (see matching-backing-layers).
- **1-3 piezocomposites:** PZT pillars in polymer; lower impedance (of the order of 8 to 20 MRayl), higher thickness-mode coupling and bandwidth, and better array element isolation; harder to make.
- **Single-crystal relaxor materials (PMN-PT):** very high coupling and sensitivity, giving wider bandwidth; more temperature and depoling sensitivity, and cost.
- **PVDF polymers:** low impedance, broadband, low sensitivity; used for hydrophones and some high-frequency work.

## Selection factors
- Thickness-mode electromechanical coupling (kt), dielectric constant (electrical matching to cable and front end), acoustic impedance, loss, and temperature stability.
- **Curie temperature and depoling:** exposure to high temperature (soldering, sterilisation, autoclave) or high field can depole; define process limits.
- Array fabrication: dicing, kerf filling, element crosstalk, and lens and backing choices.
- Lead-containing materials: regulatory restrictions on lead in some regions (confirm exemptions for medical devices).

## Verify
- [ ] Impedance and coupling measured on samples and finished elements.
- [ ] Process temperature limits documented.
- [ ] Element sensitivity and bandwidth uniformity across an array measured.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
