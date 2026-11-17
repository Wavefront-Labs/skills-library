---
id: defence-public-safety.customs-border-and-wildlife-enforcement.inspection-and-screening-systems.x-ray-image-review-radiation-portal-alarms-and-trace-detection
name: x-ray-image-review-radiation-portal-alarms-and-trace-detection
category: defence-public-safety
field: customs-border-and-wildlife-enforcement
product: inspection-and-screening-systems
tags: [customs-border-and-wildlife-enforcement, inspection-and-screening-systems, x-ray, dual-energy-x-ray, baggage-scanner, cargo-scanner, nii, non-intrusive-inspection, image-interpretation, effective-atomic-number, colour-coding, radiation-portal-monitor, rpm, norm, naturally-occurring-radioactive-material, riid, radioisotope-identification, personal-radiation-detector, etd, ion-mobility-spectrometry, trace-detection, swabbing, false-alarms, alarm-resolution, radiation-safety, alara]
level: practitioner
status: draft
description: "Operate border screening kit: read dual-energy X-ray images against the manifest, resolve radiation portal alarms with secondary screening, and run trace detection swabs without contamination."
sources: ["IAEA Nuclear Security Series guidance on detection at borders (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# X-ray image review, radiation portal alarms and trace detection

**Goal:** use non-intrusive inspection equipment to decide quickly which bags, vehicles and
containers need physical examination, and resolve alarms methodically rather than either
ignoring them or opening everything. Vendor interfaces differ (Smiths Detection, Rapiscan,
Nuctech, Leidos and others); the principles below are common.

## 1. Dual-energy X-ray image review
- Dual-energy systems estimate **effective atomic number (Zeff)** and colour-code it. A
  common convention: **orange** = organic (low Zeff: food, plastics, drugs, many explosives),
  **green** = mixed/light inorganic, **blue** = metals/inorganic, **black** = too dense to
  penetrate. Check your system's legend; conventions vary.
- **Compare image to declaration.** The core cargo question is "does this look like what the
  manifest says?" — density, uniformity, packing pattern, item count, weight vs declared weight.
- Look for anomalies: inconsistent density within uniform goods, structural features that
  don't belong (extra walls, thickened floors, items inside items), organic masses in
  places that should be empty, dense areas you can't explain.
- Use the tools: contrast/edge enhancement, organic/inorganic strip, zoom, and for
  multi-view systems compare views to locate objects in 3D. CT baggage systems give slice views.
- Black (impenetrable) areas must be resolved by other means — re-scan at a different angle or
  open the item.
- Image libraries and threat-image projection (TIP) in aviation-style systems keep screener
  performance measurable; review your hit/miss data.

## 2. Radiation portal monitor (RPM) alarms
- Portals detect gamma (and often neutron) radiation from vehicles and containers passing
  through. **Most alarms are naturally occurring radioactive material (NORM):** ceramics,
  granite and tiles, fertiliser (potassium), cat litter, some foods, and medical patients
  recently treated with radiopharmaceuticals.
- Never dismiss an alarm on the first pass. Standard **secondary inspection**: re-scan; use a
  handheld **radioisotope identification device (RIID)** to identify the isotope and localise
  the source; compare with the manifest (e.g. K-40 consistent with declared fertiliser).
- Neutron alarms and isotopes inconsistent with declared goods, or industrial/medical sources
  (Cs-137, Co-60, Am-241, Ir-192), are escalated to the national technical reachback/expert
  support per protocol. Isolate the conveyance at a safe distance meanwhile.
- **Radiation protection:** time, distance, shielding (ALARA). Wear your personal radiation
  detector/dosimeter and follow its alarm thresholds.
- Record every alarm and its resolution; nuisance-alarm statistics justify threshold tuning.

## 3. Trace detection (ETD/IMS)
- Swab surfaces most likely to be touched (handles, zips, closures, latches) and the swab is
  analysed, typically by ion mobility spectrometry, for drug or explosive residues.
- Run verification/calibration checks with the supplied test swabs at the start of each shift
  and per manufacturer schedule; record results.
- Use fresh gloves and new swabs; never swab a known-positive aid near the screening area —
  contamination of the instrument or the area produces cascades of false positives.
- A positive trace is an indicator for further search, not proof; many substances cross-react
  and residues transfer innocently (e.g. banknotes).

## Gotchas
- Reviewing the image without the manifest open next to it.
- "Known NORM" assumptions — confirm with the RIID every time.
- Skipping the start-of-shift verification on trace kit.
- Letting the queue pressure shorten review time below what the procedure requires.

## Verify
- [ ] Each image decision records consistency with declaration.
- [ ] Every RPM alarm resolved with RIID result and logged.
- [ ] Trace detector verification passed and logged this shift.
- [ ] Personal dosimeter worn and read per schedule.

*Uncertainty:* colour conventions and alarm protocols are vendor- and agency-specific; this is
a generic summary.
